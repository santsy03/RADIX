#!/usr/bin/env python
__author__ = 'andrew_kamau'
__desc__ = '''common functionality used by different app modules'''

from modular_tariffs.src.configs import EVENTS
from modular_tariffs.src.configs import EXCEPTIONS

import datetime as d
from datetime import datetime
from utilities.logging.core import log

from events.core.core import create_event
from events.core.core import check_renew_status
from events.core.core import dequeue_active_events

from ussd.metrics.metricHandler import heartBeat

class InvalidHourException(Exception):
    "Invalid Hour For Package Requested"
    pass

class MissingParameterException(Exception):
    '''Exception raised when a requisite parameters is missing'''
    def __init__(self, missingParameter):
        self.value = 'Expected parameter %r missing' % missingParameter
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

class DataProvisioningResponseException(Exception):
    '''Exception raised when an undefined action is requested'''
    def __init__(self, status):
        error = EXCEPTIONS['data_provisioning']['response'] % status
        self.value = error
    def __str__(self):
        return repr(self.value)

def verify_params(resources, params):
    '''
    PEP8 compliant wrapper
    '''
    return verifyParams(resources, params)

def verifyParams(resources, params):
    '''checks to verify that all requisite parameters 
    are bundled in a dict.

    @params: resources dict, params list
    '''
    for param in params:
        try:
            assert resources.has_key(param)
        except AssertionError:
            log(resources, 'operation:verifyParams. FAILED', 'error')
            raise MissingParameterException(param)
    log(resources, 'All Parameters verified')



def send_metric(metrics, metric_type='timer'):
    '''wrapper function for sending metrics.
    invokes respective metric sending func based on
    type of metric

    @params: metrics dict, and metric_type
    '''
    if metric_type == 'timer':
        period(metrics)
    if metric_type == 'counter':
        beat(metrics)


def beat(metrics):
    '''sends counter metrics

    @param: dict containing name_space key
    '''
    _metric = metrics['name_space']
    hb = heartBeat()
    try:
        hb.beat(_metric)
    except Exception, e:
        err = '[ERROR] Sending beat metric failed', str(e)
        log({}, err, 'error')
    else:
        log({}, 'Metric sent: %s' % _metric )


def period(metrics):
    '''sends timer metrics

    @param: dict containing name_space and 
    start_time keys
    '''
    _metric = metrics['name_space']
    start_time = metrics['start_time']
    hb = heartBeat()
    try:
        hb.period(_metric, start_time)
    except Exception, e:
        err = '[ERROR] Sending period metric failed', str(e)
        log({}, err, 'error')
    else:
        log({}, 'Metric sent: %s' % _metric )

def get_time_string(resources, time_string):
    ''' utility to convert string to datetime obj
    
    string arg format: 'yy-mm-dd hh:mm:ss'
    '''
    try:
        date = time_string.split(' ')[0]
        year, month, day = date.split('-')
        return d.datetime( int(year), int(month), int(day), 0, 0, 0 )
    except Exception, err:
        loc = 'op:mt.src.common.get_time_string()'
        error = '%s - failed to convert string to time - %s' % (
                loc, str(err))
        raise err




def convert_time(resources, time):
    ''' converts 'hh:mm' string to time object

    @params: resources dict and time string in 'hh:mm' format
    @return: time object
    '''
    try:
        assert isinstance(time, str)
        hh, mm = time.split(':')
        time_obj = datetime(99, 12, 12, int(hh), int(mm), 00).time()
    except AssertionError, e:
        log(resources, 'Time format wrong', 'error')
        raise e
    except Exception, err:
        error = 'common.convert_time. failed to convert time: %s. Error: %s' % (
                time, str(err))
        log(resources, error, 'error')

    return time_obj

def create_renewal_notify( resources, event_id = EVENTS['notify'] ):
    '''gathers requisite parameters and creates event for sms notification

    - event_id is an optional argument to allow for creation of multiple
      notification events
    '''
    parameters = resources['parameters']
    modular_id = parameters['modular_id']
    package_id = parameters['package_requested']
    pack = str(parameters['name'])
    msisdn = parameters['msisdn']
    frequency = '0'
    renewal_days = '0'
    parameters['event_id'] = event_id 
    parameters['parameters'] = '%s,%s,%s,%s,%s' % (
            parameters['event_id'], str(package_id), pack, frequency, renewal_days)
    cdr = '%s - creating event for %s -- EV_ID: %s -- SRVC_ID: %s -- EXEC_AT: %s -- CAN_EXECUTE: %s -- PARAMS: %s' % (
            str(modular_id), msisdn, parameters['event_id'], parameters['service_id'], 
            str(parameters['execute_at']), parameters['can_execute'],
            parameters['parameters'] )
    log(resources, cdr)
    resources['parameters'] = parameters
    create_event(resources)

def create_renewal_provision(resources):
    '''gathers requisite parameters and creates event for provisioning
    '''
    parameters = resources['parameters']
    modular_id = parameters['modular_id']
    msisdn = parameters['msisdn']
    package_id = parameters['package_requested']
    pack = str(parameters['name'])
    event_id = EVENTS['provision']
    renewal_days = parameters['renewal_days']
    frequency = parameters['frequency']
    parameters['parameters'] = '%s,%s,%s,%s,%s' % (
            event_id,str(package_id),pack, frequency, renewal_days)
    parameters['event_id'] = EVENTS['provision']
    cdr = '%s - creating event for %s -- EV_ID: %s -- SRVC_ID: %s -- EXEC_AT: %s -- CAN_EXECUTE: %s  -- PARAMS: %s' % (
            str(modular_id), msisdn, parameters['event_id'], parameters['service_id'], 
            str(parameters['execute_at']), parameters['can_execute'], parameters['parameters'] )
    log(resources, cdr)
    resources['parameters'] = parameters
    create_event(resources)


def check_renewals(resources, service_id=None, event_id=None):
    '''
    checks for active events

    @return:
        True  :  when there are pending events
        False :  when there are no pendng events
    '''
    parameters = resources['parameters']
    try:
        check_renew_status(resources, service_id, event_id)
        renewals = resources['parameters']['renewal_details']
        if not renewals:
            # sub has no active renewals
            return False
        else:
            log( resources, 'active renewals - %s' % renewals, 'debug' )
            return True
    except Exception, err:
        loc = 'op:mt.src.common.check_renewals()'
        renewal_check_error = '%s - failed to check renewals for %s - %s' % ( 
                loc, parameters['msisdn'], str(err) )
        log( resources, renewal_check_error, 'error' )
        raise err

def stop_sub_renewal(resources):
    '''
    stops pending events for given sub
    '''
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    try:
        parameters['service_id'] = EVENTS['service_id']['modular']
        for event in ( EVENTS['notify'], EVENTS['provision'] ):
            parameters['event_id'] = event
            resources['parameters'] = parameters
            dequeue_active_events(resources)
            log( resources, 'stopped renewal - %s - event_id: %s'%(msisdn, event), 'debug' )
    except Exception, err:
        loc = 'op:mt.src.common.stop_sub_renewal()'
        stop_renew_err = '%s - failed to stop renewals for %s - %s' % ( 
                loc, parameters['msisdn'], str(err) )
        log( resources, stop_renew_err, 'error' )
        raise err


if __name__ == '__main__':
    #print resolve_date('2013-09-26 05:24:31')
    metrics = {}
    metrics['type'] = 'counter'
    metrics['nameSpace'] = 'test.name.space'
    metrics['startTime'] = datetime.now()
    sendMetric(metrics)
