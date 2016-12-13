#!/usr/bin/env python
__author__ = 'andrew_kamau'
__desc__ = '''processes responses dequeued from rabbitmq and sends 
              appropriate responses to subscriber'''

from utilities.logging.core import log
from modular_tariffs.src.configs import SQL
from modular_tariffs.src.configs import EVENTS
from modular_tariffs.src.configs import WEB_SERVICES as WS

from utilities.db.core import execute_query
from utilities.common.core import send_message
from utilities.common.core import verify_params
from utilities.common.core import convert_da_time

from modular_tariffs.src.configs import MESSAGES
from modular_tariffs.src.configs import DA_DATA, DA_VOICE, DA_SMS, DA_FUNP
from modular_tariffs.src.configs import stop_actions
from modular_tariffs.src.configs import BALANCE_CATEGORY

from modular_tariffs.src.common import get_time_string
from modular_tariffs.src.common import check_renewals
from modular_tariffs.src.common import create_renewal_notify
from modular_tariffs.src.common import create_renewal_provision

import datetime
from random import randint
from datetime import datetime as dt
from datetime import timedelta as td

def counter(resources):
    ''' counter to determine renewal attempts
    @params: resources
    @return: resources ( updated )

    Things to consider:
        - number of tries . i.e. this is the n'th try
        - day in relation to renewal_days . i.e. this is the n'th day

            parameters['renewal_attempt'] = 'x|y'  
                where x is number of tries on day y   (frequency)
                      y is the day                    (renewal_days)

                upper limit of x is EVENTS['renewal_tries_in_a_day']
                upper limit of y is EVENTS['renewal_days']


        - interval between tries in a day  . i.e. try after x hours
                x = EVENTS['renewal_spacing']

    '''
    parameters = resources['parameters']
    verify_params(parameters, ['frequency','renewal_days'])

    resources['parameters']['re_queue'] = True
    interval = EVENTS['renewal_spacing']
    frequency = parameters['frequency']
    renewal_days = parameters['renewal_days']

    # define upper limits
    upper_frequency = EVENTS['renewal_tries_in_a_day']
    upper_renewal_days = EVENTS['renewal_days']

    try:
        x = int(frequency)
        y = int(renewal_days)
        log(resources, 'BEFORE: freq | ren_days : %d|%d'%(x,y), 'debug')
        upper_x = int(upper_frequency)
        upper_y = int(upper_renewal_days)
        now = dt.now()
        try:
            assert y < upper_y
            #day < max for renewal_days
            if x < upper_x:
                #day < max && frequency < max
                execute_at = now + td(hours = int(interval))
                x += 1
            else:
                #day < max && frequency = max
                execute_at = now + td(days = 1)
                y += 1
        except AssertionError:
            #day = max renewal_days
            if x < upper_x:
                #day = max && frequency < max
                execute_at = now + td(hours = int(interval))
                x += 1
            else:
                #day = max && frequency = max
                log(resources, 
                        ('ID: %s -- %s') % (parameters['modular_id'], parameters['msisdn']) +\
                        ('Maximum renewal attempts reached. Renewal Forfeited'),
                        'info')
                
                execute_at = False
                resources['parameters']['re_queue'] = False
    except Exception, err:
        eval_error = 'operation:counter(). failed to evaluate. %s -- %s -- %s' % (
                parameters['modular_id'], parameters['msisdn'], str(err) )
        log(resources, eval_error, 'error')
        raise err

    log(resources, 'AFTER: freq | ren_days : %d|%d'%(x,y), 'debug')

    parameters['execute_at'] = execute_at
    parameters['frequency'] = str(x)
    parameters['renewal_days'] = str(y)
    resources['parameters'] = parameters
    return resources

def get_renew_time(resources):
    '''returns renew_at time give expiry date
        distributes renewals btn 12 AM and 1 AM
    '''
    try:
        parameters = resources['parameters']
        trans_id = parameters['transactionId']
        try:
            expiry = convert_da_time(parameters['balance']['expiry'], 'string')
        except KeyError:
            # when expiry is in parameters
            expiry = convert_da_time(parameters['expiry'], 'string')
        renew_date = expiry + td(days = 1)
        r = renew_date
        minute = second = randint(10,59)
        renew_at = datetime.datetime(r.year, r.month, r.day, 
                00, minute, second)
        resources['parameters']['renew_at'] = renew_at
        return resources
    except Exception, er:
        log(resources,
                'op:get_renew_time. failed for %s. Error: %s' % (str(trans_id), str(er)),
                'error')
        raise er


