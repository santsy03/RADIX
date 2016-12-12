from lib_modular.src.common.core import get_subscriber_profile
from lib_modular.src.common.core import get_active_dedicated_accounts
from lib_modular.src.common.core import update_da
from lib_modular.src.common.core import get_da_balance

from utilities.logging.core import log
from utilities.common.core import resolve_da_value

from datetime import datetime as dt
from datetime import timedelta as td

def getBalance(resources):
    '''
    fetches balance of each DA
    '''
    balance = {}
    resources = get_subscriber_profile(resources)
    resources = get_active_dedicated_accounts(resources)
    parameters = resources['parameters']
    trans_id = str(parameters['transactionId'])
    for dedicated_acc in parameters['dedicated_accounts']:
        try:
            balance[dedicated_acc] = get_da_balance(resources, 
                    dedicated_acc)
        except Exception, err:
            error = ('libm.incremental.core.getBalance(). %s - failed ') % str(trans_id) +\
                    ('to build balance dict for DA %s -- Error: %s') % ( dedicated_acc, str(err) )
            log(resources, error, 'error')
            continue

    log(resources, '%s - balance: %s' % (trans_id, balance), 'info')
    parameters['balance'] = balance
    resources['parameters'] = parameters
    return resources

def is_barred(resources):
    '''
    '''
    return False

def checkConflictingBundles(resources):
    '''
    '''
    resources['parameters']['conflictingBundles'] = False
    return resources

def provisionBundle(resources):
    '''
    wrapper for provisioning
    '''
    resources = getBalance(resources)
    parameters = resources['parameters']
    trans_id = parameters['transactionId']
    msisdn = parameters['msisdn']
    da_id = parameters['packageDetails']['da_id']
    da_value = parameters['packageDetails']['da_value']
    bonus = parameters['bonus']
    bonus_volume = bonus['volume']
    bonus_validity = bonus['validity']
    validity = parameters['packageDetails']['dataValidity']
    curr_expiry = parameters['balance'][da_id]['expiry']
    new_exp = dt.now() + td(days=int(validity))
    new_expiry = new_exp - td(days = 1)
    expiry_cdr = '%s - %s - current expiry: %s -- new expiry: %s' % ( 
            str(trans_id), msisdn, str(curr_expiry), str(new_expiry) )
    log(resources, expiry_cdr, 'debug')
    try:
        ##  Always provision the longer validity ##
        if str(curr_expiry) == 'False':
            parameters['expiry_date'] = new_expiry
        else:
            assert new_expiry > curr_expiry
            parameters['expiry_date'] = new_expiry
    except AssertionError:
        parameters['expiry_date'] = curr_expiry

    if (parameters['balance'][da_id]['volume'] == '0' or
            parameters['balance'][da_id]['volume'] == '0.0'):
        # if da balance is 0, date is reset to default.
        # Therefore, assign new expiry date
        parameters['expiry_date'] = new_expiry

    resources['parameters'] = parameters
    update_da(resources)

    if bonus_volume:
        parameters['bonus']['expiry'] = dt.now() + td(
                days = int(bonus_validity))
        resources['parameters'] = parameters
        update_da(resources, 'bonus')

    try:
        ## Over-write balance dict with new balance info ##
        parameters = resources['parameters']
        balance = parameters['balance'][da_id]
        if balance['volume'].isdigit():
            balance['volume'] = int(float(balance['volume'])) + int(float(resolve_da_value(
                resources, str(da_value), 'da_to_mb')))
        else:
            balance['volume'] = int(float(resolve_da_value(resources, str(da_value), 'da_to_mb')))
        balance['expiry'] = parameters['expiry_date']
        balance['package_name'] = parameters['packageDetails']['packageName']
        parameters['balance'] = balance
        resources['parameters'] = parameters
    except Exception, err:
        log(resources, 'incremental.core.provisionBundle. Error: %s'%str(err), 'error')
        raise err
    else:
        return resources

def setup():
    '''
    '''
    pass
