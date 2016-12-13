'''
defines provisional logic for incremental
bundles
'''
from utilities.logging.core import log
from utilities.db.core import get_connection as getConnections
from aapcn.src.common.core import get_usage, get_offerings
from aapcn.src.common.core import update_uc_ut, provision_refill
from aapcn.src.common.core import RefillException, UpdateUCUTException  
from aapcn.src.common.core import IncompleteProvisioningException
from aapcn.src.common.core import update_uc_ut, provision_refill
from aapcn.src.common.core import get_da_balance
from config import DA_BALANCE
from config import voice_bundles_to_be_recorded, weekend_days, service_class_check_packages, unallowed_service_classes,time_restricted_packages,offer_deletion_packages
from datetime import datetime, timedelta
import traceback

renw_prefix = '_autorenewal'

def getBalance(resources):
    '''
    get all the balance for all packages in this category
    The one with the largest expiry is given as the balance
    for all packages of this group
    '''
    #resources = get_usage(resources)
    #resources = get_offerings(resources)
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
    info = "trans_id: %s. NO UC/UT CHECK FOR VOICE, msisdn: %s" %(str(trans_id),msisdn)
    #log(resources, info, 'debug')

    da_bal = 0
    #da_bal = get_da_balance(resources, int(parameters['uc']))
    info = "trans_id: %s. NO DA BAL. CHECK FOR VOICE, msisdn: %s" % (str(trans_id),msisdn)
    #log(resources, info, 'debug')

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
    #log(resources, dbg, 'debug')

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
    pack = parameters['package_name']
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
                #tagging for upsell
                if parameters['transaction_type'] == 'C':
                    parameters['externalData1'] = 'upsell'+ '_'+parameters['package_name']
                    parameters['externalData2'] = parameters['cc_msisdn']+ '_'+  parameters['beneficiary']
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
                    #Log transaction in fun_plus_subscriptions table if necessary for counting
                    if resources['parameters']['packageId'] in voice_bundles_to_be_recorded:
                        db_insert_fun_plus_record(resources)

                else:
                    raise UpdateUCUTException(str(resp_2[1])) 
        else:
            log(resources, 'TransID- %s MSISDN: %s failed to refill:%s-%s with RESP CODE: %s '% (str(trans_id),str(msisdn),str(pack),str(refill_id),str(resp[1])), 'error')
            #log(resources, 'failed to refill', 'error')
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
    if int(resources['parameters']['packageId']) in service_class_check_packages:
        log(resources, 'MSISDN: %s *********Checking SC' % (resources['parameters']['msisdn']),'debug')
        is_allowed = check_service_class(resources)
        if is_allowed:
            return False
        else:
            return True
    else:
        return False


def is_weekend(resources):
    import datetime
    today = datetime.datetime.now().strftime('%a')
    if today in weekend_days:
        info = "MSISDN: %s, TODAY IS: %s" % (resources['parameters']['msisdn'],today)
        log(resources, info, 'debug')
        return True
    else: 
        info = "MSISDN: %s, TODAY IS: %s" % (resources['parameters']['msisdn'],today)
        log(resources, info, 'debug')
        return False


def check_is_weekend(msisdn):
    import datetime
    today = datetime.datetime.now().strftime('%a')
    if today in weekend_days:
        print 'MSISDN: %s, TODAY IS: %s' %(str(msisdn),str(today))
        return True
    else:
        print 'MSISDN: %s, TODAY IS: %s' %(str(msisdn),str(today))
        return False


def is_time_barred(resources):
    """
    checks whether a sub is barred due to the current time
    """
    pack = resources['parameters']['packageId']
    current_block = 'undefined'
    now = datetime.now()
    msisdn = resources['parameters']['msisdn']

    if pack in time_restricted_packages:
        if now.hour in range(0, 17):
            info = "current time: %s, %s allowed for msisdn: %s" % (str(now),resources['parameters']['package_name'], msisdn)
            log(resources, info, 'debug')
            return False
        else:
            info = "current time: %s, %s NOT allowed for msisdn: %s" % (str(now),resources['parameters']['package_name'], msisdn)
            log(resources, info, 'debug')
            return True
    elif pack == '203':
        if now.hour in range(8, 17):
            info = "current time: %s, %s allowed for msisdn: %s" % (str(now),resources['parameters']['package_name'], msisdn)
            log(resources, info, 'debug')
            return False
        else:
            info = "current time: %s, %s NOT allowed for msisdn: %s" % (str(now),resources['parameters']['package_name'], msisdn)
            log(resources, info, 'debug')
            return True
    else:
        info = "Package: %s,%s is not time barred  msisdn: %s" % (str(pack),resources['parameters']['package_name'], msisdn)
        log(resources, info, 'debug')
        return False


