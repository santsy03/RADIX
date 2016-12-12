"""
core data provisioning functions
"""
from mg_data_interface.src.configs.config import ALLOWED_PREFIXES
from mg_data_interface.src.configs.config import PROVISION_URL, BALANCE_URL
from mg_data_interface.src.configs.config import FREQUENCY
from mg_data_interface.src.configs.config import MESSAGES as messages
from mg_data_interface.src.configs.config import SOCIAL as social
from mg_data_interface.src.configs.config import KOZY_PACKAGE_ID as kozy_id
from mg_data_interface.src.configs.config import REGIONAL_ID as reg_id
from mg_data_interface.src.configs.config import SOCIAL_PKGS as social_pkgs
from mg_data_interface.src.configs.config import UNLIMITED_ID
from mg_data_interface.src.configs.config import BONUSMEG250
from mg_data_interface.src.configs.config import BONUSMEG500
from mg_data_interface.src.configs.config import BONUSGIG1
from mg_data_interface.src.configs.config import VALIDITY as validity
from mg_data_interface.src.configs.config import DA_FACTOR
from mg_data_interface.src.configs.config import MSISDN_LENGTH
from mg_data_interface.src.configs.config import SUCCESS_HIT, FAIL_HIT
from mg_data_interface.src.lib.custom_loggers import twistd_logger as log
from mg_data_interface.src.configs.config import ACCOUNT_ID, AUTH_KEY
from mg_data_interface.src.configs.config import ROUTING_KEY
from mg_data_interface.src.configs.config import SERVICE_ID
from mg_data_interface.src.configs.config import NOW_SMS_EVENT_ID
from mg_data_interface.src.configs.config import RENEW_EVENT_ID
from mg_data_interface.src.configs.config import THIRD_DAY_SMS_EVENT_ID
from mg_data_interface.src.configs.config import DAY_OF_RENEWAL_EVENT_ID
from mg_data_interface.src.configs.config import SPECIAL_NUMBERS
from mg_data_interface.src.configs.config import DATA_USAGE
from mg_data_interface.src.configs.config import tempMsgs
from mg_data_interface.src.configs.config import bonusMsgs
from mg_data_interface.src.lib.database_handler import DataCDR
from mg_data_interface.src.lib.con import generate_connection
from utilities.ucip.core import get_balance_and_date
from utilities.metrics.core import count
from utilities.sms.core import send_message
from utilities.common.client import Publisher
from utilities.db.core import get_connection

from ussd.services.common.language.core import getLanguage
from events.core.core import create_event as enqueue_active_events
from events.core.core import dequeue_active_events

from urllib2 import urlopen, Request
from urllib import urlencode
from ast import literal_eval
from datetime import datetime, timedelta

import traceback
import time
import random
import json

res = generate_connection()


def convert_da_time(da_time):
    '''
    returns a date time object given a dedicated account time string
    '''
    da_time = da_time[:19]
    try:
        fmt = '%Y-%m-%dT%H:%M:%S'
        expiry_date = datetime.fromtimestamp(time.mktime( \
                time.strptime(str(da_time),fmt)))
    except OverflowError, e:
        expiry_date = datetime(9999, 12, 31, 0, 0)

    return expiry_date


def generate_air_tagging_params(resources, trans_type):
    '''
    generates a transaction_id for air transactions
    alongside other parameters required to tag transactions
    on air
    '''
    parameters = resources['parameters']
    parameters['externalData1'] = 'broad_band'
    #parameters['externalData1'] = 'data_bundle_renewal'
    parameters['externalData2'] = trans_type

    trans_id = random.randrange(1, 1000000000)
    trans_id = str(trans_id)
    parameters['transactionId'] = trans_id
    resources['parameters'] = parameters
    return resources

def generate_req_id():
    '''
    returns a request id
    '''
    return str(random.randrange(1, 10000000000))


