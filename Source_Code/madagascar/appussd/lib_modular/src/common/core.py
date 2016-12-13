from utilities.logging.core import log
from utilities.common.core import get_date_from_timestamp
from utilities.db.core import execute_query
from utilities.memcache.core import MemcacheHandler
from utilities.ucip.core import update_dedicated_account
from utilities.ucip4.core import get_balance_and_date
from utilities.common.core import resolve_da_value
from lib_modular.src.config.core import SQL

class ProvisioningFailure(Exception):
    def __init__(self, err):
        self.value = 'Provisioning failed with error - %r' % err
    def __str__(self):
        return repr(self.value)

def get_subscriber_profile(resources):
    '''retrieves the subscriber details for the given subscriber'''
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    try:
        response = get_balance_and_date(resources)
        parameters['dedicatedAccountInformation'] = response['dedicatedAccountInformation']
        resources['parameters'] = parameters
    except Exception, err:
        error = 'operation:get_sub_profile. Error: %s' % (str(err))
        log(resources, error, 'error')
        raise err
    else:
        return resources


def get_da_balance(resources, da_id):
    '''
    get balance and expiry of a paticular DA

    @params: resources : dict with request details
             (containing 'get_subscriber_profile' output)
             da_id : ID of DA

    @return: balance : dict with:
                 1. DA ID supplied in function arguments
                 2. balance in DA
                 3. expiry date of DA
    '''
    parameters = resources['parameters']
    balance = {}
    balance['da_id'] = str(da_id)
    if not parameters.has_key('dedicatedAccountInformation'):
        # no DA info - No bundle here
        balance['expiry'] = 'False'
        balance['volume'] = 'False'
    else:
        for account in parameters['dedicatedAccountInformation']:
            if str( account['dedicatedAccountID'] ) == str( da_id ):
                parameters['da_info'] = account
                volume = account['dedicatedAccountValue1']
                expiry = account['expiryDate']
            else:
                continue

        if int(volume) != 0:
            balance['expiry'] = get_date_from_timestamp(expiry)
            balance['volume'] = resolve_da_value(resources, volume, 'da_to_mb')
        else:
            # dedicatedAccountValue1 is 0 - No bundle here
            balance['expiry'] = 'False'
            balance['volume'] = 'False'
        balance['units'] = 'MB'

    return balance

def get_active_dedicated_accounts(resources):
    '''
    retrieves all active DAs from Memcache or DB
    '''
    parameters = resources['parameters']
    try:
        import memcache
        memc = MemcacheHandler()
        active_das = memc.get('modular_dedicated_accounts')
    except ImportError:
        active_das = None
    if not active_das:
        resources = execute_query(resources, 
                SQL['dedicated_accounts'], [])
        parameters = resources['parameters']
        cursor = parameters['cursor']
        da_list = cursor.fetchall()

        active_das = []
        counter = 0
        while counter < cursor.rowcount:
            val = str(da_list[counter][0])
            try:
                assert str(val).isdigit()
                active_das.append(val)
            except AssertionError:
                counter += 1
            else:
                counter += 1
        cursor.connection.commit()
        cursor.close()
        try:
            memc.set('modular_dedicated_accounts', active_das)
        except UnboundLocalError:
            pass
    try:
        # remove None - for bundles without a DA
        active_das.remove(None)
        active_das.remove('None')
    except ValueError:
        pass
    parameters['dedicated_accounts'] = active_das
    resources['parameters'] = parameters
    return resources

def update_da(resources, bonus = False):
    '''
    calls utilities function to update DA
    and logs result
    '''
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    transaction_id = parameters['transactionId']
    da_id = parameters['packageDetails']['da_id']
    da_value = parameters['packageDetails']['da_value']
    expiry_date = parameters['expiry_date']
    if bonus:
        bonus = parameters['bonus']
        da_id, da_value, expiry_date = bonus['da'], \
                bonus['volume'], bonus['expiry']
        log(resources, 
                'libm.common.core.update_da() - bonus provisioning -- %s -- %s' % (
                    msisdn, bonus),'info')
    prov_summ = '%s || Provisioning %s || DA_ID: %s || DA_Value: %s || Expiry: %s' % (
            str(transaction_id), msisdn, da_id, da_value, str(expiry_date))
    log(resources, prov_summ, 'info')
    try:
        resources['parameters']['action'] = 'adjustmentAmountRelative'
        resp = update_dedicated_account(resources, da_id, 
                da_value, expiry_date)
    except Exception, err:
        error = 'operation:libm.common.update_da - %s - failed to update DA for %s. Error: %s' % (
                str(transaction_id), msisdn, str(err))
        log(resources, error, 'error')
        raise err
    else:
        del(resources['parameters']['action'])
        if str(resp['responseCode']) != '0':
            failed_provisioning = '%s || Failed to provision %s || Air Resp: %s' % (
                    transaction_id, msisdn, str(resp['responseCode']))
            log(resources, failed_provisioning, 'error')
            raise ProvisioningFailure( failed_provisioning )
        else:
            resources['parameters']['provisioned'] = True