def db_insert_fun_plus_record(resources):
    '''
    inserts a record in fun_plus_subscriptions
    '''
    package_id = resources['parameters']['packageId']
    trans_id = resources['parameters']['transactionId']
    msisdn  = resources['parameters']['msisdn']
    now = datetime.now()
    sql = sql = ("insert into fun_plus_subscriptions(ID,MSISDN,PACKAGE_ID,CREATED_AT)values(:trans_id, :msisdn, :package_id, :now)")
    params = {'trans_id': trans_id,'msisdn': msisdn,'package_id': package_id,'now': now}

    try:
        connection = getConnections(resources)
        log(resources, "got connection", 'debug')
        cursor = connection.cursor()
        cursor.execute(sql,params)
        cursor.connection.commit()
        cursor.close()

    except Exception,e:
        error = ('operation: Could not insert Funplus package details' + 'for packageID:%s,Error:%s' %(str(package_id),str(e)))
        error = e
        log(resources, error, 'error')
        try:
            cursor.close()
        except:
            pass
        raise e

def subscription_check(resources):
    from datetime import datetime
    package_id = resources['parameters']['packageId']
    msisdn  = resources['parameters']['msisdn']
    fmt = "%d-%m-%y"
    today = datetime.now().strftime(fmt)
    info = "FUN_PLUS Package_ID*******%s" % (package_id)
    log(resources, info, 'info')
    #sql = sql = ("select * from fun_plus_subscriptions where PACKAGE_ID =:package_id and MSISDN =:msisdn and cast(CREATED_AT as date) LIKE to_date(sysdate, 'DD-MON-YY')")
    sql = ("select * from fun_plus_subscriptions where PACKAGE_ID =:package_id and MSISDN =:msisdn and to_char(CREATED_AT, 'dd-mm-yy') = :td")
    params = {'msisdn': msisdn,'package_id': package_id, 'td':today}

    try:
        connection = getConnections(resources)
        log(resources, "got connection", 'debug')
        cursor = connection.cursor()
        cursor.execute(sql,params)
        details = cursor.fetchall()
        cursor.close()
        if details:
            info = "MSISDN: %s, ALREADY SUBSCRIBED TO FUN_PLUS" % (msisdn)
            log(resources, info, 'info')
            return True
        else:
            info = "MSISDN: %s, NOT SUBSCRIBED TO FUN_PLUS" % (msisdn)
            log(resources, info, 'info')
            return False

    except Exception,e:
        error = ('operation: Could not Check Funplus Subscription details' + 'for packageID:%s,Error:%s' %(str(package_id),str(e)))
        error = e
        log(resources, error, 'error')
        try:
            cursor.close()
        except:
            pass
        raise e
        return False

def setup():
    from cx_Oracle import SessionPool
    import cx_Oracle
    from utilities.secure.core import decrypt
    from configs.config import databases
    from DBUtils.PooledDB import PooledDB
    resources = {}
    pool = PooledDB(
                cx_Oracle,
                maxcached = 5,
                maxconnections = 500,
                user = decrypt(databases['core']['username']),
                password = decrypt(databases['core']['password']),
                dsn = databases['core']['string'],
                threaded = True
                )
    pool.timeout = 300
    resources['connections'] = pool
    return resources


def voice_subscription_check(msisdn,package_id):
    from data_provisioning.src.common.db.core import getConnection
    from datetime import datetime
    fmt = "%d-%m-%y"
    today = datetime.now().strftime(fmt)
    #sql = sql = ("select * from fun_plus_subscriptions where PACKAGE_ID =:package_id and MSISDN =:msisdn and cast(CREATED_AT as date) LIKE to_date(sysdate, 'DD-MON-YY')")
    sql = sql = ("select * from fun_plus_subscriptions where PACKAGE_ID =:package_id and MSISDN =:msisdn and to_char(CREATED_AT, 'dd-mm-yy') = :td")
    paramms = {'msisdn': msisdn,'package_id': package_id, 'td':today}
    resources ={}
    resources = setup()
    try:
        connection = getConnection(resources)
        #log(resources, "got connection", 'debug')
        cursor = connection.cursor()
        cursor.execute(sql,paramms)
        details = cursor.fetchall()
        cursor.close()
        if details:
            print 'MSISDN: %s, ALREADY SUBSCRIBED TO FUN_PLUS' %(str(msisdn))
            return True
        else:
            print 'MSISDN: %s, NOT SUBSCRIBED TO FUN_PLUS' %(str(msisdn))
            return False

    except Exception,e:
        error = '%s operation: Could not Check Funplus Subscription details for packageID:%s,Error:%s' %(str(msisdn),str(package_id),str(e))
        print error
        log(resources, error, 'error')
        log(resources, traceback.format_exc(), 'error')
        try:
            cursor.close()
        except:
            pass
        raise e
        return False

