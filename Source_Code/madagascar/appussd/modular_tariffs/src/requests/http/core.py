#!/usr/bin/env python

from cx_Oracle import SessionPool
from configs.config import databases
from utilities.secure.core import decrypt

from utilities.db.core import call_stored_function
from utilities.logging.core import log

from modular_tariffs.src.configs import SQL
from modular_tariffs.src.requests.client import ModularClient as publish_msg
from modular_tariffs.src.configs import balance_actions

def create_request(resources, action):
    ''' insert request into db and publish to queue
    '''
    parameters = resources['parameters']
    transaction_type = parameters['transaction_type']
    msisdn = parameters['msisdn']
    package = parameters['package_id']
    if action in balance_actions:
        category = parameters['category']
    else:
        category = ''
    if transaction_type == 'b':
        msisdn = parameters['b_msisdn']
    renew = str(parameters['renew'])
    channel = str(parameters['channel'])
    try:
        resources = call_stored_function(resources,
                SQL['stored_function'], 'number', 
                [msisdn, package, action, renew, channel],
                db_name='db_connection')
        parameters = resources['parameters']
        parameters['transaction_id'] = str(parameters['stored_func_resp'])
        del(parameters['stored_func_resp'])
        resources['parameters'] = parameters
    except Exception, err:
        error = 'op:mt.req.http.core.create_request. failed for %s. - %s' % (
                msisdn, str(err))
        log(resources, error, 'error')
        raise err
    else:
        request_params = {'msisdn':parameters['msisdn'],
                'package_id':package, 
                'action':action, 
                'category':category,
                'renew':renew,
                'transaction_type':transaction_type,
                'b_msisdn':parameters['b_msisdn'],
                'transaction_id':parameters['transaction_id'],
                'channel':channel}
        
        publish_msg(str(request_params))

def setup():
    resources = {}
    db = databases['core']
    db_user = decrypt(db['username'])
    db_password = decrypt(db['password'])
    db_string = db['string']
    try:
        connection = SessionPool( 
                db_user, db_password, db_string, 5, 200, 5, threaded=True )
        resources['db_connection'] = connection
    except Exception, err:
        ora_error = 'op:mt.req.http.core.setup() - %s' % str(err)
        log(resources, ora_error, 'error')
        raise err
    
    return resources


if __name__ == '__main__':
    pass