def renewal(func):
    '''decorator to create event if response meets required conditions
    '''
    def __inner(resources):
        parameters = resources['parameters']
        renew = parameters['renew']
        status = parameters['status']
        channel = parameters['channel']
        msisdn = parameters['msisdn']
        trans_id = parameters['transactionId']
        modular_id = parameters['modular_id']
        log(resources, 'operation:renewal() %s - Renewal: %s -- Status: %s' % (
            str(modular_id), renew, status), 'debug' )
        if str(renew) == 'True' or channel == WS['renewal_channel']:


            resources['parameters']['service_id'] = EVENTS['service_id']['modular']
            resources['parameters']['can_execute'] = '1'

            prov_execute_at = get_renew_time(resources)['parameters']['renew_at']

            notif_execute_at = prov_execute_at - td(
                    minutes = int(EVENTS['notification']) )

            notif2_execute_at = prov_execute_at - td(
                    minutes = int(EVENTS['notification_two']) )

            if str(status) == '5':

                #create renewal entry for pre-renewal notification
                resources['parameters']['execute_at'] = notif_execute_at
                create_renewal_notify(resources)

                # create second renewal notification event
                resources['parameters']['execute_at'] = notif2_execute_at
                create_renewal_notify(resources, EVENTS['notify_two'])

                #create renewal entry for provisioning
                resources['parameters']['execute_at'] = prov_execute_at
                resources['parameters']['frequency'] = '0'
                resources['parameters']['renewal_days'] = '0'
                create_renewal_provision(resources)

                func(resources)
            else:
                #provisioning was not successful. Try again...

                if channel != WS['renewal_channel']:
                    # first time requests for auto renewal that are not successful
                    # requests that are:
                    #    1. new ( i.e. not from channel 'renewals' )
                    #    2. have renew as True
                    #    3. provisioning is not successful
                    func(resources)
                    return

                counter(resources)
                re_queue = resources['parameters']['re_queue']
                execute_at = resources['parameters']['execute_at']
                if re_queue:
                    log(resources, 
                            '%s -- %s eligible for requeue. Initiating...'%(msisdn, trans_id), 
                            'debug')
                    prov_execute_at = get_renew_time(resources)['parameters']['renew_at']
                    
                    '''  ** commented this out because we don't need notification\
                            events for re-tries. Un-comment if/when required  **

                    notif_execute_at = prov_execute_at - td(
                            minutes = int(EVENTS['notification']))
                    resources['parameters']['execute_at'] = notif_execute_at
                    create_renewal_notify(resources)

                    # add extra renewal notification - 1 day prior to renewal
                    resources['parameters']['execute_at'] = notif2_execute_at
                    create_renewal_notify(resources)
                    '''

                    resources['parameters']['execute_at'] = prov_execute_at
                    create_renewal_provision(resources)

                func(resources)


        else:
            #non-renewal request
            func(resources)

    return __inner

def renewal_check(func):
    '''
    decorator that checks renewal status
    '''
    def __inner(resources):

        check_renewals( resources, service_id = EVENTS['service_id']['modular'], 
                event_id = EVENTS['provision'] )
        func(resources)

    return __inner

@renewal
@renewal_check
def process_provision_response(resources):
    '''formulates and sends responses to subscriber
    '''
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    modular_id = parameters['modular_id']
    renew = parameters['renew']
    status = parameters['status']
    package = parameters['package_requested']
    message = get_message(resources)
    try:
        execute_query(resources, SQL['update_request'], 
                {'status':status, 'modular_id':modular_id},
                db_name='db_connection')
    except Exception, err:
        update_db_error = ('process_provision_response. failed to'+ 
                'update db table. Error: %s' % str(err))
        log(resources, update_db_error, 'error')
        raise err
    else:
        resources['parameters']['cursor'].connection.commit()
        resources['parameters']['cursor'].close()
        del(resources['parameters']['cursor'])

    
    sent = send_message(resources, msisdn, message)
    if sent[0]:
        log(resources, '%s -- %s -- %s -- Renew: %s -- %s -- %s' % (str(modular_id,), 
            str(msisdn), str(status), str(renew), str(message), str(sent[1]) ))

    if parameters['transaction_type'] == 'b':
        if str(status) == '5':
            b_msisdn = parameters['b_msisdn']
            b_message = get_message(resources, 'b')
            b_sent = send_message(resources, b_msisdn, b_message)
            if b_sent[0]:
                log(resources, '%s -- %s -- %s -- %s' % (str(modular_id,), 
                    str(b_msisdn), str(b_message), str(b_sent[1]) ))


