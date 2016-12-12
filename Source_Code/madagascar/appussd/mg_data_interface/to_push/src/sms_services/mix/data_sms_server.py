
___author__ = "mjanja"

from twisted.web import http
from utilities.sms.core import send_message
from utilities.ucip.core import get_balance_and_date
from mg_data_interface.src.configs.config import BUNDLES as bundles
from mg_data_interface.src.lib.core import enqueue_provision_request 
from mg_data_interface.src.lib.core import generate_air_tagging_params
from mg_data_interface.src.lib.core import disable_renewal 
from mg_data_interface.src.lib.core import b_number_is_valid
from mg_data_interface.src.configs.config import ACK as ack
from utilities.metrics.core import count
from mg_data_interface.src.configs.config import HITS as hits
from mg_data_interface.src.configs.config import BUY_KEYWORD

import traceback

allowed_service_class = [98, 909]

def get_params(request):
    ''' 
    retrieves the values of http post or get valuables
    '''
    params = {}
    for key, val in request.args.items():
        params[key] = val[0]
    return params


def is_valid_message(text):
    '''
    checks is the text is even valid
    '''

    if text.lower() == BUY_KEYWORD:
        return True
    else:
        return False

def number_is_on_correct_class(msisdn):
    '''
    validates the b number
    returns true or false
    '''
    resources = {}
    parameters = {}
    resources['parameters'] = parameters
    resources = generate_air_tagging_params(resources, "validate_number")
    resources['parameters']['msisdn'] = msisdn

    print resources
    try:
        resp = get_balance_and_date(resources)
    except IOError, err:
        print "ERROR: op|| b_number is valid %s " %(str(err))
        print traceback.format_exc()
        return False
    except Exception, err:
        print "ERROR: op|| b_number is valid %s " %(str(err))
        print traceback.format_exc()
        return False
    else:
        print "INFO resp code %s" % str(resp['responseCode'])
        if resp['responseCode'] == 0:
            if resp['serviceClassCurrent'] in allowed_service_class:
                return True
            else:
                print "DISALLOWED: current service class %s for msisdn %s" % (
                        str(resp['serviceClassCurrent']), msisdn)
                return False
        else:
            return False


def process_provision_request(request):
    '''
    1) provisions a valid request
    2) sends correct messages for invalid responses
    '''
    params = get_params(request)
    print params
    response = None

    package, msisdn, bp_msisdn, can_renew, is_web = \
            None, None, None, None, None
    text = params['txt']
    msisdn = params['msisdn']
    
    is_text = is_valid_message(text)
    print is_text
    if is_text:
        if number_is_on_correct_class(msisdn):
            package = '37'
            msisdn = params['msisdn']
            bp_msisdn = params['msisdn']
            can_renew = '0'
            response = str(ack['txt-1'])
            send_message(msisdn, response)
            print response
            request.write(response)
            request.finish()
            try:
                resp =enqueue_provision_request(package, 
                    msisdn, None, can_renew, is_web, False)
            except Exception, err:
                print "error enqueing request for provisioning"
                raise err
            else:
                print "made request for %s buying rta mix" % params['msisdn']
            
        else:
            response = str(ack['wrong_class'])
            send_message(msisdn, response)
            request.write(response)
            request.finish()
    else:
        response = str(ack['wrong_mix'])
        send_message(msisdn, response)
        request.write(response)
        request.finish()



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

