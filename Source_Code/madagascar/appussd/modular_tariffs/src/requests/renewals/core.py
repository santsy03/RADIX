#!/usr/bin/env python
__author__ = 'andrew_kamau'
__desc__ =   '''processes requests.
                Receives parameters from client apps
                Adds requisite parameters
                and sends http request to web services 
                '''
from datetime import datetime as dt

import random
from urllib2 import urlopen
from modular_tariffs.src.configs import WEB_SERVICES, TIMEOUTS, PORTS
from modular_tariffs.src.common import DataProvisioningRequestException

from utilities.logging.core import log
from utilities.common.core import send_message
from utilities.common.core import verify_params

from utilities.db.core import execute_query
from utilities.common.core import verify_params
from modular_tariffs.src.common import convert_time
from modular_tariffs.src.common import InvalidHourException
from utilities.db.core import call_stored_function
from modular_tariffs.src.configs import provision_actions, balance_actions

from modular_tariffs.src.responses.consumer.core import get_message

from modular_tariffs.src.configs import EVENTS
from modular_tariffs.src.configs import SQL, EXCEPTIONS
from modular_tariffs.src.configs import MESSAGES
from utilities.memcache.core import MemcacheHandler

def get_package_details(resources):
    ''' retrieves package attributes from Memcache ( or DB )
    and adds them to resources dict

    @params: resources dict
    @return: resources - with package_attributes key
    '''

    parameters = resources['parameters']
    package = parameters['package_id']
    memc_key = '%s_package_details' % str(package)
    MEMC = MemcacheHandler()

    try:
        pkg_details = MEMC.get(memc_key)
        p_name, start_time, stop_time = pkg_details.split('|')
        p_start = convert_time(resources, start_time)
        p_stop = convert_time(resources, stop_time)

    except Exception, err:
        # If Memcache fails / misses, log, then go to DB.. #
        memc_get_err = 'ERROR: memc.get failed for package %s. Reason: %s. Invoking SQL...' % (
                package, str(err))
        log(resources, memc_get_err, 'debug')
        
        sql_query = SQL['package_details']
        sql_params = {'package':str(package)}
        resources = execute_query(resources, sql_query, 
                sql_params, db_name='db_connection')
        parameters = resources['parameters']
        cursor = parameters['cursor']
        package_details = cursor.fetchall()
        cursor.connection.commit()
        cursor.close()
        if not package_details:
            log(resources, 
                    'Unable to fetch package_details for package_id %s' % package, 'error')
            parameters['package_attributes'] = 'False'
            return resources

        p_name = package_details[0][0]
        start_time = package_details[0][1]  # hh:mm
        stop_time = package_details[0][2]   # hh:mm
        da_id = package_details[0][3]

        p_start = convert_time(resources, start_time)
        p_stop = convert_time(resources, stop_time)

        
        ###  Persist on memcache ###
        # Format: 
        # 'package_name | start_time | stop_time'
        #
        
        p = package_details
        memc_val = '%s|%s|%s|%s' % (str(p[0][0]), str(p[0][1]), 
                str(p[0][2]), str(p[0][3]) )
        MEMC.set(memc_key, memc_val)

        ###########################



    parameters['package_attributes'] = {}
    parameters['package_attributes']['package_name'] = p_name 
    parameters['package_attributes']['package_start_time'] = p_start 
    parameters['package_attributes']['package_stop_time'] = p_stop
    parameters['package_attributes']['package_da_id'] = da_id
    resources['parameters'] = parameters
    return resources

def event_check(func):
    '''decorator that checks the type of event to process
    '''
    def __inner(resources):

        parameters = resources['parameters']
        verify_params(parameters, 
                ['msisdn', 'package_id', 'action', 'renew', 'channel', 'event_id'])
        package = parameters['package_id']
        msisdn = parameters['msisdn']
        event_id = parameters['event_id']
        if str(event_id).strip() in ( EVENTS['notify'], EVENTS['notify_two'] ):
            # notification
            cdr =  ('op:mt.src.requests.renewals.event_check. ')+\
                    ('notification event. event_id: %s') % str(event_id)
            log(resources, cdr, 'debug')
            log(resources, resources, 'debug')
            del(cdr)

            message = get_message(resources, source = 'a', notif=True)
            sent = send_message(resources, msisdn, message)
            if sent[0]:
                log(resources, ' %s -- %s -- %s' % (
                    str(msisdn), str(message), str(sent[1]) ))
                
        else:
            func(resources)

    return __inner

