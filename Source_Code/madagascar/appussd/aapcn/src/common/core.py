'''
This file contains methods that call air commands from utilities.
'''

from datetime import datetime, timedelta
from utilities.data_ucip.core import refill, updateUsageThresholdsAndCounters
from utilities.data_ucip.core import get_offers, getUsageThresholdsAndCounters,get_offers2, getUsageThresholdsAndCounters2
from utilities.logging.core import log
from utilities.db.core import execute_query
from utilities.data_ucip.core import get_balance_and_date
from utilities.data_ucip.core import set_value_offer_id,update_da_account
from aapcn.src.common.config import no_ucut_update_package_ids
import time
import traceback


def get_usage(resources):
    '''
    Calls the GetUsageThresholdsAndCounters command from utilities.
    It then packs the parameters and passes them to the calling function
    '''
    msisdn = resources['parameters']['msisdn']
    trans_id = resources['parameters']['transactionId']

    usage_list = []
    parameters = resources['parameters']

    if 'externalData1' not in parameters:
        parameters['externalData1'] = "getUCUT"
    if 'externalData2' not in parameters:
        parameters['externalData2'] = "getUCUT"
    resources['parameters'] = parameters


    try:
        resp = getUsageThresholdsAndCounters(resources)
    except Exception, err:
        error = ('%s op: get_usage failed: Error: %s ' % (msisdn, str(err)))
        log( resources, error, 'error')
        raise IncompleteProvisioningInfoException("get_usage", trans_id, msisdn) 
    else:
        log(resources, resp, 'debug')
        info = "trans_id: %s, msisdn: %s, op: getUCUT: resp code: %s " % (str(trans_id),
                str(msisdn),
                resp['responseCode'])
        log(resources, info, 'info')
        if resp['responseCode'] == 0:
            if resp.has_key('usageCounterUsageThresholdInformation'):
                usage_info = resp['usageCounterUsageThresholdInformation']
                pack_usage(resources, usage_info)
            else:
                resources['parameters']['usage_list'] = []
                resources['parameters']['depleted']= []
    return resources

def get_usage2(resources):
    '''
    Calls the GetUsageThresholdsAndCounters command from utilities.
    It then packs the parameters and passes them to the calling function
    '''
    msisdn = resources['parameters']['msisdn']
    trans_id = resources['parameters']['transactionId']

    usage_list = []
    parameters = resources['parameters']

    if 'externalData1' not in parameters:
        parameters['externalData1'] = "getUCUT"
    if 'externalData2' not in parameters:
        parameters['externalData2'] = "getUCUT"
    resources['parameters'] = parameters


    try:
        resp = getUsageThresholdsAndCounters2(resources)
    except Exception, err:
        error = ('%s op: get_usage failed: Error: %s ' % (msisdn, str(err)))
        log( resources, error, 'error')
        raise IncompleteProvisioningInfoException("get_usage", trans_id, msisdn)
    else:
        log(resources, resp, 'debug')
        info = "trans_id: %s, msisdn: %s, op: getUCUT: resp code: %s " % (str(trans_id),
                str(msisdn),
                resp['responseCode'])
        log(resources, info, 'info')
        if resp['responseCode'] == 0:
            if resp.has_key('usageCounterUsageThresholdInformation'):
                usage_info = resp['usageCounterUsageThresholdInformation']
                pack_usage(resources, usage_info)
            else:
                resources['parameters']['usage_list'] = []
                resources['parameters']['depleted']= []
    return resources


def pack_usage(resources, usage_info):
    '''
    packs the usage into an easy to parse dictionary
    '''
    usage_list = []
    depleted = []

    trans_id = resources['parameters']['transactionId']

    for element in usage_info:
        try:
            uc_id = element['usageCounterID']
            usage_counter_value = element['usageCounterValue']
            threshold_info = element['usageThresholdInformation']
            for item in threshold_info:
                if item['usageThresholdID'] == uc_id:
                    threshold_value = item['usageThresholdValue']

            if (int(threshold_value) - int(usage_counter_value) <= 0) and (int(usage_counter_value) != 0):
                dep_bal = int(threshold_value) - int(usage_counter_value)
                dep_dets = {'uc_id':uc_id,'balance': dep_bal}
                depleted.append(dep_dets)
            else:
                uc_bal = int(threshold_value) - int(usage_counter_value)
                uc_details = {'uc_id':uc_id,'balance': uc_bal}
                usage_list.append(uc_details)
        except Exception, err:
            error = 'op: pack_usage: error: %s' % (str(err))
            log(resources, error, 'error')
            
    resources['parameters']['usage_list'] = usage_list
    resources['parameters']['depleted'] = depleted

    log(resources, "trans_id: %s - active usage:msisdn: %s:usage: %s" % (
        str(trans_id),
        resources['parameters']['msisdn'],
        resources['parameters']['usage_list']), 'debug')
    log(resources, "trans_id: %s - depleted usage:msisdn: %s:usage: %s" % (
        str(trans_id),
        resources['parameters']['msisdn'],
        resources['parameters']['depleted']), 'debug')

    return resources

