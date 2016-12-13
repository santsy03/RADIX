___author__ = "rono"

from twisted.web import http
from core import provision_request
from core import setup
import config


def get_params(request):
    '''
    retrieves the values of http post or get valuables
    '''
    params = {}
    for key, val in request.args.items():
        params[key] = val[0]
    return params


def sendResponse(response, request):
    request.write(response)
    request.finish()


def process_provision_request(request):
    '''
    1) provisions a valid request
    '''
    params = get_params(request)
    print 'Params::' + str(params)
    msisdn = params['msisdn']
    action = params['action']
    parameters = params
    resources = setup(resources={})
    resources['parameters'] = parameters
    try:
        resp = provision_request(resources)
    except Exception, err:
        error = ("error provisioning request for: %s "
                 "| %s error:%s" % (msisdn, action, str(err)))
        print error
        resp = config.MESSAGES['error']
    else:
        print "made request for %s" % (msisdn)
    finally:
        sendResponse(resp, request)


class RequestHandler(http.Request):
    '''
    class to handle HTTP requests
    from flares
    '''

    pages = {'/process': process_provision_request}

    def __init__(self, channel, queued):
        http.Request.__init__(self, channel, queued)

    def process(self):
        '''
        overriden to provide custome handling
        of requests
        '''
        from twisted.internet import threads
        if self.path.__contains__('process'):
            handler = process_provision_request
        else:
            handler = self.pages[self.path]
        defer = threads.deferToThread(handler, self)
        defer.addErrback(self.handle_failure)

        return defer

    def get_connections(self):
        '''
        avails database connection pool from the RequestProtocol object
        '''
        return self.channel.get_db_connection()

    def handle_failure(self, error):
        print "exception: %s " % (error.getTraceback())


class RequestProtocol(http.HTTPChannel):

    requestFactory = RequestHandler

    def get_db_connection(self):
        '''
        avails database connection pool from the RequestFactory object
        '''
        connections = {}
        return connections


class RequestFactory(http.HTTPFactory):
    protocol = RequestProtocol

    def __init__(self):
        '''
        Setup for resources to be used by the service
        '''
        http.HTTPFactory.__init__(self)