def check_service_class(resources):
    ''' 
    Checks the serviceClassCurrent for the given subscriber
    '''
    from ussd.prepaid.airHandler import AIRHandler
    air = AIRHandler()
    try:
        details = air.getBalanceAndDate(resources['parameters']['msisdn'])
        if details['responseCode'] == 0:
            log(resources, 'MSISDN: %s is in SC %s' % (resources['parameters']['msisdn'],str(details['serviceClassCurrent'])),'debug')
            sc = int(details['serviceClassCurrent'])
            if sc in unallowed_service_classes:
                log(resources, 'MSISDN: %s SERVICE_CLASS NOT ALLOWED' % (resources['parameters']['msisdn']),'debug')
                return False
            else:
                log(resources, 'MSISDN: %s SERVICE_CLASS IS ALLOWED' % (resources['parameters']['msisdn']),'debug')
                return True
        else:
            error = 'operation:check_service_class,for %s,FAILED resp code:%s' % (resources['parameters']['msisdn'], str(details['responseCode']))
            log(resources, error, 'error')
            return False
    except Exception,e:
        error = 'operation:getBalanceAndDate,desc: error retrieving sub details for %s,desc:%s' %(resources['parameters']['msisdn'],str(e))
        error = e
        log(resources, error, 'error')
        return False

def whitelisted_customer_care(msisdn):
    from data_provisioning.src.common.db.core import getConnection
    sql = sql = ("select * from CUSTOMER_CARE_WHITELIST where MSISDN =:msisdn")
    params = {'msisdn': msisdn}
    resources ={}
    resources = setup()

    try:
        connection = getConnections(resources)
        log(resources, "Whitelisting Check-got connection", 'debug')
        cursor = connection.cursor()
        cursor.execute(sql,params)
        details = cursor.fetchall()
        cursor.close()
        if details:
            info = "CC MSISDN: %s,IS WHITELISTED" % (msisdn)
            log(resources, info, 'debug')
            return True
        else:
            info = "CC MSISDN: %s,IS NOT WHITELISTED" % (msisdn)
            log(resources, info, 'debug')
            return False
    except Exception,e:
        error = ('operation: Could not Check Whitelisting details' + 'for MSISDN:%s,Error:%s' %(msisdn,str(e)))
        error = e
        log(resources, error, 'error')
        try:
            cursor.close()
        except:
            pass
        raise e
        return False

def is_whitelisted(resources):
    package_id = resources['parameters']['packageId']
    msisdn  = resources['parameters']['msisdn']
    info = "Checking Whitelisting for Package_ID*******%s" % (package_id)
    log(resources, info, 'info')
    sql = sql = ("select * from VOICE_BUNDLES_WHITELIST where PACKAGE_ID =:package_id and MSISDN =:msisdn")
    params = {'msisdn': msisdn,'package_id': package_id}

    try:
        connection = getConnections(resources)
        log(resources, "Whitelisting Check-got connection", 'debug')
        cursor = connection.cursor()
        cursor.execute(sql,params)
        details = cursor.fetchall()
        cursor.close()
        if details:
            info = "MSISDN: %s,IS WHITELISTED FOR PACKAGE ID  %s" % (msisdn,resources['parameters']['packageId'])
            log(resources, info, 'debug')
            return True
        else:
            info = "MSISDN: %s,IS NOT WHITELISTED FOR PACKAGE ID  %s" % (msisdn,resources['parameters']['packageId'])
            log(resources, info, 'debug')
            return False
    except Exception,e:
        error = ('operation: Could not Check Whitelisting details' + 'for MSISDN:%s packageID:%s,Error:%s' %(msisdn,str(package_id),str(e)))
        error = e
        log(resources, error, 'error')
        try:
            cursor.close()
        except:
            pass
        raise e
        return False

