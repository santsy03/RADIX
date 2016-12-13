
'''
core renewal functions

'''

from mg_auto_renewal.src.configs.config import PROVISION_URL
from mg_auto_renewal.src.configs.config import MESSAGES as messages
from mg_auto_renewal.src.configs.config import PACKAGES as packages
from mg_auto_renewal.src.configs.config import VALIDITY as validity
from mg_auto_renewal.src.configs.config import DA_FACTOR
from mg_auto_renewal.src.configs.config import SUCCESS_HIT, FAIL_HIT
from mg_auto_renewal.src.configs.config import ACCOUNT_ID, AUTH_KEY
from mg_auto_renewal.src.configs.config import ROUTING_KEY
from mg_auto_renewal.src.configs.config import RENEWAL_TRIES
from mg_auto_renewal.src.configs.config import FREQUENCY_TRIES
from mg_auto_renewal.src.configs.config import NOW_SMS_EVENT_ID
from mg_auto_renewal.src.configs.config import THIRD_DAY_SMS_EVENT_ID
from mg_auto_renewal.src.configs.config import DAY_OF_RENEWAL_EVENT_ID
from mg_auto_renewal.src.configs.config import RENEW_EVENT_ID
from mg_auto_renewal.src.configs.config import POSTPONED_SMS_EVENT_ID
from mg_auto_renewal.src.configs.config import SPECIAL_NUMBERS

from mg_auto_renewal.src.lib.con import generate_connection
from events.core.core import create_event as enqueue_active_events
from utilities.metrics.core import count
from utilities.sms.core import send_message
from urllib2 import urlopen, Request
from urllib import urlencode
from ast import literal_eval
from datetime import datetime, timedelta

import time
import random
import json
import traceback
import socket


res = generate_connection()



def generate_air_tagging_params(resources, trans_type):
    '''
    generates a transaction_id for air transactions
    alongside other parameters required to tag transactions
    on air
    '''
    parameters = resources['parameters']
    parameters['externalData1'] = 'data_bundle_renewal'
    parameters['externalData2'] = trans_type

    trans_id = random.randrange(1, 1000000000)
    trans_id = str(trans_id)
    parameters['transactionId'] = trans_id
    resources['parameters'] = parameters
    return resources

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


def generate_req_id():
    '''
    returns a request id
    '''
    return str(random.randrange(1, 10000000000))


def determine_date(parameters, logger):
    '''
    determines date to relay to user based on 
    package_id and event_id
    '''
    days_no = int(validity[package_id])



def process_provision_request(parameters, logger):
    '''
    enqueues a provisioning request
    '''
    try:

        transaction_type = 'A'
        event_id = str(parameters['event_id']).strip()
        msisdn = parameters['msisdn']
        package_id = parameters['packageId']
        
        frequency = parameters['frequency']
        renewal_days = parameters['renewal_days']
        logger.info(str(parameters))
        logger.info("event id %s" % str(event_id))

        if int(event_id) == NOW_SMS_EVENT_ID:
            message = messages['will_renew']
            package = packages[package_id]
            days_no = int(validity[package_id])
            expiry  = (datetime.now() + timedelta(days = days_no)).strftime('%d-%m-%y')
            message = message.safe_substitute(package = package, expiry = expiry)
            send_message(msisdn, message)
            logger.info(message)
            logger.info("message sent to %s" % (str(msisdn)))
            
            
        elif int(event_id) == THIRD_DAY_SMS_EVENT_ID:
            #third day before message
            message = messages['will_renew']
            package = packages[package_id]
            days_no = int(validity[package_id])
            if days_no < 3:
                if days_no == 2:
                     expiry  = (datetime.now() + timedelta(days = 2)).strftime('%d-%m-%y')
                elif days_no == 1:
                     expiry  = (datetime.now() + timedelta(days = 1)).strftime('%d-%m-%y')
            else:
                expiry  = (datetime.now() + timedelta(days = 3)).strftime('%d-%m-%y')
            message = message.safe_substitute(package = package, expiry = expiry)
            send_message(msisdn, message)
            logger.info(message)
            logger.info("message sent to %s" % (str(msisdn)))
            
            
        elif int(event_id) == DAY_OF_RENEWAL_EVENT_ID:
            #auto renewal day message
            message = messages['will_renew_today']
            package = packages[package_id]
            message = message.safe_substitute(package = package)
            send_message(msisdn, message)
            logger.info(message)
            logger.info("message sent to %s" % (str(msisdn)))


        elif int(event_id) == POSTPONED_SMS_EVENT_ID:

            data = packages[package_id]
            days = validity[package_id]
            message = messages['renewal_success'].safe_substitute(\
                    days = days, data = data)
            send_message(msisdn, message)
            logger.info(message)
            logger.info("message sent to %s" % (str(msisdn)))

        elif int(event_id) == RENEW_EVENT_ID:
            try:
                params = {}
                params['msisdn'] = msisdn
                params['b_msisdn'] = msisdn
                params['packageId'] = package_id
                params['authKey'] = AUTH_KEY
                params['accountId'] = ACCOUNT_ID
                params['transaction_type'] = transaction_type
                params['requestId'] = generate_req_id()
                params['channel'] = 'renew'

                args = {}
                args['routing_key'] = ROUTING_KEY
                args['is_renew'] = "True"
                args['renewal_days'] = renewal_days
                args['frequency'] = frequency

                params['args'] = str(args)
                logger.info("params before making dp call")
                logger.info(str(params))
                
                params = urlencode(params)
                url = PROVISION_URL
                resp = urlopen(Request(url, params), timeout = 3)

            except IOError, err:
                error = 'operation: IO enqueue request, desc: failed to submit \
                        provisioning request %s: %s, error:%s'% (msisdn, package_id, str(err))
                logger.error(error)
                raise err

            except socket.timeout as e:
                logger.error ("TIMEOUT ERROR %s" % (str(e)))

            except Exception, err:
                error = 'operation: n - enqueue request, desc: failed to submit \
                        provisioning request %s: %s, error: %s'% (msisdn, package_id, str(err))
                logger.error(error)
                raise err
            else:
                logger.info(resp.read())
    except Exception, err:
        logger.error(traceback.format_exc())
        logger.error(str(err))