def b_number_is_valid(b_number):
    '''
    validates the b number
    returns true or false
    '''
    resources = {}
    parameters = {}
    resources['parameters'] = parameters
    resources = generate_air_tagging_params(resources, "validate_number")
    resources['parameters']['msisdn'] = '261'+b_number

    try:
        resp = get_balance_and_date(resources)
    except IOError, err:
        log('ERROR', "op|| b_number is valid %s " %(str(err)))
        return False
    except Exception, err:
        log('ERROR', "op|| b_number is valid %s " %(str(err)))
        return False
    else:
        log('INFO', "IN resp code %s" % str(resp['responseCode']))
        if resp['responseCode'] == 0:
            return True
        else:
             return False

def enqueue_provision_request(package, msisdn, b_msisdn, can_renew, is_web, is_night, r_key = ROUTING_KEY):
    '''
    enqueues a provisioning request
    '''
    import traceback
    transaction_type = 'A'
    if package != "stop_auto":
        if b_msisdn == None:
            b_msisdn = msisdn
        else:
            transaction_type = 'B'
            b_msisdn = '261'+b_msisdn
        try:
            parameters = {}
            args = {}
            parameters['msisdn'] = msisdn
            parameters['b_msisdn'] = b_msisdn
            parameters['packageId'] = package
            parameters['authKey'] = AUTH_KEY
            parameters['accountId'] = ACCOUNT_ID
            parameters['transaction_type'] = transaction_type
            parameters['requestId'] = generate_req_id()

            args['routing_key'] = r_key
            args['can_renew'] = can_renew
            if is_night:
                args['is_night'] = "True"
            else:
                args['is_night'] = 'False'

            print str(is_web) + "IS WEB"

            if is_web != None:
                req_id = is_web
                args['web_id'] = req_id

            parameters['args'] = str(args)
            
            params = urlencode(parameters)
            url = PROVISION_URL
            resp = urlopen(Request(url, params))

        except IOError, err:
            error = 'operation: IO enqueue request, desc: \
                    failed to submit provisioning request %s: %s, error:%s'\
                    % (msisdn, package, str(err))
            print error
            print traceback.format_exc()
            raise err
                    
        except Exception, err:
            error = 'operation: n - enqueue request, desc: \
                    failed to submit provisioning request %s: %s, error: %s'\
                    % (msisdn, package, str(err))
            print error
            raise err
        else:
            return (resp.info()).get('Transaction-Id')
    else:
        try:
            resp = disable_renewal(msisdn)
        except Exception, err:
            print traceback.format_exc()
        else:
            return resp


def execute_provision_response(message, logger):
    '''
    determines if a message is aparty or bparty
    '''
    message = literal_eval(message)
    logger.info(message)
    message = json.loads(message)

    transaction_type = message['transaction_type']

    if transaction_type  == 'A' or transaction_type == 'a':
        return process_self(message, logger)
    else:
        return process_b_party(message, logger)

