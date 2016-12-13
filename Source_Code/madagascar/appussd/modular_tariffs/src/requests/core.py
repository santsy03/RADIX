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
from utilities.logging.core import log
from utilities.db.core import execute_query
from utilities.common.core import send_message
from utilities.common.core import verify_params
from utilities.common.core import verify_params
from utilities.db.core import call_stored_function
from utilities.memcache.core import MemcacheHandler

from modular_tariffs.src.configs import MIX
from modular_tariffs.src.configs import SQL
from modular_tariffs.src.configs import PORTS
from modular_tariffs.src.configs import MESSAGES
from modular_tariffs.src.configs import TIMEOUTS
from modular_tariffs.src.configs import EXCEPTIONS
from modular_tariffs.src.configs import STOP_RENEWAL
from modular_tariffs.src.configs import WEB_SERVICES
from modular_tariffs.src.configs import stop_actions
from modular_tariffs.src.configs import balance_actions
from modular_tariffs.src.configs import provision_actions


from modular_tariffs.src.common import convert_time
from modular_tariffs.src.common import check_renewals
from modular_tariffs.src.common import stop_sub_renewal
from modular_tariffs.src.common import InvalidHourException
from modular_tariffs.src.common import DataProvisioningRequestException

from modular_tariffs.src.requests.utils import get_package_id
from modular_tariffs.src.responses.consumer.core import get_message

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
        memc_get_err = 'memc.get failed for package %s. Reason: %s. Invoking SQL...' % (
                package, str(err))
        log(resources, 'WARNING: %s' % memc_get_err, 'debug')
        
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


def time_check(func):
    '''decorator that performs the following operations:
    1. defines the resources dict
    2. packs the bundle details into resources
    3. checks whether the current time is within the allowed
       time bracket for a particular bundle.
    '''
    def __inner(resources):

        parameters = resources['parameters']
        msisdn = parameters['msisdn']
        action = parameters['action']
        if action in stop_actions:
            # no time check for stopping auto renewal
            func( resources )
            return
        if action not in balance_actions:
            resources = get_package_details(resources)
            package = parameters['package_id']
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
            resources['parameters']['transaction_type'] = 'a'
            resources['parameters']['package_id'] = '0'
            resources['parameters']['renew'] = 'False'
            resources['parameters']['b_msisdn'] = msisdn
            func(resources)

    return __inner


@time_check
def process_request(resources):
    ''' wrapper function that inserts request details into DB, 
    then invokes function
    '''
    parameters = resources['parameters']
    action = parameters['action']
    if action in provision_actions:
        process_provision_request(resources)
    elif action in balance_actions:
        process_balance_request(resources)
    elif action in stop_actions:
        stop_renewal(resources)
        # update db with response
        try:
            parameters = resources['parameters']
            params = { 'status':parameters['status'], 
                    'modular_id':parameters['transaction_id'] }
            execute_query( resources, SQL['update_request'], 
                    params, db_name='db_connection' )
            log( resources, 'db updated - %s ' % str(params), 'debug' )
            parameters = resources['parameters']
            parameters['cursor'].connection.commit()
            parameters['cursor'].close()
            del( parameters['cursor'] )
            log( resources, resources['parameters'] )
        except Exception, err:
            update_error = 'op:process_request for stop auto renew failed\
                    to update db - %s' % ( str(err)  )
            log( resources, update_error, 'error' )
            raise err
        else:
            resources['parameters']['package_requested'] = stop_actions[0]
            message = get_message( resources )
            msisdn = parameters['msisdn']
            sent = send_message(resources, msisdn, message )
            if sent[0]:
                log(resources, '%s -- %s -- %s'% (msisdn, message, str(sent[1]) ))

    else:
        log(resources, 'invalid action: %s' % action, 'error')


def stop_renewal(resources):
    '''
    cancels renewal for msisdn
    '''
    resources['connections'] = resources['db_connection']
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    transaction_id = parameters['transaction_id']
    renew_status = check_renewals(resources)
    cdr = '%s - renew_status: %s' % ( msisdn, renew_status )
    log( resources, cdr, 'info' )
    if renew_status:
        # sub has active renewals pending
        stop_sub_renewal(resources)
        log( resources, '%s - renewal stopped for %s' % ( str(transaction_id), msisdn) )
        parameters['status'] = STOP_RENEWAL['pass']
    else:
        # sub has no active renewals
        log( resources, '%s - no active renewals for %s' % ( str(transaction_id), msisdn) )
        parameters['status'] = STOP_RENEWAL['fail']

    resources['parameters'] = parameters

    # write to cache
    try:
        cache = MemcacheHandler()
        cache_key = str(int(float(transaction_id)))
        cache_val = str( parameters['status'] )
        cache.set( cache_key, cache_val )
        log( resources, 'response to cache - %s-%s' % (
            cache_key, cache_val ), 'debug' )
    except Exception, err:
        cache_err = 'Error writing to cache - %s' % str(err)
        log( resources, cache_err, 'error' )
        pass

