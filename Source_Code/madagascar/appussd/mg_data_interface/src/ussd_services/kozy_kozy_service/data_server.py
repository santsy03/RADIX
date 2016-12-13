
___author__ = "mjanja"
import urllib2
from twisted.web import http

from utilities.metrics.core import count
from utilities.ucip.core import get_balance_and_date
from utilities.sms.core  import send_message
from utilities.ucip.airHandler import AIRHandler

import config
from mg_data_interface.src.configs.config import BUNDLES as bundles
from mg_data_interface.src.configs.config import NIGHT_BUNDLES as night_bundles
from mg_data_interface.src.configs.config import B_BUNDLES as b_bundles
from mg_data_interface.src.configs.config import KOZY_PACKAGE_ID
from mg_data_interface.src.lib.core import enqueue_provision_request 
from mg_data_interface.src.lib.core import generate_air_tagging_params 
from mg_data_interface.src.lib.core import b_number_is_valid
from mg_data_interface.src.lib.con import generate_connection
from mg_data_interface.src.configs.config import ACK as ack
from mg_data_interface.src.configs.config import HITS as hits

from ussd.services.common.language.core import getLanguage


def validate_service_class(msisdn):
    '''
    gets the current service class
    '''
    res = {}
    params = {}
    params['msisdn'] = msisdn
    res['parameters'] = params
    res = generate_air_tagging_params(res, 'getserviceclass')

    try:
        resp = get_balance_and_date(res)
    except Exception, err:
        info = "msisdn: %s, op: %s, error %s" % (
                msisdn, 
                "validate service class",
                str(err))
        print info
        return False
    else:
        if resp['responseCode'] == 0:
            sc = resp['serviceClassCurrent']
            if int(sc) in [12,13]:
                return True
            else:
                return False
        else:
            return False


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
        inp_one = input_parts[0]
        params['can_renew'] = '0'
        msisdn = params['msisdn']
        params['b_msisdn'] = str(params['faf'])[-9:]
        params['package_id'] = KOZY_PACKAGE_ID

    print params
    return params

def add_faf(msisdn, faf_number):
    '''
    adds faf_number to FAF list of msisdn

    :param  msisdn     -  owner of list to be updated
    :param  faf_number -  number to be modified

    :return  bool
    '''
    return update_faf_list(msisdn, faf_number, 'ADD')

def delete_faf(msisdn, faf_number):
    '''
    deletes faf_number from FAF list of msisdn

    :param  msisdn     -  owner of list to be updated
    :param  faf_number -  number to be modified

    :return  bool
    '''
    return update_faf_list(msisdn, faf_number, 'DELETE')

def update_faf_list(msisdn, faf_number, action):
    '''
    updates the faf list of msisdn based on the action

    :param  msisdn     -  owner of list to be updated
    :param  faf_number -  number to be modified
    :param  action     -  action to take on the list [ADD/DELETE]

    :return  bool
    '''
    try:
        air = AIRHandler({}, origNodeType='1')
        #faf_num = '261%s' % faf_number[-9:]
        faf_num = '0%s' % faf_number[-9:]
        if action.upper() == 'ADD':
            resp = air.updateFaFList(msisdn, action.upper(), faf_num,
                    config.FAF_INDICATOR, config.SERVICE_NAME, owner='Subscriber')
        else:
            resp = air.updateFaFListWithoutCharge(msisdn, action.upper(), faf_num,
                    config.FAF_INDICATOR, config.SERVICE_NAME, owner='Subscriber')

        if int(resp.get('responseCode')) == 0:
            print '{} - successfully {}ed FAF {}'.format(msisdn, action, faf_number)
            return True
        elif int(resp.get('responseCode')) == 130 and action == 'ADD':
            print '{} - update_faf_list | {} FAF fail | AIR response - {}'.format(
                    msisdn, action, resp)
            return 130
        elif int(resp.get('responseCode')) == 124 and action == 'ADD':
            print '{} - update_faf_list | {} FAF fail | AIR response - {}'.format(
                    msisdn, action, resp)
            return 124
        else:
            print '{} - update_faf_list | {} FAF fail | Unexpected AIR response - {}'.format(
                    msisdn, action, resp)
            return False

    except Exception, err:
        print '{} - update_faf_list() | {} FAF fail - {}'.format(msisdn, action, str(err))
        raise err