def time_check(func):
    '''decorator that performs the following operations:
    1. defines the resources dict
    2. packs the bundle details into resources
    3. checks whether the current time is within the allowed
       time bracket for a particular bundle.
    '''
    def __inner(resources):

        resources = get_package_details(resources)
        parameters = resources['parameters']
        verify_params(parameters, 
                ['msisdn', 'package_id', 'action', 'renew', 'channel'])
        package = parameters['package_id']
        msisdn = parameters['msisdn']
        action = parameters['action']
        if action not in balance_actions:
            '''filter out balance checks and do time calculations'''
            time_now = dt.now().time()
            package_attributes = parameters['package_attributes']
            package_name = package_attributes['package_name']
            package_start_time = package_attributes['package_start_time']
            package_stop_time = package_attributes['package_stop_time']
            if time_now >= package_start_time and time_now <= package_stop_time:
                func(resources)
            else:
                time_exception = EXCEPTIONS['invalid_hour'] % (
                        msisdn, package, package_name)
                log(resources, time_exception)
                message = MESSAGES['default']['invalid_hour']
                sent = send_message(resources, msisdn, message)
                if sent[0]:
                    log(resources, '%s -- %s -- %s'% (msisdn, message, str(sent[1]) ))
                raise InvalidHourException(time_exception)
        else:
            func(resources)

    return __inner


@time_check
@event_check
def process_renewal_request(resources):
    ''' wrapper function that inserts request details into DB, 
    then invokes function
    '''
    parameters = resources['parameters']
    transaction_type = parameters['transaction_type']
    msisdn = parameters['msisdn']
    package = parameters['package_id']
    if transaction_type == 'b':
        msisdn = parameters['b_msisdn']
    action = parameters['action']
    renew = str(parameters['renew'])
    channel = str(parameters['channel'])
    resources = call_stored_function(resources, 
            SQL['stored_function'], 'number', 
            [msisdn, package, action, renew, channel],
            db_name='db_connection')
    parameters = resources['parameters']
    parameters['transaction_id'] = str(parameters['stored_func_resp'])
    del(parameters['stored_func_resp'])
    resources['parameters'] = parameters
    log(resources, 
            'Transaction_id: %s' % str(parameters['transaction_id']),
            'debug')
    process_provision_request(resources)


def process_provision_request(resources):
    ''' formulates provision request to send to web services
    '''
    from modular_tariffs.src.configs import WEB_SERVICES
    params = ['msisdn','package_id','frequency','renewal_days']
    verify_params(resources['parameters'], params)
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    package = parameters['package_id']
    channel = parameters['channel']
    transaction_type = parameters['transaction_type']
    b_msisdn = str(parameters['b_msisdn'])
    transaction_id = parameters['transaction_id']
    request = 'submitProvision?msisdn=%s&packageId=%s&channel=%s&transaction_type=%s&b_msisdn=%s' % (
            msisdn, package, channel, transaction_type, b_msisdn)
    resources['parameters']['url_params'] = request
    msg = resources['msg']
    provision_id = send_request(resources)
    summary = '%s - %s \n %s || %s || %s || %s' % (channel, msg, transaction_id, msisdn, package, str(provision_id))
    log(resources, summary)


def send_request(resources):
    '''sends http request to data provisioning web services
    @param: resources containing request key

    @return: response from web services
    '''

    parameters = resources['parameters']
    da_id = parameters['package_attributes']['package_da_id']
    port = WEB_SERVICES['port']
    account_id = WEB_SERVICES['accountId']
    auth_key = WEB_SERVICES['authKey']
    package = parameters['package_id']
    channel = parameters['channel']
    trans_id = str(int(float(parameters['transaction_id'])))
    renew = parameters['renew']
    transaction_type = parameters['transaction_type']
    b_msisdn = str(parameters['b_msisdn'])
    frequency = parameters['frequency']
    renewal_days = parameters['renewal_days']
    req_details = '/%s|%s|%s|%s|%s|%s|%s' % (
            package, trans_id, renew, da_id, channel, frequency, renewal_days)
    callback = WEB_SERVICES['requests_callback'] + str(req_details)
    params = 'accountId=%s&authKey=%s&requestId=%s&callback=%s&args=%s' % (
            account_id, auth_key, str(trans_id), callback, req_details)
    url_params = parameters['url_params'] + '&' + params
    ip_port = '127.0.0.1:%s' % port
    url = 'http://%s/%s' % (ip_port, url_params)
    try:
        response = urlopen(url, timeout=TIMEOUTS['web_services'])
        request_sent = 'Request sent to Data Provisioning: %s' % (
                url )
        log(resources, request_sent, 'debug')
        status = (response.info()).get('Status-Code')
        transaction_id = (response.info()).get('transactionId')
    except Exception, err:
        log(resources, 'operation:send_request. Error: %s' % str(err), 'error')
        raise err
    else:
        if str(status) == '0':
            return transaction_id
        else:
            log(resources, 'Data Provisionning Response for %s: %s' % (str(transaction_id), status))
            raise DataProvisioningRequestException(status)

if __name__ == '__main__':
    pass
