'''
defines provisional logic for incremental
bundles
'''
from utilities.logging.core import log
from aapcn.src.common.core import get_usage, get_offerings
from aapcn.src.common.core import update_uc_ut, provision_refill
from aapcn.src.common.core import RefillException, UpdateUCUTException  
from aapcn.src.common.core import IncompleteProvisioningException
from aapcn.src.common.core import update_uc_ut, provision_refill
from aapcn.src.common.core import get_da_balance
from config import DA_BALANCE

from datetime import datetime, timedelta
import traceback

renw_prefix = '_autorenewal'

def getBalance(resources):
    '''
    get all the balance for all packages in this category
    The one with the largest expiry is given as the balance
    for all packages of this group
    '''
    resources = get_usage(resources)
    resources = get_offerings(resources)
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    trans_id = parameters['transactionId']
    parameters['service_id'] = parameters['package_name']

    package_category_name = parameters['package_category_name']

    total_bal = 0

    #get total balance for this package category

    if 'usage_list' in parameters:
        if len(parameters['usage_list']) > 0:
            usage_list = parameters['usage_list']
            for each in usage_list:
                for _uc, bal in each.iteritems():
                    if int(each['uc_id']) == int(parameters['uc']):
                        log(resources, "UC: "+ str(parameters['uc']), 'debug')
                        total_bal = each['balance']
    cat_bal = {}
    info = "trans_id: %s. UC UT balance= %s, msisdn: %s" %(str(trans_id),
            str(total_bal),
            msisdn)
    log(resources, info, 'debug')

    da_bal = get_da_balance(resources, int(parameters['uc']))
    info = "trans_id: %s. DA balance= %s, msisdn: %s" % (str(trans_id),
            str(da_bal), 
            msisdn)
    log(resources, info, 'debug')

    if DA_BALANCE:
        total_bal = da_bal

    cat_bal = {}
    cat_bal['amount'] = total_bal

    #get largest expiry for this catgeory

    expiry_list = []
    if 'active_offers' in  parameters:
        if len(parameters['active_offers']) > 0:
            active_offers = parameters['active_offers']

            #To DO
            for each_offer in active_offers:
                curr_exp = each_offer['expiry']
                expiry_list.append(curr_exp)

    new_expiry_list = sort_expiry(expiry_list)

    if len(new_expiry_list) > 0:
        expiry = new_expiry_list[0]
    else:
        expiry = False

    cat_bal['expiry'] = expiry

    parameters['balance'] = {}

    parameters['balance'][parameters['package_category_name']]= cat_bal

    dbg = "trans_id: %s, msisdn: %s, balance: %s " % (str(trans_id),
            str(msisdn),
            str(parameters['balance']))
    log(resources, dbg, 'debug')

    resources['parameters'] = parameters
    return resources


def provisionBundle(resources):
    '''
    provisions a bundle
    1. sets  a refill id
    2. updates the usageThresholdsAndCounters
    '''

    parameters = resources['parameters']
    package_category_name = parameters['package_category_name']
    curr_bal = parameters['balance'][package_category_name]
    curr_amount = curr_bal['amount']

    top_up_amount = int(parameters['volume']) * 1024 *1024

    new_bal = top_up_amount + int(curr_amount)

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
                    curr_bal = parameters['balance'][parameters['package_category_name']]
                    curr_bal['amount'] = new_bal
                    parameters['balance'][parameters['package_category_name']] = curr_bal

                else:
                    raise UpdateUCUTException(str(resp_2[1])) 
        else:
            log(resources, 'failed to refill', 'error')
            raise RefillException(str(resp[1]))


    return resources


def checkConflictingBundles(resources):
    '''
    returns True if a sub is not allowed to subscribe 
    to the current bundle

    returns False if otherwise

    '''

    return False

def is_barred(resources):
    '''
    returns true if a number is barred from 
    purchasing this bundle
    else
    returns False
    '''
    return False

def sort_expiry(expiry_list):
    '''
    returns a list of sorted expirys given 
    a list of unsorted ones
    '''
    less = []
    equal = []
    greater = []
    if len(expiry_list) > 1:
        pivot = expiry_list[0]
        for x in expiry_list:
            if x < pivot:
                less.append(x)
            if x == pivot:
                equal.append(x)
            if x > pivot:
                greater.append(x)
        return sort_expiry(greater) + equal + sort_expiry(less)
    else:
        return expiry_list


if __name__ == '__main__':
    from cx_Oracle import SessionPool
    from etc.core import databases
    from utilities.secure.core import decrypt
    username = databases['pavp']['username']
    password = databases['pavp']['password']
    string = databases['pavp']['string']
    resources = {}
    parameters = {'msisdn':'254788292170','transactionId':'008977','externalData1':'datatests','externalData2':'datatests','packageCost':'500','ut':'1010',}
    resources['parameters'] = parameters
    resources['parameters']['refill_profile'] = 'MB37'
    #resources[ 'parameters']['volume'] = '20480'
    resources[ 'parameters']['volume'] = str(int(20*1024*1024))
    resources['parameters']['transaction_amount'] = '5'
    resources['connections'] = SessionPool(decrypt(username),decrypt(password),string,1,10,5,threaded=True)
    db_operations = DbOperations(resources)
    offers = db_operations.fetch_offers()
    resources['parameters']['avail_offers'] = offers
    resources = get_last_purchase(resources)
    #resources = get_offerings(resources)
    resources = group(resources)
    #resources = get_usage(resources)
    resources =  getBalance(resources)
    #resources = provisionBundle(resources)
    #print checkConflictingBundles(resources)
    '''
    volume = parameters['volumeString']
    expiry = parameters['expiry']
    name = parameters['packageName']
    print volume, expiry, name
    '''
    print resources['parameters']['balance']
    print resources['parameters']['bonuses']
    status = '5'