def get_offerings(resources):
    '''
    returns a lis of the current offers a
    subscriber is subscribed to
    '''
    msisdn = resources['parameters']['msisdn']
    trans_id = str(resources['parameters']['transactionId'])

    offer_list = []
    to_delete = []
    now = datetime.now()
    parameters = resources['parameters']
    if 'externalData1' not in parameters:
        parameters['externalData1'] = "getoffers"
    if  'externalData2' not in parameters:
        parameters['externalData2'] = "getoffers"
    resources['parameters'] = parameters

    try:
        resp = get_offers(resources)
    except Exception, err:
        error = "op: get_offers: error: %s" % (str(err))
        log(resources, error, 'error')
        log(resources, traceback.format_exc(), 'error')
        raise IncompleteProvisioningInfoException("get_offerings", trans_id, msisdn) 
    else:
        if resp['responseCode'] == 0 and resp.__contains__('offerInformation'):
            offer_dets = resp['offerInformation']
            for element in offer_dets:
                try:
                    start = convert_time(element['startDate'])
                    expiry = convert_time(element['expiryDate'])
                except KeyError,err:
                    start = convert_time(element['startDateTime'])
                    expiry = convert_time(element['expiryDateTime'])

                offer_id = element['offerID']
                if expiry.day == now.day:
                    offer_dict = {'offer_id': offer_id,'start':start,'expiry':expiry}
                    offer_list.append(offer_dict)
                elif expiry > now:
                    if expiry.year != 9999:
                        offer_dict = {'offer_id': offer_id,'start':start,'expiry':expiry}
                        offer_list.append(offer_dict)
                    elif expiry.year == 9999:
                        expired_dict = {'offer_id': offer_id,'start':start,'expiry':expiry}
                        to_delete.append(expired_dict)
                else:
                    expired_dict = {'offer_id': offer_id,'start':start,'expiry':expiry}
                    to_delete.append(expired_dict)

    resources['parameters']['active_offers'] = offer_list
    dbg = "trans_id: %s - active offers: %s msisdn: %s" % (str(trans_id),
            str(offer_list),
            resources['parameters']['msisdn'])
    log(resources, dbg, 'debug')

    resources['parameters']['inactive_offers'] = to_delete
    dbg = "trans_id: %s - inactive offers: %s msisdn: %s" % (str(trans_id),
            str(to_delete),
            resources['parameters']['msisdn'])
    log(resources, dbg, 'debug')

    return resources


