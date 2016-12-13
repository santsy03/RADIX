from lib_modular.src.common.core import get_subscriber_profile
from lib_modular.src.common.core import get_active_dedicated_accounts
from lib_modular.src.common.core import get_da_balance
from lib_modular.src.config.core import OFFER_ID

from utilities.logging.core import log
from utilities.ucip.core import set_offer_id

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
    for dedicated_acc in parameters['dedicated_accounts']:
        try:
            balance[dedicated_acc] = get_da_balance(resources, 
                    dedicated_acc)
        except Exception, err:
            error = ('libm.offer.core.getBalance(). failed to build ')+\
                    ('balance dict for DA %s -- Error: %s') % ( dedicated_acc, str(err) )
            log(resources, error, 'error')
            continue

    log(resources, balance, 'debug')
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
    bonus = parameters['bonus']
    bonus_volume = bonus['volume']
    bonus_validity = bonus['validity']
    validity = parameters['packageDetails']['dataValidity']
    new_exp = dt.now() + td(days=int(validity))
    new_expiry = new_exp - td(days = 1)
    log(resources, 'new_expiry: %s' % new_expiry, 'debug')
    parameters['expiry_date'] = new_expiry

    parameters['start_date'] = dt.now()
    parameters['end_date'] = new_expiry
    parameters['offer_id'] = int(OFFER_ID)

    resources['parameters'] = parameters
    try:
        provision = set_offer_id(resources)
    except Exception, err:
        log(resources, 
                'op:libm.offers.core.provisionBundle(). failed to set_offer_id. - %s'%(str(err)), 
                'error')
        raise err
    else:
        if str(provision['responseCode']) == '0':
            log(resources, 
                    '%s - %s - successfully set offer id' % (str(trans_id), msisdn),
                    'info')
        else:
            resp = provision['responseCode']
            log(resources, 
                    '%s - %s - failed to set offers' % (str(trans_id), msisdn, str(resp)),
                    'warning')

    if bonus_volume:
        parameters['bonus']['expiry'] = dt.now() + td(
                days = int(bonus_validity))
        resources['parameters'] = parameters
        update_da(resources, 'bonus')

    try:
        ## Over-write balance dict with new balance info ##
        parameters = resources['parameters']
        #balance = {}
        balance = parameters['balance']
        balance['expiry'] = parameters['expiry_date']
        balance['package_name'] = parameters['packageDetails']['packageName']
        parameters['balance'] = balance
        resources['parameters'] = parameters
    except Exception, err:
        log(resources, 'libm.offers..core.provisionBundle(). Error: %s'%str(err), 'error')
        raise err
    else:
        return resources

def setup():
    '''
    '''
    pass
