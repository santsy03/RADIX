'''
handles responses.

fetches and sends back to client
'''

from utilities.db.core import execute_query
from utilities.logging.core import log
from modular_tariffs.src.configs import SQL, STATUS, TIMEOUTS
from modular_tariffs.src.configs import WEB_SERVICES

from utilities.memcache.core import MemcacheHandler
from urllib2 import urlopen
from urllib2 import Request

LOC = 'op:mt.requests.http.responses'

def check_cache(func):
    '''decorator that checks for responses in memory'''

    def __inner(resources):

        try:
            parameters = resources['parameters']
            modular_id = parameters['transaction_id']
            cache = MemcacheHandler()
            resources['parameters']['response'] = cache.get( modular_id )

            if not parameters['response']:
                log( resources, 'MEMC: MISS %s' % modular_id )
            else:
                log( resources, 'MEMC: HIT %s - %s' % ( 
                    modular_id, parameters['response']) )
            
        except Exception, err:
            memc_get_err = ('%s.check_cache(). failed to get') % LOC +\
                    ('response from cache for %s - Error %s') % (
                            modular_id, str(err) )
            log( resources, memc_get_err, 'error')
            raise err
        else:

            try:
                func(resources)
            except Exception, err:
                log( resources, 'decorator fail - %s' % str(err), 'error' )
                raise err

    return __inner

def test_check_cache(func):
    '''decorator that checks for responses in memory'''

    def __inner(resources):
        resources['parameters']['response'] = False
        try:
            log(resources, 'resources in decorator - %s'%resources, 'debug')
            func(resources)
        except Exception, err:
            log( resources, 'decorator - %s' % str(err), 'error' )
            raise err

    return __inner

@check_cache
def fetch_provision_response(resources):
    '''
    gets provisioning response from DB
    '''
    try:
        parameters = resources['parameters']
        modular_id = parameters['transaction_id']
        #parameters['response'] = False
        assert parameters['response']
        
        response = parameters['response']
        parameters['response']['transaction_id'] = str(int(float(modular_id)))
        parameters['response']['status-code'] = response['statusCode']
        parameters['response']['status-msg'] = STATUS[str(response['statusCode'])]
        ret_val = parameters['response']

        # always do gabbage collection:
        try:
            resp = MemcacheHandler().delete( modular_id )
            if resp == 0:
                log( resources, 'MEMCACHE DELETE FAILED - %s' % modular_id, 'error' )
        except Exception, err:
            log( resources, 'MEMCACHE DELETE FAILED - %s' % modular_id, 'error' )

    except AssertionError:
        # response not in cache, so fetch it
        try:
            log( resources, 'retrieving response from API for %s..' % (
                modular_id), 'debug' )

            request = 'retrieveRequest?requestId=%s' % str( modular_id )
            resources['parameters']['url_params'] = request
            ret_val = send_request(resources, modular_id)
            resources['parameters']['resp'] = ret_val

        except Exception, err:
            fetch_err = ('%s.fetch_provision_response - failed to fetch') % LOC +\
                    (' response for %s - %s') % ( modular_id, str(err) )
            log( resources, fetch_err, 'error' )
            raise err


    except KeyError:
        modular_id = parameters['transaction_id']
        log( resources, '%s - Key Error: %s' % ( modular_id, str(err) ), 'error' )
        raise err

    except Exception, err:
        modular_id = parameters['transaction_id']
        log( resources, '%s - %s' % (modular_id, str(err) ), 'error' )
        raise err

    else:
        cdr = '%s - response - %s' % ( modular_id, ret_val )
        log( resources, cdr, 'debug' )
        resources['parameters']['resp'] = ret_val