def get_offerings2(resources):
    '''
    returns a lis of the current offers a
    subscriber is subscribed to
    '''
    msisdn = resources['parameters']['msisdn']
    trans_id = str(resources['parameters']['transactionId'])

    offer_list = []
    to_delete = []
    now = datetime.now()
    parameters = resources['parameters']
    if 'externalData1' not in parameters:
        parameters['externalData1'] = "getoffers"
    if  'externalData2' not in parameters:
        parameters['externalData2'] = "getoffers"
    resources['parameters'] = parameters

    try:
        resp = get_offers2(resources)
    except Exception, err:
        error = "op: get_offers: error: %s" % (str(err))
        log(resources, error, 'error')
        log(resources, traceback.format_exc(), 'error')
        raise IncompleteProvisioningInfoException("get_offerings", trans_id, msisdn)
    else:
        if resp['responseCode'] == 0 and resp.__contains__('offerInformation'):
            offer_dets = resp['offerInformation']
            for element in offer_dets:
                try:
                    start = convert_time(element['startDate'])
                    expiry = convert_time(element['expiryDate'])
                except KeyError,err:
                    start = convert_time(element['startDateTime'])
                    expiry = convert_time(element['expiryDateTime'])

                offer_id = element['offerID']
                if expiry.day == now.day:
                    offer_dict = {'offer_id': offer_id,'start':start,'expiry':expiry}
                    offer_list.append(offer_dict)
                elif expiry > now:
                    if expiry.year != 9999:
                        offer_dict = {'offer_id': offer_id,'start':start,'expiry':expiry}
                        offer_list.append(offer_dict)
                    elif expiry.year == 9999:
                        expired_dict = {'offer_id': offer_id,'start':start,'expiry':expiry}
                        to_delete.append(expired_dict)
                else:
                    expired_dict = {'offer_id': offer_id,'start':start,'expiry':expiry}
                    to_delete.append(expired_dict)

    resources['parameters']['active_offers'] = offer_list
    dbg = "trans_id: %s - active offers: %s msisdn: %s" % (str(trans_id),
            str(offer_list),
            resources['parameters']['msisdn'])
    log(resources, dbg, 'debug')

    resources['parameters']['inactive_offers'] = to_delete
    dbg = "trans_id: %s - inactive offers: %s msisdn: %s" % (str(trans_id),
            str(to_delete),
            resources['parameters']['msisdn'])
    log(resources, dbg, 'debug')

    return resources

def provision_refill(resources, refill_id, trans_amount):
    '''
    provisions a bundle with the correct refill id

    '''
    msisdn = resources['parameters']['msisdn']
    resources['parameters']['transactionAmount'] = trans_amount
    try:
        resp = refill(resources)
    except Exception, err:
        error = 'op: refill: error:%s' % (str(err))
        log(resources, error, 'error')
        log(resources, traceback.format_exc(), 'error')
    else:
        #if resp['responseCode'] == 0 or resp['responseCode'] == 136:
        resources['parameters']['refill_resp']= resp['responseCode']

        if resp['responseCode'] == 0:
            inf = "%s-%s:REFILL RESP:%s" %(str(msisdn),str(refill_id),str(resp['responseCode']))
            log(resources, inf, 'debug')
            return (resources, resp['responseCode'], True)
        else:
            inf = "%s-%s:REFILL RESP:%s" %(str(msisdn),str(refill_id),str(resp['responseCode']))
            log(resources, inf, 'debug')
            return (resources, resp['responseCode'], False)


def update_uc_ut(resources, amount):
    '''
    updates usage threshhold and counters
    the UC will by default be set to 0
    the amount as passed in the resources dictionary is
    what will be set as the threshold value.
      
    '''

    resources['parameters']['threshold_value'] = amount
    pack = resources['parameters']['packageId']

    if pack in no_ucut_update_package_ids:
        inf = "%s:NO UCUT UPDATE FOR:%s" %(resources['parameters']['msisdn'],str(pack))
        log(resources, inf, 'debug')
        return (resources, True, True)
    else:
        try:
            resp = updateUsageThresholdsAndCounters(resources)

        except Exception, err:
            error = "op: updateUtUC: error: %s" % str(err)
            log(resources, error, 'error')
            log(resources, traceback.format_exc(), 'error')
        else:
            log(resources, resp['responseCode'], 'debug')
            if resp['responseCode'] == 0:
                return (resources, resp['responseCode'], True)
            else:
                return (resources, resp['responseCode'], False)