def process_self(message, logger):
    '''
    processes a self data response

    '''
    msisdn = str(message['msisdn']).strip()
    status = int(str(message['status']).strip())
    package_id = str(message['package_id'])

    body = message
    args = message['args']
    can_renew = 0
    is_night = False

    if 'can_renew' in args:
        can_renew = int(args['can_renew'])
        logger.info("renew: %s" % str(args['can_renew']))
    elif 'is_night' in args:
        is_night = str(args['is_night'])


    if package_id == UNLIMITED_ID:
        rsrcs = {}
        rsrcs['msisdn'] = msisdn
        rsrcs['connections'] = res['connections']
        lang = check_language(rsrcs, logger)

    if int(message['package_id']) != 0:
        if status == 5:
            logger.info(message)
            package_name = str(message['name'])
            logger.info('B4 data_usage')
            if package_id in DATA_USAGE:
                queue_msg = '%s| %s| %s' % (msisdn, package_name, package_id)
                rcs = {}
                rcs['parameters'] = {}
                rcs['parameters']['queue_name'] = 'mg_data_usage'
                Publisher(queue_msg, rcs)
            balance = message['balance']

            if 'volume' in balance:
                expiry = str(balance['volume']['expiry'])
                balance = str(balance['volume']['amount'])
            elif 'unlimited' in balance:
                expiry = str(balance['unlimited']['expiry'])
                balance = str(balance['unlimited']['amount'])
            elif 'regional' in balance:
                expiry = str(balance['regional']['expiry'])
                balance = str(balance['regional']['amount'])
                
            balance = int(balance) / DA_FACTOR

            if balance == 0 or balance < 0:
                balance = '1'
            else:
                balance = str(balance)
                
        if status == 5:
            if expiry != 'False' or expiry !='false':
               try:
                   date = expiry.split('T')[0].split('-')
                   expiry_date = date[2]+'-'+date[1]+'-'+date[0]
                   metrics_name = package_name.replace(' ','_')
               except Exception, err:
                   expiry_date = (datetime.now()+timedelta(days=int(validity[package_id]))).replace(hour = 23, minute=59)
               else:
                   expiry_date = (datetime.now()+timedelta(days=int(validity[package_id]))).replace(hour = 23, minute =59)

            try:
                count(SUCCESS_HIT % 'self.'+metrics_name)
            except Exception:
                pass
            #Temporary Messages
            if int(package_id) in tempMsgs:
                message = tempMsgs[int(package_id)]
 
            #End of Temporary Messages 
            #Bonus Messages
            elif package_id == BONUSMEG250:
                message = bonusMsgs['131'][lang]
            elif package_id == BONUSMEG500:
                message = bonusMsgs['132'][lang]
            elif package_id == BONUSGIG1:
                message = bonusMsgs['133'][lang]
            #End of Bonus Messages
            elif is_night == 'True':
                message = messages['success_night'].safe_substitute(
                        expiry = expiry_date, data = package_name)
            elif package_id in social:
                message = messages['social'].safe_substitute(
                        expiry = expiry_date, data = package_name, code =social_pkgs[package_id])
            elif package_id == kozy_id:
                message = messages['kozy']

            elif package_id == reg_id:
                message = messages['regional']

            elif package_id == UNLIMITED_ID:
                message = messages['unlimited_succ'][lang]
            else:
                message = messages['success'].safe_substitute(
                        expiry = expiry_date, data = package_name)

        elif status == 7:
            if package_id == UNLIMITED_ID:
                message = messages['unlimited_unsucc'][lang]
            else:
                message = messages['insufficient_funds']
            count(FAIL_HIT % 'self.nofunds')

        elif status == 6:
            message = messages['conflicting_bundle']
            count(FAIL_HIT % 'self.conflicting')

        elif status == 9:
            message = messages['is_barred']
            count(FAIL_HIT % 'self.isbarred')

        else:
            message = messages['error']
            count(FAIL_HIT % 'self.nofunds')
        logger.info(message)
        send_message(msisdn, message, logger)

        '''
        having sent messages try create events
        '''
        if status == 5:
            if can_renew == 1:
                try:
                    create_events(body, logger)
                except Exception, err:
                    error = "no events created for %s " % msisdn
                    logger.error(error)
                    logger.error(str(traceback.format_exc()))
                else:
                    dump = "events for %s created" % msisdn
                    logger.info(dump)
    else:
        if message['balance']:
            expiry = str(message['balance']['volume']['expiry'])
            balance = str(message['balance']['volume']['amount'])
            balance = int(balance)/ DA_FACTOR
            date = expiry.split('T')[0].split('-')
            expiry_date = date[2]+'-'+date[1]+'-'+date[0]
            message = messages['balance'].safe_substitute(\
                    expiry = expiry_date, data = balance)
        else:
            message = messages['no_balance']

        logger.info(message)
        send_message(msisdn, message, logger)

    if 'web_id' in args:
        '''
        insert request info into table
        '''
        db = DataCDR()
        db.insert_web_response(msisdn, args['web_id'], body, logger)
        
