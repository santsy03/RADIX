#!/usr/bin/env python
from utilities.logging.core import log

class TimeoutException(Exception):
    """
    handles timeout exceptions
    """
    pass


def invoke_cmb(resources):
    ''' encodes params and invokes CMB service via http

    @params: dict containing url parameters
    @return: response from CMB service
    '''
    from direct_cmb_mg.src.config import CMB, TIMEOUT
    from direct_cmb_mg.src.metrics.config import USSD_CMB_SERVICE_TEMPLATE
    from direct_cmb_mg.src.metrics.sendmetric import send_metric
    from datetime import datetime
    from urllib import urlencode 
    from urllib2 import urlopen
    import socket
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    b_number = parameters['b_number']
    language = parameters['language']
    session = parameters['sessionId']
    action = CMB['action']
    url = CMB['url']
    args = urlencode({'msisdn':msisdn, 'recipient':b_number, 
        'language':language, 'action':action, 'sessionId':session})
    try:
        params = url % str(args)
        print '[DEBUG]: URL Invoked: %s' % params
        start_time = datetime.now()
        resources['start'] = start_time
        response = urlopen(params, timeout = TIMEOUT['cmb']) # 5 second timeout
    except socket.timeout, err:
        timeout_error = 'ERROR: Connection to %s timed out:  %r' % (params, err)
        log ( resources, error)
        raise TimeoutException(timeout_error)
    except Exception, err:
        error = ("operation invoke_cmb Desc: Failed to invoke CMB for") + (
                " msisdn: %s, Error: %s") % (str(msisdn), str(err))
        log ( resources, error)
        raise  err
    else:
        resources['type'] = 'timer'
        resources['nameSpace'] = USSD_CMB_SERVICE_TEMPLATE
        send_metric ( resources )
        return response.read()
