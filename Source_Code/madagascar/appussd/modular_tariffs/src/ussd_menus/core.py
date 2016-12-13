#!/usr/bin/env python2.7
# Author : andrew_kamau
import socket
from urllib2 import urlopen, Request
from urllib import  urlencode

from utilities.logging.core import log
from modular_tariffs.src.configs import airtel_prefix
from modular_tariffs.src.configs.packages import PACKAGES
from modular_tariffs.src.configs import accepted_ussd_shortcuts

from modular_tariffs.src.requests.client import ModularClient
from modular_tariffs.src.configs import provision_actions, balance_actions

from modular_tariffs.src.configs import TIMEOUT
from modular_tariffs.src.configs import APPLICATIONS
from modular_tariffs.src.configs import stop_actions
from modular_tariffs.src.configs.packages import BALANCE_PACKAGES

from utilities.secure.core import encrypt

def validate(resources):
    '''validates the USSD shortcut code.
        Adds 'validate' key in parameters
        valid = 0 (valid)
        valid = 1 (invalid)
    '''

    parameters = resources['parameters']
    s_code = parameters['ussd_req'][0]
    opt = parameters['ussd_req'][1]
    b_msisdn = parameters['b_msisdn']
    valid = 0
    try:
        assert opt.isdigit()  # assert validity of option
        assert s_code in PACKAGES  # assert existence of package

        if b_msisdn:
            log( resources, 'b-party request. b_msisdn: %s'%b_msisdn, 'debug' )
            assert len(str(b_msisdn)) > 6
            assert b_msisdn.startswith(airtel_prefix)   # 033XXXXXX
            resources['parameters']['b_msisdn'] = '261%s' % b_msisdn[-9:]
        log(resources, 'Validation Successful', 'debug')
    except AssertionError:
        log(resources, 'Validation failed', 'debug')
        valid = 1
    resources['parameters']['validate'] = valid
    log(resources, 'vaildate - %s'%valid, 'debug')
    return resources

def enqueue_request(resources):
    '''publishes requests to provisioning queue
    @params: resources dict with request parameters
    '''

    msisdn = resources['parameters']['msisdn']
    package_id = resources['parameters']['package_id']
    transaction_type = resources['parameters']['transaction_type']
    b_msisdn = resources['parameters']['b_msisdn']
    renew = resources['parameters']['renew']
    if str(package_id) not in ('0','00','000'):
        action = provision_actions[0]
        balance_category = ''
    else:
        action = balance_actions[0]
        transaction_type = renew = b_msisdn = ''
        balance_category = BALANCE_PACKAGES[ str(package_id) ]

    if str(package_id) in stop_actions:
        # for stop renewal requests
        action = stop_actions[0]
        transaction_type = renew = package_id = b_msisdn = balance_category = ''

    request_params = {'msisdn':msisdn, 
            'package_id':package_id, 
            'action':action, 
            'renew':renew,
            'transaction_type':transaction_type,
            'b_msisdn':b_msisdn,
            'category':balance_category,
            'channel':'modular_tariffs'}

    params = urlencode(request_params)
    log(resources, 'Sending Request Params: %s' % str(request_params), 'debug')
    try:
        application_url = APPLICATIONS['requests'][action]
        url = '%s%s' % (application_url, params)
        log(resources, url, 'debug')
        response = ( urlopen( Request(url, 
            headers= {'auth_key':encrypt('modular_tariffs')})))
        log(resources, 'Web service response - %s' % str(response.read()), 'info')
    except socket.timeout, err:
        time_out = '%s - request timed out' % (url)
        log(resources, time_out, 'error')
        raise err
    except Exception,e:
        enq_error = 'op:mt.ussd.core.enqueue_request. enque_request: Could not enqueue request for :%s, Error:%s' % (
                str(msisdn), str(e))
        log(resources, enq_error, 'error')
        raise e