def process_b_party(message, logger):
    '''
    process an a party b party message

    '''
    msisdn = str(message['msisdn']).strip()
    status = int(str(message['status']).strip())
    b_msisdn = str(message['b_msisdn']).strip()
    package_id = str(message['package_id']).strip()

    if status == 5:
        package_name = str(message['name'])
        expiry = str(message['balance']['volume']['expiry'])
        balance = str(message['balance']['volume']['amount'])
        balance = int(balance)/ DA_FACTOR

        if balance == 0 or balance < 0:
            balance = '1'
        else:
            balance = str(balance)

    if status == 5:
        if expiry != 'False':
            date = expiry.split('T')[0].split('-')
            expiry_date = date[2]+'-'+date[1]+'-'+date[0]
            metrics_name = package_name.replace(' ','_')
        else:
            expiry_date = (datetime.now()+timedelta(days=int(validity[package_id]) - 1)).replace(hour = 23, minute =59)

        try:
            count(SUCCESS_HIT % 'b_party.'+metrics_name)
        except Exception:
            pass
        valid = validity[package_id]
        
        #Temporary Messages
        if int(package_id) in tempMsgs:
            response = tempMsgs[int(package_id)].safe_substitute(\
                b_msisdn = b_msisdn, data = package_name, days = valid)
            response_rec = messages['recipient']['success'].safe_substitute(\
                    benefactor = msisdn, data = package_name, balance = balance, expiry = expiry_date)
        #End of Temporary Messages 
        else: 
            response = messages['subscriber']['success'].safe_substitute(\
                    b_msisdn = b_msisdn, data = package_name, days = valid)
            response_rec = messages['recipient']['success'].safe_substitute(\
                    benefactor = msisdn, data = package_name, balance = balance, expiry = expiry_date)

        logger.info(response)
        logger.info(response_rec)

        send_message(msisdn, response, logger)
        send_message(b_msisdn, response_rec, logger)

    elif status == 7:
        response = messages['insufficient_funds']
        logger.info(response)
        count(FAIL_HIT % 'bparty.nofunds')
        send_message(msisdn, response, logger)

    elif status == 6:
        response = messages['conflicting_bundle']
        logger.info(response)
        count(FAIL_HIT % 'bparty.conflicting')
        send_message(msisdn, response, logger)

    elif status == 9:
        response = messages['is_barred']
        logger.info(response)
        count(FAIL_HIT % 'bparty.isbarred')
        send_message(msisdn, response, logger)
    else:
        response = messages['error']
        logger.info(response)
        count(FAIL_HIT % 'bparty.isbarred')
        send_message(msisdn, response, logger)


def check_language(resources, logger):
    msisdn = resources['msisdn']
    try:
        language = getLanguage(resources)
        logger.info('%s-%s' % (msisdn, language))
    except Exception, err:
        error = 'error, failed checking langeage for:%s error: %s' % (msisdn, str(err))
        logger.error(error)
        return 'txt-3'
    else:
        return language

