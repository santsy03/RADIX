
___author__ = "mjanja"

from twisted.web import http
from mg_aapcn_me2u.src.configs.config import ACK as ack
#from utilities.metrics.core import count
#from mg_aapcn_me2u.src.configs.config import HITS as hits
from mg_aapcn_me2u.src.consumer.client import InternetMe2uClient as client 
from mg_aapcn_me2u.src.lib.core import process_change_password 

def get_params(request):
    ''' 
    retrieves the values of http post or get valuables
    '''
    params = {}
    for key, val in request.args.items():
        params[key] = val[0]
    print params
    return params

def process_change_pin(request):
    '''
    processes a change pin request
    '''
    params = get_params(request)
    print params

    curr_pin = params['curr_pin']
    new_pin = params['new_pin']
    confirm_pin = params['confirm_pin']
    lang = params['lang']
    msisdn = params['msisdn']
    
    response = str(ack[lang])
    request.write(response)
    print response
    request.finish()

    try:
        process_change_password(curr_pin, new_pin,
            confirm_pin, lang, msisdn)
    except Exception, err:
        raise err
    
def process_provision(request):
    '''
    1) provisions a valid request
    2) sends correct messages for invalid responses
    '''
    params = get_params(request)
    response = None

    unit = params['unit']
    sender_msisdn = params['msisdn']
    recipient = params['b_number']
    pin = params['pin']
    lang = params['lang']
    amount = params['amount']

    if unit == 'GB':
        amount = int(amount) *1024

    message = [sender_msisdn, recipient, str(amount), pin, lang]
    message = "||".join(message)

    print client(message)
    response = str(ack[lang])
    request.write(response)
    print response
    request.finish()


class RequestHandler(http.Request):
    '''
    class to handle HTTP requests
    from flares
    '''

    pages = {'/provision': process_provision,
            '/changepin':process_change_pin}

    def __init__(self, channel, queued):
        http.Request.__init__(self, channel, queued)

    def process(self):
        ''' 
        overriden to provide custome handling
        of requests 
        '''
        from twisted.internet import threads
        if self.path.__contains__('provision'):
            handler = process_provision
        elif self.path.__contains__('changepin'):
            handler = process_change_pin
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

