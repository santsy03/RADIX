'''
Telescopic provisioning module

1. get Balance
2. check Conflicting Bundles
3. check Subscription Time
4. provision Bundle
'''
import traceback
import time
from datetime import datetime, timedelta

from utilities.logging.core import log
from utilities.common.core import convert_da_time
from utilities.data_ucip.core import get_balance_and_date

from data_provisioning.src.configs.core import status
from aapcn.src.common.core import (provision_dedicated_accounts,
        IncompleteProvisioningException, provision_refill, update_uc_ut,
        UpdateUCUTException, RefillException, get_offerings, convert_time)
from aapcn.src.telescopic.config import (TELESCOPIC_PACKAGE_ATTRIBUTES,
        TIME_RESTRICTION, TELESCOPIC_DA)
from telescopic_interface.core import add_modify_sub_count


def getBalance(resources):
    '''
    - define tagging parameters

    - gets offers for telescopic

    - gets DA balances for telescopic Dedicated Accounts
    '''
    try:
        parameters = resources.get('parameters')
        transaction_id = parameters.get('transactionId')

        if 'externalData1' not in parameters:
            parameters['externalData1'] = 'get_balance'
        if 'externalData2' not in parameters:
            parameters['externalData2'] = 'get_balance'

        # OFFERS
        # ======
        get_offerings(resources)
        log(resources, 'i got the offers', 'debug')
        active_offers = parameters.get('active_offers')
        inactive_offers = parameters.get('inactive_offers')
        telescopic_offers = get_telescopic_offers()

        parameters['telescopic_offers'] = {}
        for offer in active_offers + inactive_offers:
            # check for presense of telescopic offers
            if int(offer['offer_id']) in telescopic_offers:
                parameters['telescopic_offers'][offer['offer_id']] = offer

        resources['parameters'] = parameters
        log(resources, '{transactionId} - {msisdn} - telescopic offers -'
                ' {telescopic_offers}'.format(**parameters), 'info')

        # DEDICATED ACCOUNTS
        # ==================
        telescopic_balances = {}
        resp = get_balance_and_date(resources)
        if resp.get('responseCode') == 0:
            da_balances = resp['dedicatedAccountInformation']
            for da in da_balances:
                if int(da.get('dedicatedAccountID')) in TELESCOPIC_DA:
                    telescopic_balances[str(da.get('dedicatedAccountID'))] = {}
                    telescopic_balances[str(da.get('dedicatedAccountID'))]['volume'] = da.get('dedicatedAccountValue1')
                    telescopic_balances[str(da.get('dedicatedAccountID'))]['start_date'] = convert_time(da.get('startDate'))
                    telescopic_balances[str(da.get('dedicatedAccountID'))]['expiry_date'] = convert_time(da.get('expiryDate'))
        log(resources, '{} - telescopic DAs - {}'.format(
            transaction_id, telescopic_balances), 'info')
        resources['parameters']['telescopic_dedicated_accounts'] = telescopic_balances

        resources['parameters']['balance'] = telescopic_balances
        return resources

    except Exception, err:
        log(resources, '{} - telescopic.getBalance - {}'.format(
            transaction_id, str(err)), 'error')
        log(resources, traceback.format_exc(), 'error')
        #raise err


def get_telescopic_offers():
    '''
    return telescopic offer IDs
    '''
    telescopic_offers = []
    for each in TELESCOPIC_PACKAGE_ATTRIBUTES.values():
        telescopic_offers.append(each[6])

    return telescopic_offers

def is_barred(resources):
    '''
    returns true if a number is barred from 
    purchasing this bundle
    else
    returns False
    '''
    return False

def checkConflictingBundles(resources):
    '''
    @param   resources    dict
    @return  conflicting  bool
    '''
    parameters = resources.get('parameters')
    transaction_id = parameters.get('transactionId')
    return False


