#!/usr/bin/env python
__author__ = 'andrew_kamau'
__desc__ = '''common functionality used by different app modules'''

from me2u.src.config import EXCEPTIONS
from me2u.src.config import BILL
from utilities.ucip.core import bill_subscriber
from utilities.logging.core import log
from datetime import datetime
import time
from utilities.metrics.core import send_metric
from me2u.src.config import METRICS
#from ussd.metrics.metricHandler import heartBeat

class InvalidHourException(Exception):
    "Invalid Hour For Package Requested"
    pass

class BillingException(Exception):
    '''Exception raised when billing returns unexpected response code'''
    def __init__(self, resp):
        error = EXCEPTIONS['billing_error']
        self.value = '%s -- Response Code: %s' % (error, resp)
    def __str__(self):
        return repr(self.value)

class MissingParameterException(Exception):
    '''Exception raised when a requisite parameters is missing'''
    def __init__(self, missingParameter):
        error = EXCEPTIONS['missingParameter'] % str(missingParameter)
        self.value = error
    def __str__(self):
        return repr(self.value)

class InvalidActionException(Exception):
    '''Exception raised when an undefined action is requested'''
    def __init__(self, action):
        error = EXCEPTIONS['invalid_action'] % action
        self.value = error
    def __str__(self):
        return repr(self.value)


class DataProvisioningRequestException(Exception):
    '''Exception raised when an undefined action is requested'''
    def __init__(self, status):
        error = EXCEPTIONS['data_provisioning']['request'] % status
        self.value = error
    def __str__(self):
        return repr(self.value)


def verify_params(resources, params):
    '''checks to verify that all requisite parameters 
    are bundled in a dict.

    @params: resources dict, params list
    '''
    for param in params:
        try:
            assert resources.has_key(param)
        except AssertionError:
            log(resources, 'operation:verify_params. FAILED', 'error')
            raise MissingParameterException(param)
    log(resources, 'All Parameters verified')


def log(resources, text, debug='info'):
    '''
    logs the text using the logger defined in resources.
    if none defined, prints the results on screen.

    @params: 
        1. resources dict (to check if logger is available)
           instantiated to empty dict if not passed 
        2. text to log
        3. log entry type <info/error> . 
            (default is info)
    '''
    if resources.has_key('logger'):
        logger = resources['logger']
        if debug == 'error':
            err = 'ERROR -- %s' % str(text)
            logger.error(err)
        else:
            info = 'INFO -- %s' % str(text)
            logger.info(info)
    else:
        if debug == 'error':
            err = 'ERROR: %s' % str(text)
            print err
        else:
            info = 'INFO -- %s' % str(text)
            print info

def resolve_da_value(resources, value, target):
    from utilities.common.core import resolve_da_value as resolve
    return resolve(resources, value, target)

def convert_da_time(da_time):
    ''' 
    returns a date time object given a dedicated account time string
    '''
    expiry_date = None
    try:
        fmt = '%Y%m%dT%H:00:00+1200'
        expiry_date = datetime.fromtimestamp(time.mktime\
                (time.strptime(str(da_time),fmt)))
    except Exception, err:
        fmt = '%Y%m%dT%H:00:00+0000'
        expiry_date = datetime.fromtimestamp(time.mktime\
                (time.strptime(str(da_time),fmt)))
    except OverflowError, err:
        expiry_date = datetime(9999, 12, 31, 0, 0)

    return expiry_date


def resolve_expiry(resources, date_one, date_two):
    ''' takes in two datetime objects and returns the 
    larger (later) one
    '''
    dates = [date_one, date_two]
    for date in dates:
        try:
            assert isinstance(date, datetime)
        except AssertionError:
            date_error = 'resolve_expiry failed || date %s not \
                    datetime object' % str(date)
            log(resources, date_error, 'error')
            return

        try:
            assert date_two.year != 9999
        except AssertionError:
            return date_one

    if date_one > date_two:
        return date_one
    else:
        return date_two

def bill(resources):
    ''' 
    generic function that invokes billing in utilities
    and returns resolved response
    '''
    if BILL['toggle'] == 'off':
        return True
    try:
        resp = bill_subscriber(resources)
    except Exception, err:
        bill_error = ''
        log(resources, bill_error, 'error')
        raise err
    else:
        air_resp = str(resp['responseCode'])
        if air_resp == '0':
            return True
        elif air_resp == '124':
            return False
        else:
            raise BillingException(air_resp)