@get_package_id
def process_provision_request(resources):
    ''' formulates provision request to send to web services
    '''
    from modular_tariffs.src.configs import WEB_SERVICES
    parameters = resources['parameters']
    verify_params(parameters, 
            ['msisdn', 'package_id', 'action', 'renew', 'channel', 
                'new_package_id'])
    msisdn = parameters['msisdn']
    package = parameters['new_package_id']
    channel = parameters['channel']
    transaction_type = parameters['transaction_type']
    b_msisdn = str(parameters['b_msisdn'])
    transaction_id = parameters['transaction_id']
    if str(package) in MIX:
        resources['parameters']['mix'] = [ True, package ]
        # mix bundle - multiple calls
        for pack in MIX[package]:
            package = str(pack)
            request = 'submitProvision?msisdn=%s&packageId=%s&channel=%s&transaction_type=%s&b_msisdn=%s' % (
                    msisdn, package, channel, transaction_type, b_msisdn)
            resources['parameters']['url_params'] = request
            msg = resources['msg']
            provision_id = send_request(resources)
            summary = '%s - %s - %s || %s || %s || %s' % (
                    transaction_id, msisdn, channel, package, str(provision_id), msg)
            log(resources, summary)


    request = 'submitProvision?msisdn=%s&packageId=%s&channel=%s&transaction_type=%s&b_msisdn=%s' % (
            msisdn, package, channel, transaction_type, b_msisdn)
    resources['parameters']['url_params'] = request
    msg = resources['msg']
    provision_id = send_request(resources)
    summary = '%s - %s - %s || %s || %s || %s' % (
            transaction_id, msisdn, channel, package, str(provision_id), msg)
    log(resources, summary)

def process_balance_request(resources):
    ''' formulates balance check request to 
    send to web services
    '''
    from modular_tariffs.src.configs import WEB_SERVICES
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    package = parameters['package_id']
    channel = parameters['channel']
    transaction_id = parameters['transaction_id']
    request = 'submitBalance?msisdn=%s&packageId=%s&channel=%s' % (
            msisdn, package, channel)
    resources['parameters']['url_params'] = request
    msg = resources['msg']
    provision_id = send_request(resources, 'balance')
    summary = '%s - %s - %s - balance || %s || %s' % (
            transaction_id, msisdn, channel, str(provision_id), msg)
    log(resources, summary)

def send_request(resources, action='provision'):
    '''sends http request to data provisioning web services
    @param: resources containing request key

    @return: response from web services
    '''

    parameters = resources['parameters']
    port = WEB_SERVICES['port']
    account_id = WEB_SERVICES['accountId']
    auth_key = WEB_SERVICES['authKey']
    package = parameters['package_id']
    channel = parameters['channel']
    trans_id = str(int(float(parameters['transaction_id'])))
    renew = parameters['renew']
    transaction_type = parameters['transaction_type']
    b_msisdn = str(parameters['b_msisdn'])
    balance_category = parameters['category']
    if action in provision_actions:
        da_id = parameters['package_attributes']['package_da_id']
    else:
        # balance check has no DA ID
        da_id = 'False'

    mix = [ True, package ] if parameters.has_key('mix') else False

    req_details = '/%s|%s|%s|%s|%s|%s|%s' % (package, trans_id, renew, da_id, 
            channel, balance_category, mix)
    if channel != 'modular_tariffs':
        callback = WEB_SERVICES['requests_callback'] + str(req_details)
    else:
        callback = ''
    params = 'accountId=%s&authKey=%s&requestId=%s&callback=%s&args=%s' % (
            account_id, auth_key, str(trans_id), callback, req_details)
    url_params = parameters['url_params'] + '&' + params
    ip_port = '127.0.0.1:%s' % port
    url = 'http://%s/%s' % (ip_port, url_params)
    try:
        response = urlopen(url, timeout=TIMEOUTS['web_services'])
        request_sent = '%s - Request sent to Data Provisioning: %s' % (
                trans_id, url )
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
