
___author__ = "mjanja"

from twisted.web import http
from utilities.sms.core import send_message
from mg_data_interface.src.configs.config import BUNDLES as bundles
from mg_data_interface.src.configs.config import NIGHT_BUNDLES as night_bundles
from mg_data_interface.src.configs.config import B_BUNDLES as b_bundles
from mg_data_interface.src.configs.config import NON_GIFT_VOICE_BUNDLES as non_gift_bundles
from mg_data_interface.src.lib.core import enqueue_provision_request,enqueue_cc_provision_request 
from mg_data_interface.src.lib.core import b_number_is_valid
from mg_data_interface.src.configs.config import ACK as ack
from utilities.metrics.core import count
from mg_data_interface.src.configs.config import HITS as hits
from mg_data_interface.src.configs.config import MEG_KEY
from mg_data_interface.src.configs.config import MY_MEG_10
from aapcn.src.voice.config import voice_bundles_to_be_recorded,retailer_packages_check,weekend_check_packages
from aapcn.src.voice.core import voice_subscription_check,check_is_weekend,voice_is_whitelisted,retailer_fun_cool_whitelisted,retailer_fun_ora_whitelisted,whitelisted_customer_care
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
    print 'PARAMS FROM MENUS: ' + str(params)
    
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

    elif 'ussd_input' in params and '||' in params['ussd_input']:
        input_string = params['ussd_input']
        input_parts = input_string.split('||')
        if len(input_parts) ==2:
            #Normal BPARTY
            inp = input_parts[0]
            params['can_renew'] = '0'
            params['b_msisdn'] = input_parts[1][-9:]
        elif len(input_parts) > 2 and input_parts[1]=='121':
            #Customer Care BPARTY
            inp = input_parts[0]
            params['can_renew'] = '0'
            params['cc_msisdn'] = '261%s' % input_parts[2][-9:]
        #params['b_msisdn'] = '261%s' % input_parts[1][-9:]
        #params['package_id'] = get_package_id(inp, 'b')

    elif 'ussd_input' in params and len(params['ussd_input'].split('*'))>2:
        #to do away with the last #
        input_string = params['ussd_input'].translate(None, '#')
        input_parts = input_string.split('*')

        if len(input_parts) ==3:
            #Normal BPARTY
            params['can_renew'] = '0'
            params['b_msisdn'] = input_parts[2][-9:]
        elif len(input_parts) > 3 and input_parts[2]=='121':
            #Customer Care BPARTY
            params['can_renew'] = '0'
            params['cc_msisdn'] = '261%s' % input_parts[3][-9:]
        #params['package_id'] = get_package_id(inp, 'b')


    print 'PARAMS FROM MENUS ++ : ' + str(params)

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
    packageId = params['package_id']
    if 'cc_msisdn' in params:
        msisdn = params['cc_msisdn']
    else:
        msisdn = params['msisdn']


    if packageId in voice_bundles_to_be_recorded:
        already_subscribed = voice_subscription_check(msisdn,packageId)
        if already_subscribed:
            if packageId == '197':
                params['package_id'] = '199'
                #packageId == '199'
            elif packageId == '222':
                params['package_id'] = '223'
                #packageId == '223'
    elif packageId in weekend_check_packages:
        print 'MSISDN: %s ***********************Checking if its a weekend' %(str(msisdn))
        if packageId == '233' and check_is_weekend(msisdn):
            print 'MSISDN: %s ***********************IS on a weekend' %(str(msisdn))
            params['package_id'] = '232'
            #packageId = '232'
        elif packageId == '253' and check_is_weekend(msisdn):
            print 'MSISDN: %s ***********************IS on a weekend' %(str(msisdn))
            params['package_id'] = '252'
            #packageId = '252'
        else:
            print 'MSISDN: %s ***********************NOT on a weekend' %(str(msisdn))
    
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
                if _pkg == '1' or _pkg == MY_MEG_10:
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
                    if int(package) not in non_gift_bundles:
                        if package in retailer_packages_check:
                            if msisdn[-9:] != bp_msisdn:
                                #resources['parameters']['msisdn'] = benefactor
                                if package == '207' and retailer_fun_cool_whitelisted(msisdn,package):
                                #if package == '207' and voice_is_whitelisted(msisdn,package):
                                    print 'MSISDN: %s ***********Retailer Fun Cool to: %s' %(str(msisdn),str(bp_msisdn))
                                    params['package_id'] = '255'
                                    package = params['package_id']
                                elif package == '220' and retailer_fun_ora_whitelisted(msisdn,package):
                                #elif package == '220' and voice_is_whitelisted(msisdn,package):
                                    print 'MSISDN: %s ***********Retailer Fun ORA to: %s' %(str(msisdn),str(bp_msisdn))
                                    params['package_id'] = '254'
                                    package = params['package_id']
                                #resources['parameters']['msisdn'] = beneficiary

                        try:
                            enqueue_provision_request(package, \
                                    msisdn, bp_msisdn, can_renew, is_web, is_night)
                        except Exception, err:
                            print "error enqueing request for provisioning"
                            raise err
                        else:
                            print "made request for %s buying data for %s" % (msisdn, bp_msisdn)
                    else:
                        response = str(ack['non_gift_bundle'])
                        send_message(msisdn, response)
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

        elif 'cc_msisdn' in params:
            msisdn = params['msisdn']
            package = params['package_id']
            can_renew = params['can_renew']
            cust_msisdn = params['cc_msisdn']

            response = str(ack['txt-1'])
            request.write(response)
            print response
            request.finish()

            if whitelisted_customer_care(msisdn):
                if b_number_is_valid(cust_msisdn):
                    #msisdn = bp_msisdn
                    #print 'Customer Care BPARTY Provisioning'
                    try:
                        enqueue_cc_provision_request(package,
                            msisdn, cust_msisdn, can_renew, is_web, is_night)
                    except Exception, err:
                        print "error enqueing request for provisioning"
                        raise err
                    else:
                        print "made request for %s" % (msisdn)
                else:
                    response = str(ack['wrong_rec'])
                    send_message(msisdn, response)
            else:
                response = str(ack['not_allowed'])
                send_message(msisdn, response)


        else:
            msisdn = params['msisdn']
            package = params['package_id']
            can_renew = params['can_renew']
            
            response = str(ack['txt-1'])
            request.write(response)
            print response
            request.finish()
            
            if _pkg == '1' or _pkg == MY_MEG_10:
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