def send_sms(resources, recip):
    '''
    invokes utilities method for sending sms
    sends message to recip <msisdn / recipient>
    '''
    from utilities.common.core import send_message
    from me2u.src.config import MESSAGES
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    amount = parameters['amount']
    recipient = parameters['recipient']
    send_to = parameters[recip]
    status = parameters['status_code']
    if status == '5':
        if recip == 'msisdn':
            msg = MESSAGES[status]
            recipient_no = str(recipient)[-8:] # convert to national format for SMS
            message = msg % (amount, recipient_no)
        elif recip == 'recipient':
            rec_profile = parameters['recipient_profile']['after']
            new_volume = rec_profile['data_balance']
            expiry_date = rec_profile['expiry_date'].strftime('%d-%m-%Y')
            msg = MESSAGES['recipient']['success']
            msisdn_no = str(msisdn)[-9:] # convert to national format for SMS
            message = msg % (amount, msisdn_no, 
                    str(int(float(new_volume))), expiry_date)
    else:
        message = MESSAGES[status]
    start = datetime.now()
    sent = send_message(resources, send_to, message)
    mtrcs = {'name_space':METRICS['sms'],
            'start_time':start}
    send_metric(mtrcs, 'timer')
    del(mtrcs)
    if sent:
        sent_dump = '%s -- %s -- %s' % (send_to, message, sent)
    else:
        sent_dump = 'Message Sending Failed: %s -- %s' % (send_to, message)
    log(resources, sent_dump)

def fetch_package_volumes(resources):
    '''
    go to DB to fetch volumes of pre-configured data bundles
    '''
    verify_params(resources, ['db_connection'])
    from utilities.db.core import execute_query
    from me2u.src.config import SQL
    try:
        start = datetime.now()
        resources = execute_query(resources, SQL['fetch_packages'], 
                [], db_name='db_connection')
    except Exception, err:
        sql_exec_error = 'operation:fetch_package_volumes. Error: %s' % (
                str(err))
        log(resources, sql_exec_error, 'error')
        raise err
    try:
        parameters = resources['parameters']
        cursor = resources['parameters']['cursor']
        volumes = cursor.fetchall()
        cursor.close()
        mtrcs = {'name_space':METRICS['db_select'],
                'start_time':start}
        send_metric(mtrcs, 'timer')
        del(mtrcs)

        parameters['allowed_volumes'] = []
        vol_ind = 0
        while vol_ind < len(volumes):
            parameters['allowed_volumes'].append(volumes[vol_ind][0])
            vol_ind += 1
        resources['parameters'] = parameters
        return resources
    except Exception, err:
        fetch_error = 'operation:fetch_package_volumes. Error: %s' % str(err)
        log(resources, fetch_error, 'error')
        raise err


def log_transaction(resources):
    '''
    logs transaction in DB
    '''
    verify_params(resources, ['db_connection'])
    from utilities.db.core import execute_query
    from me2u.src.config import SQL
    parameters = resources['parameters']
    args = {}
    sql_params = ['msisdn', 'recipient', 'bal_before', 
            'bal_after', 'rec_bal_before', 'rec_bal_after', 
            'rec_expiry', 'status', 'amount', 'created_at']
    args['msisdn'] = parameters['msisdn']
    args['recipient'] = parameters['recipient']
    args['bal_before'] = parameters['sender_profile']['data_balance']
    args['bal_after'] = parameters['sender_profile']['after']['data_balance']
    args['rec_bal_before'] = parameters['recipient_profile']['data_balance']
    args['rec_bal_after'] = parameters['recipient_profile']['after']['data_balance']
    args['rec_expiry'] = parameters['recipient_profile']['after']['expiry_date']
    args['status'] = parameters['status_code']
    args['amount'] = parameters['amount']
    args['created_at'] = datetime.now()

    verify_params(args, sql_params)
    try:
        start = datetime.now()
        resources = execute_query(resources, SQL['log_transaction'], args, db_name='db_connection')
        resources['parameters']['cursor'].connection.commit()
        resources['parameters']['cursor'].close()
        mtrcs = {'name_space':METRICS['db_insert'],
                'start_time':start}
        send_metric(mtrcs, 'timer')
        del(mtrcs)
    except Exception, err:
        db_error = 'operation:log_transaction. execute_query failed with error: %s' % str(err)
        log(resources, db_error, 'error')
        raise err



if __name__ == '__main__':
    #print resolve_date('2013-09-26 05:24:31')
    from datetime import datetime as dt
