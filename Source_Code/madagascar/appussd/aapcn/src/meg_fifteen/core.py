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
from datetime import datetime, timedelta
from config import MAX_PURCHASES_PER_BLOCK
from utilities.db.core import get_connection
from utilities.db.core import execute_query
from aapcn.src.common.core import get_da_balance
from config import DA_BALANCE



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

    dbg = "balance: %s " % str(parameters['balance'])
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
    purchasing this bundle else
    returns False

    For my meg 15 one may be barred due to:
    a) current time
    (only available between 8 and 11.59 and 2 and 4.59)

    b) number of subscriptions per time block
    (only two for each time block)

    '''
    is_time_blocked = is_time_barred(resources)
    if is_time_blocked:
        return is_time_blocked
    else:
        has_bought_enough = is_quota_blocked(resources)
        return has_bought_enough


def is_time_barred(resources):
    """
    checks whether a sub is barred due to the current time
    """
    barred = False

    now = datetime.now()
    msisdn = resources['parameters']['b_msisdn']

    if now.hour in range(17, 25):
        info = "current time: %s, my meg 15 not available: msisdn: %s" % (str(now), msisdn)
        log(resources, info, 'info')

        barred = True
    elif now.hour in range(0, 8):
        info = "current time: %s, my meg 15 not available: msisdn: %s" % (str(now), msisdn)
        log(resources, info, 'info')

        barred = True
    elif now.hour == 12:
        info = "current time: %s, my meg 15 not available: msisdn: %s" % (str(now), msisdn)
        log(resources, info, 'info')

        barred = True

    return barred

def is_quota_blocked(resources):
    '''
    gets whether thhe number is blocked based on number of purchase per block
    '''
    quota = False
    block = get_current_time_block(resources)
    msisdn = resources['parameters']['b_msisdn']

    conf = get_current_status(resources)

    if block == 'undefined':
        quota = False
    else:
        if conf:
            count = conf[block]
            if count >= MAX_PURCHASES_PER_BLOCK:
                info = "msisdn: %s purchases: %s block: %s" % (msisdn, str(count), str(block))
                log(resources, info, 'debug')
                quota = True
            else:
                info = "msisdn: %s purchases: %s block: %s" % (msisdn, str(count), str(block))
                log(resources, info, 'debug')
                info = "sub: %s is eligible, purchases: %s block: %s" % (msisdn, str(count), str(block))
                log(resources, info, 'debug')
                quota = False
        else:
            info = "subscriber: %s not in MEG_15 db. Hes therefore ELIGIBLE" % (msisdn)
            log(resources, info, 'debug')
            quota = False


    return quota


def get_current_time_block(resources):
    '''
    returns whether its morning or afternoon based on time
    '''
    current_block = 'undefined'
    now = datetime.now()

    if now.hour in range(8,12):
        info = "current time: %s" % (str(now))
        current_block = 'morning'

    elif now.hour in range(13, 18):
        info = "current time: %s" % (str(now))
        log(resources, info, 'info')
        current_block = 'afternoon'

    return  current_block



def get_current_status(resources):
    '''
    returns the current configuration from the tracker table
    '''
    msisdn = resources['parameters']['b_msisdn']

    sql = ("SELECT ID, MSISDN, MORNING_COUNT,AFTERNOON_COUNT," +
            "COMPLETED_AT FROM MEG_FIFTN_TRACKER WHERE MSISDN = :MSISDN")
    params = {'MSISDN':msisdn}

    try:
        connection = get_connection(resources)
        cursor = connection.cursor()
        cursor.execute(sql, params)
        results = cursor.fetchall()
    except Exception, err:
        error = "error; op: get_current_status: aapcn.meg_fifteen: msisdn: %s" %(msisdn)
        log(resources, error, 'error')
        log(resources, traceback.format_exc(), 'error')

        return None
    else:
        cursor.close()
        if not results:
            # create initial record. the return None
            create_initial_record(resources)
            return None
        else:
            if is_todays_record(resources, results, msisdn):
                info = "current status: %s. msisdn %s" % (str(results), msisdn)
                log(resources, info, 'debug')
                conf = {}
                results = results[0]
                conf['id'] = results[0]
                conf['morning'] = results[2]
                conf['afternoon'] = results[3]
                conf['completed_at'] = results[4]
                return conf

            else:
                #rebase to today
                res = rebase_to_today(resources)
                
                conf = {}
                conf['id'] = results[0][0]
                conf['morning'] = 0
                conf['afternoon'] = 0
                conf['completed_at'] = datetime.now()

                return conf


def create_initial_record(resources):
    '''
    creates the very first configuration for
    the tracker table
    '''
    
    msisdn = resources['parameters']['b_msisdn']

    sql = ("INSERT INTO MEG_FIFTN_TRACKER (MSISDN,MORNING_COUNT,AFTERNOON_COUNT,REQUESTED_AT,COMPLETED_AT)"+
            "VALUES(:msisdn,0,0,systimestamp, systimestamp)")
    params = {'MSISDN':msisdn}

    try:
        connection = get_connection(resources)
        cursor = connection.cursor()
        cursor.execute(sql, params)
    except Exception, err:
        error = "error; op: create_initial_record: aapcn.meg_fifteen: msisdn: %s" %(msisdn)
        log(resources, error, 'error')
        log(resources, traceback.format_exc(), 'error')
    else:
        cursor.connection.commit()
        cursor.close()
        info = "initial my meg 15 record created: msisdn %s" % (msisdn)
        log(resources, info, 'info')

def is_todays_record(resources, results, msisdn):
    """
    checks whether the given data is todays
    """
    today = False
    results = results[0]

    last_trans = results[4]
    now = datetime.now()

    if (last_trans.day == now.day) and (last_trans.month == now.month) and (last_trans.year == now.year):
        info = "last transcation took place today %s: %s 's record is still valid" %(str(last_trans),msisdn)
        log(resources, info, 'debug')

        today = True
    else:
        info = "last transcation took place %s: %s 's record needs updating to today" %(str(last_trans),msisdn)
        log(resources, info, 'debug')

    return today

def rebase_to_today(resources):
    '''
    resets the values in the tracker to today
    to rebegin the counting
    '''

    msisdn = resources['parameters']['b_msisdn']

    sql = (
    "UPDATE MEG_FIFTN_TRACKER SET REQUESTED_AT = SYSTIMESTAMP, COMPLETED_AT = SYSTIMESTAMP," +
    "MORNING_COUNT = 0, AFTERNOON_COUNT = 0 WHERE MSISDN = :msisdn"
    )
    params = {'MSISDN':msisdn}

    try:
        connection = get_connection(resources)
        cursor = connection.cursor()
        cursor.execute(sql, params)
    except Exception, err:
        error = "error; op: rebase_to_today: aapcn.meg_fifteen: msisdn: %s" %(msisdn)
        log(resources, error, 'error')
        log(resources, traceback.format_exc(), 'error')
    else:
        cursor.connection.commit()
        cursor.close()
        info = "rebased %s 's record to today" % (msisdn)
        log(resources, info, 'debug')

        return True





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
    from configs.config import databases
    from utilities.secure.core import decrypt
    username = databases['core']['username']
    password = databases['core']['password']
    string = databases['core']['string']
    resources = {}
    parameters = {'b_msisdn':'261330465390','transactionId':'008977','externalData1':'datatests','externalData2':'datatests','packageCost':'500','ut':'1010',}
    resources['parameters'] = parameters
    resources['parameters']['refill_profile'] = 'MB37'
    #resources[ 'parameters']['volume'] = '20480'
    resources[ 'parameters']['volume'] = str(int(20*1024*1024))
    resources['parameters']['transaction_amount'] = '5'
    resources['connections'] = SessionPool(decrypt(username),decrypt(password),string,1,10,5,threaded=True)
    print get_current_status(resources)
    #print create_initial_record(resources)
    #print rebase_to_today(resources)