def process_renewal_response(message, logger):
    message = literal_eval(message)
    logger.info(message)
    message = json.loads(message)
    msisdn = str(message['msisdn']).strip()
    status = int(str(message['status']).strip())
    package_id = str(message['package_id'])
    
    body = message
    
    if status == 5:
        logger.info(message)
        package_name = str(message['name'])
        expiry = str(message['balance']['volume']['expiry'])
        balance = str(message['balance']['volume']['amount'])
        balance = int(balance)/ DA_FACTOR

        if status == 5:
            if expiry != 'False':
                date = expiry.split('T')[0].split('-')
                expiry_date = date[2]+'-'+date[1]+'-'+date[0]
                metrics_name = package_name.replace(' ','_')
            else:
                expiry_date = (datetime.now()+timedelta(days=int(validity[package_id]))).replace(hour = 23, minute =59)
        try:
            count(SUCCESS_HIT % metrics_name)
        except Exception:
            pass

        valid = validity[package_id]
        message = messages['renewal_success'].safe_substitute(\
                days = valid, data = package_name)

        curr_time = datetime.now()

        if curr_time.hour in range(8, 21):
            send_message(msisdn, message)
            logger.info(message)
        else:
            logger.info("current time not between 8am and 8pm %s" % str(curr_time))

            parameters = {}
            parameters['msisdn'] = msisdn
            parameters['status'] = 0
            parameters['service_id'] = 2
            parameters['can_execute'] = 1
            parameters['parameters'] = '%s,%s,%s' % (str(package_id), str(0), str(0))
            
            try:
                #SMS event
                parameters['event_id'] = 3
                if curr_time.hour <= 8:
                    #its between midnight and eight set to execute at 8
                    logger.debug("its between midnight and 8:AM set to execute at 8")
                    execute_at = datetime.now().replace(hour = 8, minute =0, second =0)

                elif curr_time.hour >= 20:
                    #its past 8PM set to execute tommorrow at 8 AM
                    logger.debug("its past 8PM set to execute tommorrow at 8 AM")
                    execute_at = datetime.now() + timedelta(days = 1)
                    execute_at = execute_at.replace(hour = 8, minute =0, second =0)

                parameters['execute_at'] = execute_at

                res['parameters'] = parameters
                enqueue_active_events(res)
            except Exception, err:
                error = "failed creating sms event for msisdn || %s " % msisdn
                logger.error(error)
            else:
                dump = "created 8:00 AM notification sms event for msisdn || %s" % msisdn
                logger.info(dump)
    else:
        package_name = str(message['name'])
        count(FAIL_HIT % package_name + "."+ str(status))

    try:
        schedule_event(body, status, logger)
    except Exception, error:
        logger.error("error rescheduling events %s" % error)
        logger.error(traceback.format_exc())