@check_cache
def fetch_stop_response(resources):
    '''
    fetch response for stop renewal requests
    '''
    log(resources, 'resources in fetch_stop_response - %s'%resources, 'debug')
    try:
        parameters = resources['parameters']
        modular_id = parameters['transaction_id']
        #status = False   
        status = parameters['response']
        if status:
            log( resources, '%s - response from cache - %s' % (
                modular_id, status), 'debug' )
            # always do gabbage collection:
            try:
                resp = MemcacheHandler().delete( modular_id )
                if resp == 0:
                    log( resources, 'MEMCACHE DELETE FAILED - %s' % (
                        modular_id), 'error' )
            except Exception, err:
                log( resources, 'MEMCACHE DELETE FAILED - %s' % (
                    modular_id), 'error' )


        else:
            # not in cache
            log( resources, '%s - response not in cache. Going to DB..' % (
                modular_id), 'debug' )
            execute_query( resources, SQL['stop_status'], 
                    {'modular_id':modular_id}, db_name='db_connection' )
            response = resources['parameters']['cursor'].fetchall()
            resources['parameters']['cursor'].close()
            log( resources, '%s - response from DB - %s' % (
                modular_id, response), 'debug' )
            status = response[0][0]

        ret_val = {}
        ret_val['transaction_id'] = str(modular_id)
        ret_val['status-code'] = status
        ret_val['status-msg'] = STATUS[status]
        log(resources, 'ret_val - %s'%ret_val, 'debug')
        resources['parameters']['resp'] = ret_val

    except Exception, err:
        fetch_err = '%s - %s.fetch_stop_response() - %s' % ( 
                modular_id, LOC, str(err) )
        log( resources, fetch_err, 'error')
        raise err


def get_action(resources):
    '''
    goes to DB to check the request type
    to determine which response method to invoke
    '''
    parameters = resources['parameters']
    modular_id = parameters['transaction_id']
    try:
        execute_query( resources, SQL['request_type'],
                {'modular_id':modular_id}, db_name='db_connection' )
        action = resources['parameters']['cursor'].fetchall()
        resources['parameters']['cursor'].close()
        if not action[0][0]:
            # invalid ID
            log( resources, 'invalid transaction_id supplied: %s' %
                    modular_id )
            return False
        else:
            log( resources, 'id: %s - action: %s' % (
                modular_id, action[0][0]), 'info' )
            resources['parameters']['msisdn'] = action[0][1]
            return action[0][0]

    except Exception, err:
        error = '%s - %s.get_action failed - %s' % ( modular_id, LOC, str(err) )
        log( resources, error, 'error' )
        raise err

def send_request(resources, request_id):
    '''sends http request to data provisioning web services
    @param: resources containing url_params key

    @return: response from web services
    '''

    parameters = resources['parameters']
    port = WEB_SERVICES['port']
    account_id = WEB_SERVICES['accountId']
    auth_key = WEB_SERVICES['authKey']
    params = 'accountId=%s&authKey=%s&requestId=%s' % (
            account_id, auth_key, str(request_id) )
    url_params = parameters['url_params'] + '&' + params
    ip_port = '127.0.0.1:%s' % port
    url = 'http://%s/%s' % (ip_port, url_params)
    try:
        #response = urlopen(url, timeout=TIMEOUTS['web_services'])
        response = urlopen(Request(url), timeout=TIMEOUTS['web_services'])
        request_sent = '%s - Request sent to Data Provisioning: %s' % (
                request_id, url )
        log(resources, request_sent, 'debug')
    except Exception, err:
        log(resources, 'op:send_request. Error: %s' % str(err), 'error')
        raise err
    else:
        resp = {}
        resp['status-code'] = (response.info()).get('Status-Code')
        if str( resp['status-code'] ) != '0':
            resp['transaction_id'] = str(int(float((response.info()).get('Request-Id'))))
            resp['status-msg'] = (response.info()).get('Status-Msg')
            resp['category'] = (response.info()).get('Category')
            resp['volume'] = (response.info()).get('Volume')
            resp['expiry'] = (response.info()).get('Expiry')
            resp['name'] = (response.info()).get('Name')
            log( resources, '%s - Response from API - %s' % (
                request_id, resp ), 'debug' )
        else:
            # processing not complete
            log( resources, 'requestId %s - status 0' % parameters['transaction_id'], 'debug' )
            resp['status-msg'] = (response.info()).get('Status-Msg')

        return resp