def get_message(resources, source = 'a', notif = False):
    '''
    returns response SMS to be sent to subsriber
    '''
    parameters = resources['parameters']

    try:
        status_code = parameters['status']
    except KeyError:
        pass
    try:
        da_id = parameters['da_id']
    except KeyError:
        pass
    try:
        name = parameters['name']
    except KeyError:
        pass
    try:
        package = parameters['package_requested']
    except KeyError:
        package = ''

    msisdn = parameters['msisdn']
    msg_msisdn = '0%s' % str(msisdn)[-9:]
    if notif:
        # renewal notification messages
        package_name = parameters['package_name']
        sms_exec_at = get_time_string( resources, parameters['execute_at'] )

        # + period btn notification and renewal
        exec_at = sms_exec_at + td( minutes = int(EVENTS['notification']) )

        log(resources, 
                'op:mt.src.resp.cons.get_message. renewal notification msg',
                'debug')
        return MESSAGES['default']['renewal_notification'] % ( package_name, exec_at )

    if source == 'b':
        # message to b-party
        return MESSAGES['default']['b_party'] % (name, msg_msisdn)


    if str(package) == '0':
        # balance checks
        resp = str(parameters['response'])
        active_renewals = parameters['renewal_details']
        
        status, expiry, volume, name, transactionId = resp.split('||')
        balance = parameters['balance']
        balance_category = parameters['category']
        da_id = str( BALANCE_CATEGORY[balance_category][0] )
        expiry = balance[ da_id ][ 'expiry' ]
        volume = balance[ da_id ][ 'volume' ]
        if balance_category != 'data' and str(volume) != 'False':
            category_volume = float(volume) * 100
        else:
            category_volume = volume

        if not active_renewals:
            if volume in ('False', '0'):
                #return MESSAGES['default']['payg']['no_renewal']
                return MESSAGES['default']['no_bundle'] % balance_category.upper()
            return MESSAGES[balance_category]['balance'] % (
                    str(category_volume), str(expiry))
        else:
            for ren in active_renewals:
                renewal_bundle = active_renewals[ren]['package_name']
                renewal_date = active_renewals[ren]['executed_at']

            if volume in ('False', '0'):
                return MESSAGES['default']['no_bundle_renewal'] % ( renewal_bundle, renewal_date )

            return MESSAGES[balance_category]['balance_renewal'] % ( 
                    str(category_volume), str(expiry), renewal_bundle, renewal_date )

    if str(package) in stop_actions:
        return MESSAGES['renewals'][status_code]
        
    if da_id in DA_DATA:
        category = 'data'
    elif da_id in DA_VOICE:
        category = 'voice'
    elif da_id in DA_SMS:
        category = 'sms'
    elif da_id in DA_FUNP:
        category = 'funp'
    else:
        error = 'DA %s not categorized' % str(da_id)
        log(resources, error, 'error')
        raise InvalidDa(error)

    try:
        if parameters['transaction_type'] == 'b':
            b_msisdn = '0%s' % str(parameters['b_msisdn'])[-9:]
            if str(status_code) == '5':
                # succesful b-party transaction
                return MESSAGES['default']['a_party'] % (name, b_msisdn)
            else:
                # unsuccesful b-party transaction
                return MESSAGES[category][str(status_code)]

        if parameters['channel'] == WS['renewal_channel'] and str(status_code) == '5':
            # renewal message
            return MESSAGES[category][WS['renewal_channel']]
        else:
            
            # custom messages:
            if parameters['packageId'] == '37' and str(status_code) == '5':
                return MESSAGES['custom_clubsms']
            if parameters['packageId'] == '42' and str(status_code) == '5':
                return MESSAGES['custom_pay']
            if parameters['packageId'] == '43' and str(status_code) == '5':
                return MESSAGES['custom_lib']
            if parameters['packageId'] == '45' and str(status_code) == '5':
                return MESSAGES['custom_f15']
            


            if category == 'voice' and str(status_code) == '5':
                return MESSAGES[category][str(status_code)] % name
            
            return MESSAGES[category][str(status_code)]

    except KeyError, err:
        log(resources, 'get_message. %s' % str(err) )
        return MESSAGES['default'][str(status_code)]

class InvalidDa(Exception):
    "DA provided is not categorized on config"
    pass

if __name__ == '__main__':
    pass