def create_events(message, logger):
    '''
    creates events
    1) creates an sms event
    2) creates a renewal event
    '''
    msisdn = str(message['msisdn']).strip()
    package_id = message['package_id'].strip()
    try:
        expiry = convert_da_time(str(message['balance']['volume']['expiry']))
    except ValueError, err:
        dbg = "no previous offers therefore no expiry for %s" % msisdn
        logger.debug(dbg)
        if int(validity[package_id]) == 1:
            expiry =(datetime.now()).replace(hour = 23, minute =59)
        else:
            expiry =(datetime.now()+timedelta(days=int(validity[package_id]))).replace(hour = 23, minute =59)
    
    freq = 0
    renw = 0

    parameters = {}
    parameters['msisdn'] = msisdn
    parameters['status'] = 0
    parameters['service_id'] = SERVICE_ID
    parameters['can_execute'] = 1
    parameters['parameters'] = '%s,%s,%s' % (str(package_id), str(freq), str(renw))

    try:
        #SMS event
        parameters['event_id'] = NOW_SMS_EVENT_ID
        parameters['execute_at'] = datetime.now() + timedelta(minutes = 1)
        res['parameters'] = parameters
        enqueue_active_events(res)
    except Exception, err:
        error = "failed creating sms event for msisdn || %s " % msisdn
        logger.error(error)

    else:
        dump = "created sms event for msisdn || %s" % msisdn
        logger.info(dump)
        
    try:
        #SMS event# 3rd day before renewal
        parameters['event_id'] = THIRD_DAY_SMS_EVENT_ID
        parameters['execute_at'] =  (expiry + timedelta(days = -3)).replace(hour= 8 )
        if msisdn in SPECIAL_NUMBERS:
            parameters['execute_at'] =  datetime.now() + timedelta(minutes = 1)
        res['parameters'] = parameters
        enqueue_active_events(res)
    except Exception, err:
        error = "failed creating 3rd day from renewal sms event for msisdn || %s " % msisdn
        logger.error(error)

    else:
        dump = "created 3rd day from renewal sms event for msisdn || %s" % msisdn
        logger.info(dump)
        
        
    try:
        #SMS event # day of renewal
        parameters['event_id'] = DAY_OF_RENEWAL_EVENT_ID
        parameters['execute_at'] = (expiry + timedelta(days = -1)).replace(hour= 8 )
        if msisdn in SPECIAL_NUMBERS:
            parameters['execute_at'] =  datetime.now() + timedelta(minutes = 1)
        res['parameters'] = parameters
        enqueue_active_events(res)
    except Exception, err:
        error = "failed creating day of renewal sms event for msisdn || %s " % msisdn
        logger.error(error)

    else:
        dump = "created day of renewal sms event for msisdn || %s" % msisdn
        logger.info(dump)



    try:
        #Renewal event
        parameters['event_id'] = RENEW_EVENT_ID
        # temporary for testing DONT FORGET FI REMOVE
        parameters['execute_at'] = (expiry+ timedelta(days=1)).replace(hour = 0, minute = 2)
        if msisdn in SPECIAL_NUMBERS:
            parameters['execute_at'] =  datetime.now() + timedelta(minutes = 15)
            res['parameters'] = parameters
        enqueue_active_events(res)
    except Exception, e:
        error = "failed creating renewal event for msisdn || %s " % str(parameters)
        logger.error(error)
        logger.error(res)
        logger.error(traceback.format_exc())
    else:
        info = "created renewal event successfully for msisdn || %s " % str(parameters)
        logger.info(info)

def disable_renewal(msisdn):
    '''
    disables renewal
    '''
    parameters = {}
    parameters['service_id'] = SERVICE_ID 
    parameters['msisdn'] = msisdn
    parameters['event_id'] = RENEW_EVENT_ID

    res['parameters'] = parameters
    try:
        resp = check_renew_status(res)
    except Exception, err:
        print traceback.format_exc()
    else:
        if resp:
            if resp[0]:
                try:
                    dequeue_active_events(res)
                except Exception, err:
                    error = "could not disable renewal for %s " % (msisdn)
                    print error
                else:
                    '''
                    send message
                    '''
                    message = messages['renewal_removed']
                    print message
                    send_message(msisdn, message)
                    return ("SUCCESS", resp[1])
            else:
                message = messages['no_renew']
                print message
                send_message(msisdn, message)
                return ("NO_RENEWAL", '0')


        else:
            message = messages['no_renew']
            print message
            send_message(msisdn, message)
            return ("NO_RENEWAL", '0')


def check_renew_status(resources):
    '''
    Function gets the latest event queued for a subscriber.
    The event should still be pending as  per service_id 
    and event_id
    '''
    results = False
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    service_id = parameters['service_id']
    event_id = parameters['event_id']

    sql = 'select * from service_events where msisdn = :msisdn \
            and can_execute = 1 and status = 0 and service_id = \
            :service_id and event_id = :event_id'
    params = {'msisdn':msisdn, 'service_id':service_id, 'event_id':event_id}
    try:
        connection = get_connection(resources)
        cursor = connection.cursor()
        cursor.execute(sql, params)
        records = cursor.fetchall()
        #log(resources, records, 'debug')
        count = cursor.rowcount
        if int(count) == 0:
            results = (False, 0)
        else:
            results = (True, records[0][3])
    except Exception, err:
        error = ' operation check_renew_status failed for %s, error:%s' % (
                msisdn, str(err))
        log(resources, error, 'error')
        #raise err
        return False
    else:
         return results