def check_subscription_time(resources):
    '''
    checks that we are within transaction time constraint

    @param   resources            dict
    @return  within_time_limits   bool
    '''
    resources['parameters']['now'] = time.asctime()
    log(resources, '{transactionId} - {msisdn} subsc time - {now}'.format(
        **resources['parameters']), 'debug')
    try:
        assert time.localtime().tm_hour <= TIME_RESTRICTION.get('hour') and\
                time.localtime().tm_min <= TIME_RESTRICTION.get('min')
        return True
    except AssertionError:
        log(resources, '{transactionId} - {msisdn} - time limit'.format(
            **resources['parameters']), 'debug')
        return False
    except Exception, err:
        log(resources, '{} - check_subscription_time - {}'.format(
            resources['parameters']['transactionId'], str(err)), 'error')
        raise err


def get_package_attributes(resources):
    '''
    get price, volume, validity, DA of telescopic bundle
    based on whether it's the 1st, 2nd, 3rd, or nth subscription
    of the day

    @return package
    '''
    try:
        today = datetime.now().date()
        parameters = resources.get('parameters')
        transaction_id = parameters.get('transactionId')
        msisdn = parameters.get('msisdn')

        telescopic_balances = parameters.get('telescopic_dedicated_accounts')
        telescopic_offers = parameters.get('telescopic_offers')

        off1, off2, off3 = TELESCOPIC_PACKAGE_ATTRIBUTES['1'][6],\
                TELESCOPIC_PACKAGE_ATTRIBUTES['2'][6],\
                TELESCOPIC_PACKAGE_ATTRIBUTES['3'][6]
        da1, da2, da3 = TELESCOPIC_PACKAGE_ATTRIBUTES['1'][3],\
                TELESCOPIC_PACKAGE_ATTRIBUTES['2'][3],\
                TELESCOPIC_PACKAGE_ATTRIBUTES['3'][3]
        
        package = TELESCOPIC_PACKAGE_ATTRIBUTES['1']
        log(resources, '{transactionId} - {msisdn} - telescopic dedicated accounts '
                '- {telescopic_dedicated_accounts} - telescopic offers - '
                '{telescopic_offers}'.format(**parameters), 'debug')

        if str(da1) in telescopic_balances:
            expiry_date1 = telescopic_balances[str(da1)]['expiry_date']
            if expiry_date1.year == 9999:
                package = TELESCOPIC_PACKAGE_ATTRIBUTES['1']
            elif expiry_date1.date() == today and str(da2) in telescopic_balances:
                expiry_date2 = telescopic_balances[str(da2)]['expiry_date']
                if expiry_date2.year == 9999:
                    package = TELESCOPIC_PACKAGE_ATTRIBUTES['2']

                elif expiry_date2.date() == today:
                    package = TELESCOPIC_PACKAGE_ATTRIBUTES['3']
            else:
                package = TELESCOPIC_PACKAGE_ATTRIBUTES['2']
        

    except Exception, err:
        log(resources, '{} - telescopic.getpackage fail - {}'.format(
            transaction_id, str(err)), 'error')

    else:
        log(resources, '{} - telescopic package - {}'.format(
            transaction_id, package), 'info')
        return package


def telescopic_subscription_limit(resources):
    today = datetime.now().date()
    parameters = resources.get('parameters')
    transaction_id = parameters.get('transactionId')
    msisdn = parameters.get('msisdn')
    telescopic_balances = parameters.get('telescopic_dedicated_accounts')
    da3 = TELESCOPIC_PACKAGE_ATTRIBUTES['3'][3]
    try:
        if str(da3) in telescopic_balances:
            expiry_date = telescopic_balances[str(da3)]['expiry_date']
            if expiry_date.date() == today:
                return True
            else:
                return False
        else:
            return False

    except Exception, e:
        log(resources, "{} - telescopic - subscription -err - {}"\
                .format(transaction_id, str(traceback.format_exc())))


