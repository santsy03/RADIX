import logging
from logging.handlers import TimedRotatingFileHandler

from twisted.web import http
from twisted.internet import threads
from configs.config import databases
from cx_Oracle import SessionPool as sp
from utilities.secure.core import decrypt
from utilities.logging.core import log
from utilities.common.core import (verify_params, 
        MissingParameterException)
from authentication.configs import DB_POOL, HTTP, LOGS, cdrlogger
from authentication.common.core import (authenticate, change_password,
        unlock_account, reset_password, create_user_account)


def get_params(request):
    '''
    retrieve request params and add to dict
    '''
    try:
        params = {}
        for key, val in request.args.items():
            params[key] = val[0]
        log({}, 'request params - %s' % params, 'debug')
        return params
    except Exception, err:
        log({}, 'get_params() fail - %r' % err, 'error')
        raise err


def write_response(response, request):
    '''
    write http response
    '''
    try:
        request.write(str(response))
        request.finish()
    except Exception, err:
        log({}, 'write_response() fail - %r' % err, 'error')
        write_error(request, 'error')


def write_error(request, error):
    '''
    write error on http response
    '''
    try:
        request.write(str(error))
        request.finish()
    except Exception, err:
        log({}, 'write_error() fail - %r' % err, 'error')
        return


def setup(func):
    '''
    decorator that defines resources dict

    Adds below keys to resources:

    db_connection  :  dict with db connection object
    parameters     :  dict with request parameters
    cdr_logger     :  logger object 
    '''
    def __inner(request):
        try:
            resources = {}
            connection_pools = request.getConnections()
            resources['db_connection'] = connection_pools['core']
            resources['parameters'] = get_params(request)
            resources['cdr_logger'] = request.getLoggers()
            func(resources, request)
        except Exception, err:
            error = 'setup() fail - %r' % err
            log({}, error, 'error')
            raise err
    return __inner


@setup
def process_authentication(resources, request):
    '''
    authentication request handling/routing
    '''
    try:
        parameters = resources['parameters']
        verify_params(parameters, HTTP['args']['authenticate'])

        status = authenticate(resources, parameters['username'],
                parameters['password'])
        write_response(status, request)

    except MissingParameterException:
        write_error(request, 'missing_parameter')
        return
    except Exception, err:
        log(resources, 'process_authentication() fail - %r' % err, 'error')
        write_error(request, 'error')
    finally:
        cdrlogger.log_cdr(resources, parameters)


@setup
def process_change_password(resources, request):
    '''
    change_password request handling/routing
    '''
    try:
        parameters = resources['parameters']
        verify_params(parameters, HTTP['args']['change_password'])

        user = parameters['username']
        curr_password = parameters['current_password']
        new_password = parameters['new_password']
        status = change_password(resources, user, curr_password, new_password)
        write_response(status, request)

    except MissingParameterException:
        write_error(request, 'missing_parameter')
        return
    except Exception, err:
        log(resources, 'process_change_password() fail - %r' % err, 'error')
        write_error(request, 'error')
    finally:
        cdrlogger.log_cdr(resources, parameters)


@setup
def process_unlock(resources, request):
    '''
    unlock request handling/routing
    '''
    try:
        parameters = resources['parameters']
        verify_params(parameters, HTTP['args']['unlock'])

        status = unlock_account(resources, parameters['username'])
        write_response(status, request)

    except MissingParameterException:
        write_error(request, 'missing_parameter')
    except Exception, err:
        log(resources, 'process_unlock() fail - %r' % err, 'error')
        write_error(request, 'error')
    finally:
        cdrlogger.log_cdr(resources, parameters)


@setup
def process_reset(resources, request):
    '''
    reset request handling/routing
    '''
    try:
        parameters = resources['parameters']
        verify_params(parameters, HTTP['args']['reset'])

        status = reset_password(resources, parameters['username'])
        write_response(status, request)

    except MissingParameterException:
        write_error(request, 'missing_parameter')
    except Exception, err:
        log(resources, 'process_reset() fail - %r' % err, 'error')
        write_error(request, 'error')
    finally:
        cdrlogger.log_cdr(resources, parameters)


@setup
def process_create_user(resources, request):
    '''
    create user request handling/routing
    '''
    try:
        parameters = resources['parameters']
        verify_params(parameters, HTTP['args']['create_user'])

        args = [resources, parameters['username']]
        if 'password' in parameters: args.append(parameters['password'])
        status = create_user_account(*args)
        write_response(status, request)

    except MissingParameterException:
        write_error(request, 'missing_parameter')
    except Exception, err:
        log(resources, 'process_create_user() fail - %r' % err, 'error')
        write_error(request, 'error')
    finally:
        cdrlogger.log_cdr(resources, parameters)


def get_pages():
    '''
    returns mapping of servlet : process function
    '''
    pages = {}
    try:
        for page in HTTP['pages'].items():
            pages['/{0}'.format(page[0])] = eval(page[1])
    except Exception, err:
        log({}, 'get_pages() fail - %r' % err, 'error')
    else:
        return pages


def catch_error(*args):
    for arg in args:
        log({}, 'error from deffered - %r' % arg, 'error')
    return 'system error'


class requestHandler(http.Request):

    pages = get_pages()

    def __init__(self, channel, queued):
        http.Request.__init__(self, channel, queued)

    def process(self):
        if self.path in self.pages:
            handler = self.pages[self.path]
            d = threads.deferToThread(handler, self)
            d.addErrback(catch_error)
            return d
        else:
            self.setResponseCode(http.NOT_FOUND)
            self.write('page not found')
            self.finish()

    def getConnections(self):
        return self.channel.getDbConnection()

    def getLoggers(self):
        return self.channel.get_cdr_logger()


class requestProtocol(http.HTTPChannel):
    requestFactory = requestHandler

    def getDbConnection(self):
        connections = self.factory.connectionPools
        return connections

    def get_cdr_logger(self):
        cdr_logger = self.factory.cdr_logger
        return cdr_logger


class RequestFactory(http.HTTPFactory):
    protocol = requestProtocol
    isLeaf = True

    def __init__(self):
        http.HTTPFactory.__init__(self)
        db = databases['core']
        db_user = decrypt(db['username'])
        db_pas = decrypt(db['password'])
        db_string = db['string']
        db_conn = sp(db_user, db_pas, db_string, *DB_POOL[0], **DB_POOL[1])
        self.connectionPools = {}
        self.connectionPools['core'] = db_conn

        #-----------------------
        # custom logger for CDRs
        #-----------------------
        things = LOGS['cdr'].split('/')
        cdrlog = LOGS['cdr']
        cdr_logger = logging.getLogger(things[len(things) - 1])
        cdr_logger.setLevel(logging.DEBUG)
        cdr_handler = TimedRotatingFileHandler(LOGS['cdr'], **LOGS['when'])
        cdr_handler.setFormatter(logging.Formatter(LOGS['cdr_format']))
        cdr_logger.addHandler(cdr_handler)
        self.cdr_logger = cdr_logger