def get_data_profile(resources):
    '''
    to be done
    will get ALL THE DATA information for a given bundle and 
    pack it according to the different categories
    '''
    from utilities.db.core import get_connection as getConnections
    from config import da_mappings
    resources = get_offerings(resources)
    parameters = resources['parameters']
    if 'externalData1' not in parameters:
        parameters['externalData1'] = 'get_balance'
    if 'externalData2' not in parameters:
        parameters['externalData2'] = 'get_balance'

    resources['parameters'] = parameters
    msisdn = resources['parameters']['msisdn']
    trans_id = str(resources['parameters']['transactionId'])
    balance = 0
    bal_dets = {}
    check_night_offer_id = 'False'

    resources['parameters']['balance'] = {}
    try:
        resp = get_balance_and_date(resources)
    except Exception, err:
        error = "op: get_balance: %s" % (str(err))
        log(resources, error, 'error')
        log(resources, traceback.format_exc(), 'error')
        raise IncompleteProvisioningInfoException("get_da_balance (balance)", trans_id, msisdn)
    else:
        log(resources, str(resp), 'debug')
        offer_list = []
        night_das = ['1150', '1151']
        list_string = ""
        if 'active_offers' in resources['parameters']:
            for each in resources['parameters']['active_offers']:
                offer_list.append(str(each['offer_id']))
            if len(offer_list) <=0:
                return resources
            list_string = tuple([str(x) for x in offer_list])
            if '1044' in list_string:
                check_night_offer_id = 'True'
            off_param = {}
            if len(offer_list) == 1:
                off_param['offer_id'] = str(offer_list[0])
                sql = "select distinct(uc) from new_provisioning_packages where offer_id = :offer_id"
            else:
                sql = "select distinct(uc) from new_provisioning_packages where offer_id in %s" % str(list_string)
            log(resources,trans_id + " : " +sql, 'debug')
            conn = getConnections(resources)
            cursor = conn.cursor()
            try:
                if off_param and len(offer_list) == 1:
                    cursor.execute(sql, off_param)
                else:
                    cursor.execute(sql)
            except Exception, err:
                raise err
            else:
                possible_das = cursor.fetchall()
                log(resources, str(possible_das),'debug')
                possible_das = [x[0] for x in possible_das]

                if len(possible_das) > 0:
                    if check_night_offer_id:
                        possible_das.extend(night_das)
                    log(resources,trans_id + " : " +"possible das: " + str(possible_das), 'debug')
                    bal_dets = {}
                    if resp['responseCode'] == 0:
                        ded_info = resp['dedicatedAccountInformation']
                        for da in ded_info:
                            if str(da['dedicatedAccountID']) in possible_das:
                                name = da_mappings[str(da['dedicatedAccountID'])]
                                amount = da['dedicatedAccountValue1']
                                expiry = str(convert_time(da['expiryDate']))

                                bal_dets[name] = {'amount': str(amount), 'expiry':expiry}


                        info = "trans_id: %s -, balance = %s, msisdn: %s " % (str(trans_id),
                                str(bal_dets),
                                str(msisdn))

                        log(resources, info, 'info')


        resources['parameters']['balance'] = bal_dets

    return resources


def get_da_balance(resources, da_id):
    '''
    gets the balance as per the given DA ID
    '''

    parameters = resources['parameters']
    if 'externalData1' not in parameters:
        parameters['externalData1'] = 'get_balance'
    if 'externalData2' not in parameters:
        parameters['externalData2'] = 'get_balance'

    resources['parameters'] = parameters
    msisdn = resources['parameters']['msisdn']
    trans_id = str(resources['parameters']['transactionId'])

    balance = 0
    try:
        resp = get_balance_and_date(resources)
    except Exception, err:
        error = "op: get_balance: %s" % (str(err))
        log(resources, error, 'error')
        log(resources, traceback.format_exc(), 'error')
        raise IncompleteProvisioningInfoException("get_da_balance", trans_id, msisdn)
    else:
        if resp['responseCode'] == 0:
            ded_info = resp['dedicatedAccountInformation']
            for da in ded_info:
                if da['dedicatedAccountID'] == da_id:
                    balance = da['dedicatedAccountValue1']
                    
            info = "trans_id: %s - da id: %s, balance = %s, msisdn: %s " % (str(trans_id),
                    str(da_id), 
                    str(balance),
                    str(msisdn))
            log(resources, info, 'info')
    return balance

            

def convert_time(air_time):
    '''
    converts air time to datetime
    '''
    log({}, "AIRTIME:%s"%str(air_time), 'info')
    t = str(air_time)[-4:]
    try:
        fmt = '%Y%m%dT%H:%M:%S+' + str(t)
        new_time = datetime.fromtimestamp(time.mktime(time.strptime(str(air_time),fmt)))
    except OverflowError, e:
        new_time = datetime(9999,12,31,0,0)
        raise err
    return new_time


class RefillException(Exception):
    """
    Exception raised when a refill 
    fails du to resp code
    """
    def __init__(self, resp_code):
        error = 'REFILL FAILED: RESP CODE %s' % resp_code
        self.value = error

    def __str__(self):
        return repr(self.value)


class UpdateUCUTException(Exception):
    """
    Exception raised when an update uc ut
    fails due to resp code
    """
    def __init__(self, resp_code):
        error = 'UPDATE UC UT FAILED: RESP CODE %s' % resp_code
        self.value = error

    def __str__(self):
        return repr(self.value)

