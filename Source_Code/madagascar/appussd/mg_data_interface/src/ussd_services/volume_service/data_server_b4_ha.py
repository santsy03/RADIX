
___author__ = "mjanja"

from twisted.web import http
from utilities.sms.core import send_message
from mg_data_interface.src.configs.config import BUNDLES as bundles
from mg_data_interface.src.configs.config import NIGHT_BUNDLES as night_bundles
from mg_data_interface.src.configs.config import B_BUNDLES as b_bundles
from mg_data_interface.src.lib.core import enqueue_provision_request 
from mg_data_interface.src.lib.core import b_number_is_valid
from mg_data_interface.src.configs.config import ACK as ack
from utilities.metrics.core import count
from mg_data_interface.src.configs.config import HITS as hits
from mg_data_interface.src.configs.config import MEG_KEY

def get_params(request):
    ''' 
    retrieves the values of http post or get valuables
    '''
    params = {}
    for key, val in request.args.items():
        params[key] = val[0]
    print params
    return params

def determine_params(params):
    '''
    gets the correct parameters for provisioning
    '''
    if 'input' in params:
        input_string = params['input']
        input_parts = input_string.split('*')
        inp = input_parts[0]

        if len(input_parts) >1:
            inp_one = input_parts[1]


        if 'is_bparty' in params:
            params['can_renew'] = '0'
            params['b_msisdn'] = inp_one[1:]
            params['package_id'] = get_package_id(inp, 'b')

        elif 'disable_renew' in params:
            params['can_renew'] = '0'
            params['action'] = 'stop_auto' 
            params['package_id'] = get_package_id(inp)

        else:
            params['package_id'] = get_package_id(inp)

    print params
    return params

def get_package_id(input_string, r_type = 'a'):
    '''
    given an amount, it returns a possible
    package id
    else returns a False
    '''
    package_id = False
    try:
        if r_type == 'a':
            package_id = bundles[input_string]
        else:
            package_id = b_bundles[input_string]
    except KeyError,err:
        print "no such package configured"
    
    return package_id

def is_night_bundle(package_id):
    '''
    returns a booleean depending on whether 
    a package id is true or false
    '''

    if package_id in night_bundles:
        return True
    else:
        return False

def process_provision_request(request):
    '''
    1) provisions a valid request
    2) sends correct messages for invalid responses
    '''
    params = get_params(request)
    response = None
    #count(hits % ('ussd'))

    params = determine_params(params)
    _pkg = params['package_id']

    package, msisdn, bp_msisdn, can_renew, is_web = None, None, None, None, None

    if _pkg:
        if _pkg == '0':
            params['action'] == 'stop_auto'
        is_night = is_night_bundle(params['package_id'])
        if 'b_msisdn' in params:
            package = params['package_id']
            msisdn = params['msisdn']
            bp_msisdn = params['b_msisdn']
            can_renew = params['can_renew']
            
            response = str(ack['txt-1'])
            request.write(response)
            print response
            request.finish()

            if b_number_is_valid(bp_msisdn):
                try:
                    enqueue_provision_request(package, \
                            msisdn, bp_msisdn, can_renew, is_web, is_night)
                except Exception, err:
                    print "error enqueing request for provisioning"
                    raise err
                else:
                    print "made request for %s buying data for %s" % (msisdn, bp_msisdn)
            else:
                response = str(ack['wrong_rec'])
                send_message(msisdn, response)

        elif 'action' in params:
            package  = params['action']
            msisdn = params['msisdn']

            try: 
                enqueue_provision_request(package, \
                        msisdn, bp_msisdn, can_renew, is_web, is_night)
            except Exception, err:
                print str(err)
                print 'failed making auto renew disable request %s' % msisdn
            else:
                response = str(ack['txt-1'])
                request.write(response)
                print response
                request.finish() 

        else:
            msisdn = params['msisdn']
            package = params['package_id']
            can_renew = params['can_renew']
            
            response = str(ack['txt-1'])
            request.write(response)
            print response
            request.finish()
            
            if _pkg == '1':
                can_renew = '0'
                
                try:
                    enqueue_provision_request(package, 
                            msisdn, bp_msisdn, can_renew, is_web, is_night,  r_key=MEG_KEY)
                
                except Exception, err:
                    print "error enqueing request for provisioning"
                    raise err
                else:
                    print "made request for %s" % (msisdn)
            else:
                try:
                    enqueue_provision_request(package, 
                            msisdn, bp_msisdn, can_renew, is_web, is_night)
                except Exception, err:
                    print "error enqueing request for provisioning"
                    raise err
                else:
                    print "made request for %s" % (msisdn)
    else:
        response = str(ack['wrong'])
        request.write(response)
        print response
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

