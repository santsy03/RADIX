#!/usr/bin/env python

from twisted.web import http
from string import Template
from twisted.internet import threads,reactor,defer
from cx_Oracle import SessionPool
from utilities.logging.core import log

from modular_tariffs.src.configs import HTTP
from utilities.common.core import verify_params
from utilities.common.core import MissingParameterException
from modular_tariffs.src.configs import balance_actions
from modular_tariffs.src.configs import provision_actions
from modular_tariffs.src.configs import stop_actions
from modular_tariffs.src.configs import response_actions

from modular_tariffs.src.common import check_renewals
from modular_tariffs.src.requests.http.core import setup
from modular_tariffs.src.requests.http.core import create_request

from configs.config import databases
from utilities.secure.core import encrypt, decrypt

from modular_tariffs.src.requests.http.responses import get_action
from modular_tariffs.src.requests.http.responses import fetch_stop_response
from modular_tariffs.src.requests.http.responses import fetch_provision_response

def getParams(request):
    params = {}
    for k,v in request.args.items():
        params[k] = v[0]

    log( {}, 'headers - %s' % request.getAllHeaders(), 'debug' )
    try:
        params['auth_key'] = request.getHeader('auth_key')
    except Exception, err:
        error = 'getParams() - failed to get auth_key in request headers - %s' % request
        log( {}, error, 'error' )
        write_error( request, 'auth_failed' )

    return params


def write_error(request, error):
    '''
    writes http error on response
    '''
    log( {}, 'http error response - %s' % error )
    status_code = HTTP[str(error)]['code']
    status_msg = HTTP[str(error)]['desc']
    request.setHeader( 'status-code', status_code )
    request.write( status_msg )
    request.finish()

def write_response( request, resources ):
    '''
    write http response
    '''
    try:
        transaction_id = resources['parameters']['transaction_id']
        status_code = HTTP['queued']['code']
        log( resources, 'sending response - %s' % transaction_id, 'debug')
        request.setHeader( 'transaction_id', str(int(float(transaction_id))) )
        request.setHeader( 'status-code', status_code  )
        request.write( HTTP['queued']['desc'] )
        request.finish()
    except Exception, err:
        write_error( request, 'error' )


def fetch_auth_keys(resources):
    '''gets valid authentication keys from db
    '''
    try:
        from modular_tariffs.src.configs import USERS
        valid_users = []
        for user in USERS:
            valid_users.append( encrypt(user) )

        return valid_users
    except Exception, err:
        auth_err = 'op:fetch_auth_keys failed. - %s' % str(err)
        log( resources, auth_err, 'error' )


def auth(func):
    '''
    decorator that verifies request authenticity
    '''
    def __inner(request):
        resources = {}
        connection_pools = request.getConnections()
        resources['db_connection'] = connection_pools['core']
        resources['connections'] = connection_pools['core']
        resources['parameters'] = getParams(request)
        log( {}, resources['parameters'] )
        parameters = resources['parameters']
        
        try:
            #authenticate
            assert parameters['auth_key'] in fetch_auth_keys(resources)
        except AssertionError:
            write_error( request, 'auth_failed' )
            return
        except KeyError:
            write_error( request, 'missing_parameter' )
            return
        except Exception, err:
            log( {}, 'op:auth - %s' % str(err) )
            write_error( request, 'error' )
            return

        func(request, resources)

    return __inner

@auth
def process_provision_request(request, resources):
    parameters = resources['parameters']

    try:
        verify_params(parameters, 
                ['msisdn', 'channel', 'package_id', 'renew', 'transaction_type'])
    except MissingParameterException:
        write_error(request, 'missing_parameter')
        return

    try:
        assert parameters['transaction_type'] in ('a','b')
    except AssertionError, er:
        write_error( request, 'invalid_transaction_type' )
        return

    if parameters['transaction_type'] == 'a':
        parameters['b_msisdn'] = parameters['msisdn']
    else:
        try:
            assert 'b_msisdn' in parameters
        except AssertionError:
            write_error( request, 'missing_parameter' )
            return

    resources['parameters'] = parameters

    try:
        create_request(resources, provision_actions[0])
    except:
        write_error( request, 'error' )
        return
    else:
        write_response( request, resources )