def update_package_details(resources):
    '''
    '''
    try:
        package_attrs = get_package_attributes(resources)
        price, volume, validity, da_id, refill_id, uc_id, offer =\
                package_attrs
        resources['parameters']['price'] = price
        resources['parameters']['volume'] = volume
        resources['parameters']['validity'] = validity
        resources['parameters']['da_id'] = da_id
        resources['parameters']['refill_id'] = refill_id
        resources['parameters']['uc'] = uc_id
        resources['parameters']['ut'] = uc_id
        resources['parameters']['trans_amount'] = '00'

    except Exception, err:
        log(resources, '{} - telescopic.update_package_details- {}'.format(
            resources['parameters']['transactionId'], str(err)), 'error')


def provisionBundle(resources):
    '''
    provisions a bundle
    1. sets  a refill id
    2. updates the usageThresholdsAndCounters
    '''
    log(resources, resources, 'debug')
    parameters = resources['parameters']
    package_category_name = parameters['package_category_name']

    top_up_amount = int(parameters['volume']) * 1024 * 1024

    new_bal = top_up_amount

    refill_id = parameters['refill_id']
    trans_amount = parameters['trans_amount'] 
    # first set refill_id
    
    msisdn = parameters['msisdn']
    trans_id = parameters['transactionId']

    parameters['uc_id'] = int(parameters['uc'])
    parameters['ut_id'] = int(parameters['ut'])
    if 'args' in parameters:
        if 'is_renew' in (parameters['args']):
            log(resources, "is_renew", 'info')
            parameters['externalData1'] = parameters['package_name'] + renw_prefix
            parameters['externalData2'] = 'auto_renewal' + '_' + parameters['beneficiary']
        elif 'can_renew' in (parameters['args']):
            args = parameters['args']
            if args['can_renew'] == '1':
                parameters['externalData1'] = parameters['package_name'] + renw_prefix
                parameters['externalData2'] = 'auto_renewal' + '_' + parameters['beneficiary']
            else:
                parameters['externalData1'] = parameters['package_name']
                parameters['externalData2'] = 'oneoff' + '_' + parameters['beneficiary']

        elif parameters['transaction_type'] == 'B':
            parameters['externalData1'] = parameters['package_name']
            parameters['externalData2'] = 'oneoff'+ '_'+  parameters['beneficiary']

        else:
            parameters['externalData1'] = parameters['package_name']
            parameters['externalData2'] = 'oneoff' + '_' + parameters['beneficiary']

    log(resources, str(parameters['externalData1']), 'info')
    log(resources, str(parameters['externalData2']), 'info')
    try:
        resp = provision_refill(resources, refill_id, trans_amount)
    except Exception, err:
        error = "op: provisionBundle: error %s" % (str(err)) 
        log(resources, error, 'error')
        log(resources, traceback.format_exc(), 'error') 
        raise IncompleteProvisioningException("provisionBundle(refill)",
                trans_id, msisdn)
    else:
        if resp[2] == True:
            try:
                resp_2 = update_uc_ut(resources, new_bal)
            except Exception, err:
                log(resources, traceback.format_exc(), 'error')
                raise IncompleteProvisioningException("provisionBundle(updateucut)", 
                        trans_id, msisdn)
            else:
                if resp_2[2] == True:
                    info = "successfully provisioned %s with %s" % (
                            resources['parameters']['msisdn'], refill_id)
                    log(resources, info, 'info')
                    da_id = parameters['da_id']
                    bal = {}
                    bal['amount'] = str(new_bal)
                    parameters['balance'][str(package_category_name)] = bal
                    add_modify_sub_count(resources)

                else:
                    raise UpdateUCUTException(str(resp_2[1])) 
        else:
            log(resources, 'failed to refill', 'error')
            raise RefillException(str(resp[1]))


    return resources


def check_conflicting_bundles(resources):
    '''
    PEP8 compliant wrapper for `checkConflictingBundles`
    '''
    return checkConflictingBundles(resources)


def get_balance(resources):
    '''
    PEP8 compliant wrapper for `getBalance`
    '''
    return getBalance(resources)


def provision_bundle(resources):
    '''
    PEP8 compliant wrapper for `provisionBundle`
    '''
    return provisionBundle(resources)
