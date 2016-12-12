'''
utility functions used across various applications
'''

import time
import urllib
from utilities.db.core import execute_query
from utilities.logging.core import log
from datetime import datetime, timedelta, tzinfo
from urllib import urlopen, urlencode
from configs.config import kannel
from utilities.secure.core import decrypt
from lib_modular.src.config.core import AIR

DEFAULT_MSG_SENDER = 'Airtel'

EXCEPTIONS = {}
EXCEPTIONS['billing_error'] = 'Failed to bill on AIR.'
EXCEPTIONS['missingParameter'] = 'Parameter Missing: %s'
EXCEPTIONS['invalid_action'] = 'Invalid Action Invoked: %s'

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


def get_configuration(resources):
    '''
    retrieves the configuration for the given service and package_id
    '''
    parameters = resources['parameters']
    service_id = parameters['service_id']
    package_id = parameters['package_id']

    sql = ('select name,parameters,price from service_packages where '+
            'service_id = :service_id and id = :package_id and status = 1')

    params = {'service_id': int(service_id), 'package_id': int(package_id)}
    resources = execute_query(resources, sql, params)
    parameters = resources['parameters']
    cursor = parameters['cursor']
    result = cursor.fetchone()
    count = cursor.rowcount
    try:
        del(parameters['cursor'])
        cursor.close()
    except Exception, err:
        pass
    if count == 0:
        parameters['configuration'] = False
    else:
        configuration = {}
        configuration['package_name'] = result[0]
        configuration['price'] = result[2]
        configuration['params'] = result[1]
        parameters['configuration'] = configuration
    resources['parameters'] = parameters
    return resources

def create_billing_cdr(resources):
    '''
    creates a record in the billings record for the given subscription
    '''
    sql = 'insert into service_cdrs(msisdn, service_id, package_id,created_at,channel) values(:msisdn, :service_id, :package_id, :created_at, :channel)'
    parameters = resources['parameters']
    params = {}
    params['msisdn'] = parameters['msisdn']
    params['service_id'] = parameters['service_id']
    params['package_id'] = parameters['package_id']
    params['created_at'] = datetime.now()
    params['channel'] = parameters['channel']
    resources = execute_query(resources, sql, params)
    parameters = resources['parameters']
    cursor = parameters['cursor']
    cursor.connection.commit()
    try:
        del(parameters['cursor'])
        cursor.close()
    except Exception, err:
        pass


def resolve_da_value(resources, value, target):
    ''' converts DA value to MB and vice versa
    @params: 
        1. value : the value to convert
        2. target - <da_to_mb / mb_to_da> : conversion direction 

    @return: <da_value / mb_value>
    '''
    from me2u.src.config import AIR
    factor = int(AIR['dedicated_account_factor'])
    if target == 'da_to_mb':
        kb_value = float(value) / factor
        mb_value = kb_value / 1024
        #log(resources, 'DA Value: %s -- MB Value: %s' % (str(value), str(mb_value)))
        return str(mb_value)
    elif target == 'mb_to_da':
        kb_value = int(value) * 1024
        da_value = kb_value * factor
        #log(resources, 'MB Value: %s -- DA Value: %s' % (str(value), str(int(da_value))))
        return str(int(da_value))



def convert_da_time(da_time, opt='string'):
    ''' 
    returns a date time object given a dedicated account time string
    '''
    expiry_date = None
    try:
        fmt = '%Y%m%dT%H:00:00+1200'
        if opt == 'string':
            fmt = '%Y-%m-%dT%H:%M:%S'
            da_time = str(da_time).split('.')[0]
        expiry_date = datetime.fromtimestamp(time.mktime\
                (time.strptime(str(da_time),fmt)))
    except ValueError:
        fmt = '%Y%m%dT%H:00:00+0000'
        expiry_date = datetime.fromtimestamp(time.mktime\
                (time.strptime(str(da_time),fmt)))
    except OverflowError:
        expiry_date = datetime(9999, 12, 31, 0, 0)
    except Exception, err:
        log({}, 'utilities.convert_da_time. failed to convert time format.\
                Error: %s' % str(err), 
                'error')
        raise err

    return expiry_date


def get_date_from_timestamp(timestamp):
    '''
    creates a datetime object from an e/// timestamp
    '''
    return convert_da_time(timestamp)


def verify_params(res, params, logger=None):
    ''' pep 8 compatible wrapper to verifyParams'''
    verifyParams(res, params, logger)

def verifyParams(res, params, logger=None):
    '''checks to verify that all requisite parameters 
    are bundled in a dict.

    @params: resources dict, params list, optional logger obj

    - If logger arg is nog supplied, we will look for logger in res dict.
      If it isn't in res either, then output will be printed on screen
    '''
    if logger:
        logger = {'logger':logger}
    else:
        if res.has_key('logger'):
            logger = {'logger':res['logger']}
        else:
            logger = {}

    try:
        assert isinstance(params, list)
    except AssertionError:
        log(logger, ' utilities.common.core.verifyParams. \
                Cannot evaluate. params is not a list', 'error')
        raise
    for param in params:
        try:
            assert res.has_key(param)
        except AssertionError:
            log(logger, 'operation:verifyParams. FAILED', 'error')
            raise MissingParameterException(param)
    log(logger, 'All Parameters verified', 'debug')

def send_message(resources, msisdn, message, sender=DEFAULT_MSG_SENDER):
    '''
    send message to msisdn
    '''
    message = str(message)
    user_name = decrypt(str(kannel['username']))
    password = decrypt(str(kannel['password']))
    args = urlencode({'username':user_name,'password':password,
        'to':str(msisdn),'from':sender,'text':message,})#'charset':'utf-8','coding':'2'})
    try:
        url = 'http://127.0.0.1:14020/cgi-bin/sendsms?%s' %  str(args)
        resp = urlopen(url).read()
    except Exception,e:
        raise e
        log(resources, "could not send message: %s for this sub %s" %  (str(e), str(msisdn)), 'error')
    else:
        return [True, resp]

class GMT330( tzinfo ):
        '''
         Africa/Nairobi
        '''
        def utcoffset( self, dt ):
                return timedelta( hours=+2, minutes=+00 )

        def tzname( self ):
                return "GMT +03:00"

        def dst( self, dt ):
                return timedelta( 0 )

        def __repr__( self ):
                return self.tzname()