def voice_is_whitelisted(msisdn,package_id):
    from data_provisioning.src.common.db.core import getConnection
    print '%s :Checking Whitelisting for Package_ID*******%s' %(str(msisdn),str(package_id))
    sql = sql = ("select * from VOICE_BUNDLES_WHITELIST where PACKAGE_ID =:package_id and MSISDN =:msisdn")
    paramms = {'msisdn': msisdn,'package_id': package_id}
    resources ={}
    resources = setup()
    try:
        connection = getConnection(resources)
        log(resources, "Whitelisting Check-got connection", 'debug')
        cursor = connection.cursor()
        cursor.execute(sql,paramms)
        details = cursor.fetchall()
        cursor.close()
        if details:
            print 'MSISDN: %s,IS WHITELISTED FOR PACKAGE ID  %s' %(str(msisdn),str(package_id))
            return True
        else:
            print 'MSISDN: %s,IS NOT WHITELISTED FOR PACKAGE ID  %s' %(str(msisdn),str(package_id))
            return False
    except Exception,e:
        error = 'operation: Could not Check Whitelisting details for MSISDN:%s packageID:%s,Error:%s' %(str(msisdn),str(package_id),str(e))
        print error
        log(resources, error, 'error')
        log(resources, traceback.format_exc(), 'error')
        try:
            cursor.close()
        except:
            pass
        raise e
        return False

def retailer_fun_cool_whitelisted(msisdn,package_id):
    from data_provisioning.src.common.db.core import getConnection
    print '%s :Checking Whitelisting for Package_ID*******%s' %(str(msisdn),str(package_id))
    sql = sql = ("select * from RETAILER_FUNCOOL_WHITELIST where MSISDN =:msisdn")
    paramms = {'msisdn': str(msisdn)}
    resources ={}
    resources = setup()
    try:
        connection = getConnection(resources)
        log(resources, "Whitelisting Check-got connection", 'debug')
        cursor = connection.cursor()
        cursor.execute(sql,paramms)
        details = cursor.fetchall()
        cursor.close()
        if details:
            print 'MSISDN: %s,IS WHITELISTED FOR PACKAGE ID  %s' %(str(msisdn),str(package_id))
            return True
        else:
            print 'MSISDN: %s,IS NOT WHITELISTED FOR PACKAGE ID  %s' %(str(msisdn),str(package_id))
            return False
    except Exception,e:
        error = 'operation: Could not Check Whitelisting details for MSISDN:%s packageID:%s,Error:%s' %(str(msisdn),str(package_id),str(e))
        print error
        log(resources, error, 'error')
        log(resources, traceback.format_exc(), 'error')
        try:
            cursor.close()
        except:
            pass
        raise e
        return False

def retailer_fun_ora_whitelisted(msisdn,package_id):
    from data_provisioning.src.common.db.core import getConnection
    print '%s :Checking Whitelisting for Package_ID*******%s' %(str(msisdn),str(package_id))
    sql = sql = ("select * from RETAILER_FUNORA_WHITELIST where MSISDN =:msisdn")
    paramms = {'msisdn': str(msisdn)}
    resources ={}
    resources = setup()
    try:
        connection = getConnection(resources)
        log(resources, "Whitelisting Check-got connection", 'debug')
        cursor = connection.cursor()
        cursor.execute(sql,paramms)
        details = cursor.fetchall()
        cursor.close()
        if details:
            print 'MSISDN: %s,IS WHITELISTED FOR PACKAGE ID  %s' %(str(msisdn),str(package_id))
            return True
        else:
            print 'MSISDN: %s,IS NOT WHITELISTED FOR PACKAGE ID  %s' %(str(msisdn),str(package_id))
            return False
    except Exception,e:
        error = 'operation: Could not Check Whitelisting details for MSISDN:%s packageID:%s,Error:%s' %(str(msisdn),str(package_id),str(e))
        print error
        log(resources, error, 'error')
        log(resources, traceback.format_exc(), 'error')
        try:
            cursor.close()
        except:
            pass
        raise e
        return False