def count_frequency(status, frequency, renewal_days):
    '''
    1) if status == 5: frequency =0, renewal_days =0
    2) if status !=5:
        if frequency < renewal_tries :
           frequency +=1
        elif frequency == renewal_tries:
            frequency == false
        if renewal_days == renewal_tries:
            renewal_days == false
        if frequency == False:
           renewal_days +=1
    '''
    if status == 5:
        frequency = 0
        renewal_days = 0

        return (frequency, renewal_days)
    else:
        if frequency < FREQUENCY_TRIES:
            frequency += 1

        elif frequency == FREQUENCY_TRIES:
            frequency = "exhausted"

        if renewal_days == RENEWAL_TRIES:
            renewal_days = "exhausted"

        if frequency == "exhausted":
            renewal_days += 1 

    return(frequency, renewal_days)


def schedule_event(message, status, logger):
    '''
    1) schedules an event (if need be) with the correct parameters
    2) Reports on the situation
    '''

    msisdn = str(message['msisdn']).strip()
    package_id = message['package_id'].strip()
    status = int(message['status'])
    
    try:
        expiry = convert_da_time(str(message['balance']['volume']['expiry']))
    except ValueError, err:
        dbg = "no previous offers therefore no expiry for %s" % msisdn
        logger.debug(dbg)
        if int(validity[package_id]) == 1:
            expiry =(datetime.now()).replace(hour = 23, minute =59)
        else:
            expiry =(datetime.now()+timedelta(days=int(validity[package_id]))).replace(hour = 23, minute =59)
 
    args = message['args']
    freq = int(args['frequency'])
    renw = int(args['renewal_days'])
    logger.info("%s||%s frequency renewal before" % (freq, renw))
    frequency, renewal_days = count_frequency(status, freq, renw)
    logger.info("%s||%s frequency renewal after" % (frequency, renewal_days))

    if status == 5:
        parameters = {}
        parameters['msisdn'] = msisdn
        parameters['status'] = 0
        parameters['service_id'] = 2
        parameters['can_execute'] = 1
        parameters['parameters'] = '%s,%s,%s' % (str(package_id), \
                str(frequency), str(renewal_days))
        parameters['event_id'] = 2
        if msisdn in SPECIAL_NUMBERS:
            parameters['execute_at'] =  datetime.now() + timedelta(minutes =15)
        else:
            parameters['execute_at'] = (expiry+ timedelta(days=1)).replace(hour = 0, minute = 2)
        res['parameters'] = parameters

        try:
            enqueue_active_events(res)
        except Exception, e:
            error = "failed creating renewal event for msisdn || %s " % str(parameters)
            logger.error(error)
            logger.error(traceback.format_exc())
        else:
            info = "created renewal event successfully for msisdn || %s " % str(parameters)
            logger.info(info)             
            create_sms_events(parameters, logger)
    else:
        if renewal_days != 'exhausted':
            if frequency == "exhausted":
                frequency = 0

            parameters = {}
            parameters['msisdn'] = msisdn
            parameters['status'] = 0
            parameters['service_id'] = 2
            parameters['can_execute'] = 1
            parameters['parameters'] = '%s,%s,%s' % (str(package_id), \
                    str(frequency), str(renewal_days))
            parameters['event_id'] = 2
            if frequency == 0:
                #means we have exhausted the tries today we queue for tommorrow
                parameters['execute_at'] = datetime.now() + timedelta(days = 1)
                logger.info("%s has reached maximum retries a day." % msisdn)
                message = messages['no_renew_funds']
                send_message(msisdn, message)
            else:
                #we havent exhausted, try after two hours
                parameters['execute_at'] = datetime.now() + timedelta(hours = 2)
                #parameters['execute_at'] = datetime.now() + timedelta(minutes = 2)
                dump = "%s has tried %s times today. will retry again in two hours"\
                        % (msisdn, str(frequency))
                logger.info(dump)

            res['parameters'] = parameters

            try:
                enqueue_active_events(res)
            except Exception, e:
                error = "failed creating renewal event for msisdn || %s " % str(parameters)
                logger.error(error)
                logger.error(traceback.format_exc())
            else:
                info = "created renewal event successfully for msisdn || %s " % str(parameters)
                logger.info(info)
        else:
            dump = "%s has been retried three times per day for 3 days. Giving up" % (msisdn)
            logger.info(dump)
            message = messages['no_renew_funds']
            send_message(msisdn, message)


def create_sms_events(parameters, logger):
    '''
    creates sms events
    '''
    expiry = parameters['execute_at']
    msisdn = parameters['msisdn']

    try:
        #SMS event
        parameters['event_id'] = NOW_SMS_EVENT_ID
        parameters['execute_at'] = expiry + timedelta(minutes = 1)
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
        res['parameters'] = parameters
        enqueue_active_events(res)
    except Exception, err:
        error = "failed creating day of renewal sms event for msisdn || %s " % msisdn
        logger.error(error)

    else:
        dump = "created day of renewal sms event for msisdn || %s" % msisdn
        logger.info(dump)