class IncompleteProvisioningException(Exception):
    """
    Exception raised when ANY of the provisioning commands 
    fails due to some other error
    """
    def __init__(self, method_name, trans_id, msisdn):
        error = "%s- error at: %s. PROVISIONING FAILED %s" % (str(trans_id),
                method_name, 
                msisdn) 
        self.value = error

    def __str__(self):
        return repr(self.value)

class IncompleteProvisioningInfoException(Exception):
    """
    Exception raised when ANY of the IN commands run 
    before provisioning fail due to any error
    """
    def __init__(self, method_name, trans_id, msisdn):
        error = '%s - error at: %s. CANNOT PROCEED. %s' % (str(trans_id),
                method_name, 
                msisdn)
        self.value = error

    def __str__(self):
        return repr(self.value)



def get_dedicated_account_ids(resources, cat_id):
    sql = ('select offer_id from new_provisioning_packages where package_category_id = :cat_id')
    params = {'cat_id':cat_id}
    resources = execute_query(resources, sql, params)
    parameters = resources['parameters']
    cursor = parameters['cursor']
    results = cursor.fetchall()
    try:
        cursor.close()
    except Exception, err:
        pass
    da_list=[]
    final_list = []
    l = []
    for i in results:
        da_list.append(i[0])

    for i in da_list:
        l.extend(i.split('-'))
    log(resources, (str(l)), 'debug')
    l = list(set(l))
    final_list = l[:]
    return final_list


def get_dedicated_account_values(resources, da_list):
    '''
    retrieves the value and expiry for the dedicated accounts specified in the the da list
    '''
    parameters = resources['parameters']
    parameters['externalData1'] = "getbalance"
    parameters['externalData2'] = "getbalance"
    resources['parameters'] = parameters
    response = get_balance_and_date(resources)
    log(resources, str(response), 'debug')
    da_information = response['dedicatedAccountInformation']
    category_details = {'balance': 0 , 'accounts':{}, 'expiry': datetime.now()}
    max_expiry = category_details['expiry']
    balance = category_details['balance']
    accounts = {}
    for dedicated_account in da_information:
        if str(dedicated_account['dedicatedAccountID']) in da_list:
            da_value = dedicated_account['dedicatedAccountValue1']
            da_id = dedicated_account['dedicatedAccountID']
            if int(da_value) > 0:
                da_expiry = convert_da_time(dedicated_account['expiryDate'])
                accounts[str(da_id)] = {'value':int(da_value), 'expiry': da_expiry}
                balance = balance + int(da_value)
                if da_expiry > max_expiry:
                    max_expiry = da_expiry
    category_details['balance'] = balance
    category_details['accounts'] = accounts
    category_details['expiry'] = max_expiry
    return category_details


def get_subscriber_profile(resources):
    '''retrieves the subscriber details for the given subscriber'''
    from aapcn.src.sacc_fun.core import getBalance as get_fun_balance
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    response = get_balance_and_date(resources)
    parameters['currentMainAccount'] = response['accountValue1']
    parameters['dedicatedAccountInformation'] = response['dedicatedAccountInformation']
    parameters['currentServiceClass'] = response['serviceClassCurrent']
    log(resources, "current service class: " + str(parameters['currentServiceClass']))
    resources['parameters'] = parameters
    resources = get_fun_balance(resources)
    return resources


def provision_dedicated_accounts(resources, dedicated_accounts, provision_expiry):
    ''' provisions the actual dedicated accounts'''
    from utilities.ucip.core import update_dedicated_account
    parameters = resources['parameters']
    status = []
    for key, value in dedicated_accounts.iteritems():
        da_id = int(key)
        da_value = value['value']
        log(resources, '%s,%s,%s,%s' %(str(da_id), str(da_value), str(provision_expiry), parameters['transactionId']),'debug')
        resp = update_dedicated_account(resources, da_id, da_value, provision_expiry)
        log(resources,str(resp),'debug')
        status.append(resp['responseCode'])

    return status


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