def voice_offer_deletion(resources):
    '''
     checks and deletes offer_id if in sub's profile
    '''
    from aapcn.src.common.core import get_offerings
    from utilities.data_ucip.core import delete_offers
    offer = int(resources['parameters']['offer_id'])
    pack = int(resources['parameters']['packageId'])
    resources['parameters']['offer_id'] = offer
    resp = get_offerings(resources)
    if 'active_offers' or 'inactive_offers' in resources['parameters']:
        if(any(offerid.get('offer_id', None) == offer for offerid in (resources['parameters']['active_offers']))):
            info = "MSISDN: %s Offer:%s Available in Active_offers" % (resources['parameters']['msisdn'],str(resources['parameters']['offer_id']))
            log(resources,info,'debug')
            try:
                details = delete_offers(resources)
                if details['responseCode'] == 0:
                    info = "MSISDN: %sOffer_ID: %s Deleted From Active_offers" % (resources['parameters']['msisdn'],str(resources['parameters']['offer_id']))
                    log(resources,info,'debug')
                    return True
                else:
                    info = 'operation:Delete Offer_Id: %s FAILED,for %s,resp code:%s' % (str(resources['parameters']['offer_id']),resources['parameters']['msisdn'], str(details['responseCode']))
                    log(resources,info,'debug')
                    if pack in offer_deletion_packages:
                        return True
                    else:
                        return False
            except Exception,e:
                error = 'operation:Delete Offer_ID: %s,desc: error Deleting Offer for %s,desc:%s' %(str(resources['parameters']['offer_id']),resources['parameters']['msisdn'],str(e))
                log(resources,error,'error')
                if pack in offer_deletion_packages:
                    return True
                else:
                    return False

        elif(any(offerid.get('offer_id', None) == offer for offerid in (resources['parameters']['inactive_offers']))):
            info = "MSISDN: %sOffer_ID:%s Available in Inactive_offers" % (resources['parameters']['msisdn'],str(resources['parameters']['offer_id']))
            log(resources,info,'debug')
            try:
                details = delete_offers(resources)
                if details['responseCode'] == 0:
                    info = "MSISDN: %sOffer_ID: %s Deleted From Active_offers" % (resources['parameters']['msisdn'],str(resources['parameters']['offer_id']))
                    log(resources,info,'debug')
                    return True
                else:
                    error = 'operation:Delete Offer_Id: %s FAILED,for %s,resp code:%s' % (str(resources['parameters']['offer_id']),resources['parameters']['msisdn'],str(details['responseCode']))
                    log(resources,error,'error')
                    if pack in offer_deletion_packages:
                        return True
                    else:
                        return False
            except Exception,e:
                error = 'operation:Delete Offer_ID: %s,desc: error Deleting Offer for %s,desc:%s' %(str(resources['parameters']['offer_id']),resources['parameters']['msisdn'],str(e),)
                log(resources,error,'debug')
                if pack in offer_deletion_packages:
                    return True
                else:
                    return False

        else:
            info = "MSISDN: %s Has  No Offer_ID: %s" % (resources['parameters']['msisdn'],str(resources['parameters']['offer_id']))
            log(resources,info,'debug')
            return True

    else:
        info = "MSISDN: %s Has  No Offer_ID: %s" % (resources['parameters']['msisdn'],str(resources['parameters']['offer_id']))
        log(resources,info,'debug')
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
    #from etc.core import databases
    from utilities.secure.core import decrypt
    #username = databases['pavp']['username']
    #password = databases['pavp']['password']
    #string = databases['pavp']['string']
    resources = {}
    parameters = {'msisdn':'254788292170'}
    resources['parameters'] = parameters
    #print is_time_barred(resources)
    '''
    parameters = {'msisdn':'254788292170','transactionId':'008977','externalData1':'datatests','externalData2':'datatests','packageCost':'500','ut':'1010',}
    resources['parameters'] = parameters
    resources['parameters']['refill_profile'] = 'MB37'
    #resources[ 'parameters']['volume'] = '20480'
    resources[ 'parameters']['volume'] = str(int(20*1024*1024))
    resources['parameters']['transaction_amount'] = '5'
    #resources['connections'] = SessionPool(decrypt(username),decrypt(password),string,1,10,5,threaded=True)
    #db_operations = DbOperations(resources)
    #offers = db_operations.fetch_offers()
    #resources['parameters']['avail_offers'] = offers
    #resources = get_last_purchase(resources)
    #resources = get_offerings(resources)
    #resources = group(resources)
    #resources = get_usage(resources)
    
    #resources =  getBalance(resources)
    #resources = provisionBundle(resources)
    #print checkConflictingBundles(resources)
    volume = parameters['volumeString']
    expiry = parameters['expiry']
    name = parameters['packageName']
    print volume, expiry, name
    print is_time_barred(resources)
    print resources['parameters']['balance']
    print resources['parameters']['bonuses']
    status = '5'
    '''