@auth
def process_balance_request(request, resources):
    parameters = resources['parameters']

    try:
        verify_params(parameters, 
                ['msisdn', 'channel'])
    except MissingParameterException:
        write_error( request, 'missing_parameter' )
        return

    parameters['b_msisdn'] = parameters['msisdn']
    parameters['transaction_type'] = 'a'
    parameters['renew'] = 'False'
    parameters['package_id'] = '0'

    if 'category' not in parameters:
        parameters['category'] = 'data'

    log( resources, '%s - balance check' % parameters['category'], 'debug' )

    resources['parameters'] = parameters
    create_request(resources, balance_actions[0])

    write_response( request, resources )

@auth
def process_stop_renewal_request(request, resources):
    parameters = resources['parameters']
    
    try:
        verify_params(parameters, 
                ['msisdn', 'channel'])
    except MissingParameterException:
        write_error( request, 'missing_parameter' )
        return

    parameters['b_msisdn'] = parameters['msisdn']
    parameters['transaction_type'] = 'a'
    parameters['renew'] = 'False'
    parameters['package_id'] = 'stop'

    resources['parameters'] = parameters
    create_request(resources, stop_actions[0])

    write_response( request, resources )

@auth
def retrieve_response(request, resources):
    '''routes request based on action'''
    action = get_action(resources)
    if not action:
        # invalid ID
        write_error( request, 'invalid_transaction_id' )
        return
    if (action in provision_actions or
            action in balance_actions):
        fetch_provision_response(resources)
        resp = resources['parameters']['resp']
        if action in balance_actions:
            # check renewals
            if check_renewals( resources ):
                resp['Active-Renewal'] = 'True'
                renewals = resources['parameters']['renewal_details']
                for ren in renewals:
                    resp['Renewal-Bundle'] = renewals[ren]['package_name']
                    resp['Renewal-Date'] = renewals[ren]['executed_at']
            else:
                resp['Active-Renewal'] = 'False'

    elif action in stop_actions:
        #resp = {'status-msg': 'no renewals', 'transaction_id': '214', 'status-code': '31'}  
        fetch_stop_response(resources)
        resp = resources['parameters']['resp']
        log( resources, 'fetch_stop_response() response - %s' % resp, 'debug' )
    else:
        log( resources, 'invalid action' )
        write_error( request, 'error' )

    try:
        for each in resp:
            value = resp[each]
            request.setHeader( each, value )
        log( resources, '-- written headers for -- %s' % resp, 'debug' )
    except Exception, err:
        log( resources, 'failed to write headers - %s' % str(err), 'error' )
        raise err

    request.write( resp['status-msg'] )
    request.finish()


def get_pages():
    pages = {}
    for action in provision_actions:
        pages['/%s'%action] = process_provision_request
    for action in balance_actions:
        pages['/%s'%action] = process_balance_request
    for action in stop_actions:
        pages['/%s'%action] = process_stop_renewal_request
    for action in response_actions:
        pages['/%s'%action] = retrieve_response
    return pages

class requestHandler(http.Request):
    
    pages = get_pages()

    def __init__(self,channel,queued):
        http.Request.__init__(self,channel,queued)

    def process(self):
        if self.pages.has_key(self.path):
            handler = self.pages[self.path]
            d = threads.deferToThread(handler,self)
	    d.addErrback(self.catchError)
            return d
        else:
            self.setResponseCode(http.NOT_FOUND)
            self.write('page not found')
            self.finish()

    def getConnections(self):
        return self.channel.getDbConnection()

    def catchError(self,request):
	return 'Error'


class requestProtocol(http.HTTPChannel):
    requestFactory = requestHandler

    def getDbConnection(self):
        connections = self.factory.connectionPools
        return connections

class RequestFactory(http.HTTPFactory):
    protocol = requestProtocol
    isLeaf = True

    def __init__(self):
        http.HTTPFactory.__init__(self)
        db = databases['core']
        db_user = decrypt(db['username'])
        db_pass = decrypt(db['password'])
        db_string = db['string']
        db_conn = SessionPool( db_user, db_pass, db_string, 5, 200, 5, threaded=True,)
        self.connectionPools = {}
        self.connectionPools['core'] = db_conn