def update_parabole_offer(resources, offer, start, expiry):
    '''
    Update refilled parabole offer withe the parameters supplied
    @params:
        1) msisdn: the msisdn to provision
        2) offer_id: the offer_id to set
        3) expiry: the expiry for the offer id

    @return:
        Pass -  Nothing expected
    '''
    res = {}
    params = {}
    msisdn = resources['parameters']['msisdn']
    trans_id = resources['parameters']['transactionId']
    res['parameters'] = params
    tag = 'updateOffer_%s' % (msisdn)
    res['parameters']['externalData1'] = 'parabole'
    res['parameters']['externalData2'] = tag
    res['parameters']['transactionId'] = trans_id
    res['parameters']['msisdn'] = resources['parameters']['msisdn']
    res['parameters']['end_date'] = expiry
    res['parameters']['offer_id'] = offer
    res['parameters']['start_date'] = start

    try:
        resp = set_value_offer_id(res)
    except Exception, err:
        error = "UPDATE PARABOLE OFFER EXPIRY FAILED: msisdn: %s, trans_id: %s, err: %s" %(
                msisdn,
                trans_id,
                str(err))
        log(resources, error, 'error')
        log(resources, traceback.format_exc(), 'error')
        pass
    else:
        if resp['responseCode'] == 0:
            dbg = "msisdn: %s, trans_id: %s PARABOLE OFFER EXPIRY UPDATED TO: %s" %(msisdn,trans_id,str(expiry))
            log(resources, dbg, 'info')
            pass
        else:
            error = "UPDATE PARABOLE OFFER EXPIRY FAILED: trans_id: %s, msisdn: %s, RESP: %s" %(
                    msisdn,
                    trans_id,
                    str(resp['responseCode']))
            log(resources, error, 'error')
            pass

def update_parabole_da(resources, da, expiry):
    '''
    Update refilled parabole DA withe the parameters supplied
    @params:
        1) msisdn: the msisdn to provision
        2) da_id: the da_id to update expiry
        3) expiry: the expiry for the DA id

    @return:
        Pass -  Nothing expected
    '''
    res = {}
    params = {}
    msisdn = resources['parameters']['msisdn']
    trans_id = resources['parameters']['transactionId']
    res['parameters'] = params
    tag = 'updateDa_%s' % (msisdn)
    res['parameters']['externalData1'] = 'parabole'
    res['parameters']['externalData2'] = tag
    res['parameters']['transactionId'] = trans_id
    res['parameters']['msisdn'] = resources['parameters']['msisdn']
    res['parameters']['expiryDate'] = expiry
    res['parameters']['dedicatedAccountId'] = da
    res['parameters']['daAction']  = 'adjustmentAmountRelative'
    res['parameters']['adjustmentAmount'] = '0'

    try:
        resp =update_da_account(res)
    except Exception, err:
        error = "UPDATE PARABOLE DA EXPIRY FAILED: msisdn: %s, trans_id: %s, err: %s" %(
                msisdn,
                trans_id,
                str(err))
        log(resources, error, 'error')
        log(resources, traceback.format_exc(), 'error')
        pass
    else:
        if resp['responseCode'] == 0:
            dbg = "msisdn: %s, trans_id: %s PARABOLE DA EXPIRY UPDATED TO: %s" %(msisdn,trans_id,str(expiry))
            log(resources, dbg, 'info')
            pass
        else:
            error = "UPDATE PARABOLE DA EXPIRY FAILED: trans_id: %s, msisdn: %s, RESP: %s" %(
                    msisdn,
                    trans_id,
                    str(resp['responseCode']))
            log(resources, error, 'error')
            pass


if __name__ == '__main__':
    '''
    from utilities.secure.core import decrypt
    from configs.config import databases
    from cx_Oracle import SessionPool
    username = databases['core']['username']
    password = databases['core']['password']
    string = databases['core']['string']
    resources = {}
    resources['connections'] = SessionPool(decrypt(username),decrypt(password),string,1,10,5,threaded=True)
    parameters = {}
    parameters['msisdn'] = '261330465390'
    parameters['transactionId'] = '008977'
    parameters['externalData1'] = 'datatests'
    parameters['externalData2'] = 'datatests'
    parameters['packageCost'] = '2000'
    parameters['ut']  = '1011'
    parameters['uc']  = '1011'
    resources['parameters'] = parameters
    resources['parameters']['refill_profile'] = 'MB05'
    resources[ 'parameters']['volume'] = '20480'
    #print get_usage(resources)
    #print do_refill(resources)
    #print update_thresholds(resources)
    #print get_dedicated_account_ids(resources, 4)
    '''
    pass