def faf_validation(msisdn, faf_number):
    '''
    :return True on success
    '''
    try:
        air = AIRHandler({}, origNodeType='1')
        faf_list = air.getFaFList(msisdn)
        print '{} - FAF list - {}'.format(msisdn, faf_list.get('fafInformationList'))
        if not faf_list.get('fafInformationList'):
            # no faf info
            print '{} - no FAF info'.format(msisdn)
            added = add_faf(msisdn, faf_number)
            if added == True:
                return 0
            elif added == 124:
                print '{} - this is a 124'.format(msisdn)
                return 124
            elif added == 130:
                print '{} - this is a 130'.format(msisdn)
                return 130

        else:
            is_present = False
            fafs = len(faf_list.get('fafInformationList'))
            for each in faf_list.get('fafInformationList'):
                if str(each['fafNumber'])[-9:] == faf_number[-9:] and\
                        int(each['fafIndicator']) == config.FAF_INDICATOR:
                            is_present = True
                            break

            if fafs == config.MAX_FAF_LIST and is_present:
                # 2 FAFs exist and one of them is faf_number
                # delete it then add it...
                deleted = delete_faf(msisdn, faf_number)
                added = add_faf(msisdn, faf_number)
                if deleted == True and added == True:
                    return 0
                elif added == 130:
                    print '{} - this is a 130'.format(msisdn)
                    return 130
                elif added == 124:
                    print '{} - this is a 124'.format(msisdn)
                    return 124
                else:
                    print '{} - either both delete and add failed or one of them'.format(msisdn)
                    return 1

            elif fafs >= config.MAX_FAF_LIST:
                print '{} - {} or more FAFs in list'.format(msisdn, str(config.MAX_FAF_LIST))
                return 2

            elif fafs < config.MAX_FAF_LIST:
                added = add_faf(msisdn, faf_number)
                if added == True:
                    return 0
                elif added == 124:
                    return 124
                elif added == 130:
                    return 130
                else:
                    return 1

            else:
                print '{} - unhandled scenario - {}'.format(msisdn, faf_list)
                if add_faf(msisdn, faf_number):
                    return 0
                else:
                    return 1

    except Exception, err:
        print '{} - faf_validation() fail - {}'.format(msisdn, str(err))
        raise err


def process_provision_request(request):
    '''
    1) provisions a valid request
    2) sends correct messages for invalid responses
    '''

    params = get_params(request)
    if 'input' not in params:
        print '{} - input not in params'.format(params)
        response = 'Incorrect request'
        print response
        request.write(response)
        request.finish()
        return
    else:
        faf_number = '261%s' % str(params['input'])[-9:]
        if faf_number.__contains__('*'):
            response = config.MESSAGES.get('incorrect_format')
            print response
            request.write(response)
            request.finish()
            return

        if len(faf_number) != 12:
            response = config.MESSAGES.get('incorrect_b_number')
            print response
            request.write(response)
            request.finish()
            return


    response = None
    #count(hits % ('ussd'))

    params['faf'] = faf_number
    params = determine_params(params)
    _pkg = params['package_id']

    package, msisdn, b_msisdn, can_renew, is_web = None, None, None, None, None
    is_night = False

    if _pkg:
        if 'b_msisdn' in params:
            package = params['package_id']
            msisdn = params['msisdn']
            can_renew = params['can_renew']
            
            response = str(ack['txt-1'])
            request.write(response)
            print response
            request.finish()

            if validate_service_class(msisdn):

                try:
                    language_url = 'http://127.0.0.1:9062/language?msisdn={}&operation=get'.format(msisdn)

                    faf_val = faf_validation(msisdn, faf_number)
                    print '{} - {} - faf validation result - {}'.format(
                            msisdn, b_msisdn, str(faf_val))
                    if faf_val == 0:
                        enqueue_provision_request(package,
                                msisdn, b_msisdn, can_renew, is_web, is_night)
                        print 'enqueued {} for provisioning of package ID {}'.format(msisdn, package)

                    elif faf_val == 1:
                        response = config.MESSAGES.get('failed')
                        print response
                        request.write(response)
                        request.finish()
                        send_message(msisdn, response)
                        return
                    elif faf_val == 2:
                        try:
                            resp = urllib2.urlopen(language_url)
                            lang = resp.read()
                        except:
                            lang = 'txt-2'
                        print '{} - language {}'.format(msisdn, lang)
                        response = config.MESSAGES.get('max_faf')[lang]
                        print response
                        request.write(response)
                        request.finish()
                        send_message(msisdn, response)
                        return
                    elif faf_val == 130:
                        try:
                            resp = urllib2.urlopen(language_url)
                            lang = resp.read()
                        except:
                            lang = 'txt-2'
                        print '{} - language {}'.format(msisdn, lang)
                        response = config.MESSAGES.get('130')[lang]
                        print response
                        request.write(response)
                        request.finish()
                        send_message(msisdn, response)
                        return
                    elif faf_val == 124:
                        print '{} into 124...'.format(msisdn)
                        try:
                            resp = urllib2.urlopen(language_url)
                            lang = resp.read()
                        except:
                            lang = 'txt-2'
                        print '{} - language {}'.format(msisdn, lang)
                        response = config.MESSAGES.get('124')[lang]
                        print response
                        request.write(response)
                        request.finish()
                        send_message(msisdn, response)
                        return
                    else:
                        response = config.MESSAGES.get('error')
                        print response
                        request.write(response)
                        request.finish()
                        send_message(msisdn, response)
                        return
                        
                except Exception, err:
                    print "error enqueing request for provisioning - %s" % str(err)
                    raise err
            else:
                response = str(ack['postpaid'])
                send_message(msisdn, response)

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
        connections = self.factory.connectionPools
        return connections


class RequestFactory(http.HTTPFactory):
    protocol = RequestProtocol

    def __init__(self):
        '''
        Setup for resources to be used by the service
        '''
        http.HTTPFactory.__init__(self)
        self.connectionPools = generate_connection().get('connections')

