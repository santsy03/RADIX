from utilities.logging.core import log
from datetime import datetime
from utilities.metrics.core import response_time 

'''core methods for accessing ucip functionality'''

def get_air(resources):
    '''
    method for creating a standard air object
    '''
    from utilities.data_ucip.airHandler import AIRHandler
    from utilities.data_ucip.config import hosts

    parameters = resources['parameters']
    params = {}
    params['transactionId'] = str(parameters['transactionId'])
    '''
    if 'originHost' in parameters:
        originHost = (str(parameters['originHost'])).strip().upper()
        params['originHost'] = 'radix%s'%(originHost)
    ''' 
    try:
        params['externalData1'] = parameters['externalData1']
    except KeyError:
        params['externalData1'] = 'rdx_%s' % str(parameters['service_id'])
    else:
        print params['externalData1']
        log(resources, params['externalData1'], 'debug')

    try:
        params['externalData2'] = parameters['externalData2']
    except KeyError:
        params['externalData2'] = 'rdx_%s' % str(parameters['package_id'])
    else:
        print params['externalData1']
        log(resources, params['externalData2'], 'debug')

    
    host = hosts[int(params['transactionId'])%2]
    
    return AIRHandler(params, host)

def bill_subscriber(resources, transaction_id=''):
    '''
    method for billing a prepaid subscriber
    '''
    air = get_air(resources)
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    amount = '-%d' % (int(parameters['price'])*100)
    msisdn = parameters['msisdn']
    transaction_id = str(parameters['transactionId'])
    to_bill = '%s - util.data_ucip.core.bill_sub(). billing %s from %s' % (
            str(transaction_id), amount, msisdn)
    log(resources, to_bill, 'info')
    try:
        return air.updateBalanceAndDate(msisdn, amount)
    except Exception, err:
        bill_error = 'operation: utilities.ucip.core.bill_subscriber() failed. - %s' % (
                str(err) )
        log(resources, bill_error, 'error')
        raise err


def set_service_class(resources):
    '''
    set the subscriber's service class
    '''
    air = get_air(resources)
    parameters = resources['parameters']
    service_class = parameters['service_class']
    msisdn = parameters['msisdn']
    return air.setServiceClass(msisdn, service_class)

def get_balance_and_date(resources):
    '''
    method for setting an offer_id for a given subscriber
    '''
    air = get_air(resources)
    parameters = resources['parameters']
    msisdn = parameters['msisdn']

    start = datetime.now()

    metric = "aapcn.air.getbalanceanddate"
    resp = air.getBalanceAndDate(msisdn,)
    response_time(metric, start)
    stop = datetime.now()
    duration = str((stop - start).total_seconds())
    log(resources, 'time: get_balance_and_date: %s' %duration, 'info')
    return resp


def set_offer_id(resources):
    '''
    method for setting an offer_id for a given subscriber
    '''
    air = get_air(resources)
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    offer_id = parameters['offer_id']
    start_date = parameters['start_date']
    end_date = parameters['end_date']
    log(resources, 'Update offers' + str([msisdn, offer_id, end_date, start_date]), 'info')
    resp = air.updateOffer(msisdn, offer_id, end_date, start_date)
    resp_code = int(resp['responseCode'])
    if resp_code != 0:
        print 'info-%s-Error setting Offer ID %s - Resp code - %s'%(msisdn, str(offer_id),str(resp_code))
    return resp

def set_value_offer_id(resources):
    '''
    method for setting an offer_id for a given subscriber
    '''
    air = get_air(resources)
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    offer_id = parameters['offer_id']
    start_date = parameters['start_date']
    end_date = parameters['end_date']
    log(resources, 'Update offers' + str([msisdn, offer_id, end_date, start_date]), 'info')
    resp = air.updateValueOffer(msisdn, offer_id, end_date, start_date)
    resp_code = int(resp['responseCode'])
    if resp_code != 0:
        print 'info-%s-Error setting Offer ID %s - Resp code - %s'%(msisdn, str(offer_id),str(resp_code))
    return resp

def get_accumulators(resources):
    '''
    method for retrieving accumulators for the given subscriber
    '''
    air = get_air(resources)
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    return air.getAccumulators(msisdn)

def get_offers(resources):
    '''
    method for retrieving currently provisioned offers
    '''
    air = get_air(resources)
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    
    start = datetime.now()

    metric = "aapcn.air.getoffers"
    resp = air.getOffers(msisdn)
    response_time(metric, start)

    stop = datetime.now()
    duration = str((stop - start).total_seconds())
    log(resources, 'time: get_offers: %s' % duration, 'info')

    return resp

def delete_offers(resources):
    '''
    method for deleting offer ids
    '''
    air = get_air(resources)
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    offer_id = parameters['offer_id']
    return air.deleteOffer(msisdn, offer_id)

def update_da_account(resources, data_unit = 6):
    '''
    method to update dedicated account
    '''
    air = get_air(resources)
    parameters = resources['parameters']
    amount = parameters['adjustmentAmount']
    msisdn = parameters['msisdn']
    account = parameters['dedicatedAccountId']
    action = parameters['daAction']
    expiry_date = parameters['expiryDate']
    log(resources, 'Update DA' + str([msisdn, amount, action, account, expiry_date]), 'info')
    resp = air.updateDedicatedAccount(msisdn, amount, action, account, expiry_date, data_unit)
    resp_code = int(resp['responseCode'])
    if resp_code != 0:
        print 'info-%s-Error updating DA %s, Amount %s, Resp code - %s'%(msisdn, str(account), str(amount), str(resp_code))
    return resp

def get_sub_balance(resources, dtype = 'A'):
    '''
    method for getting subscriber balance for self and B_party
    '''
    air = get_air(resources)
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    if dtype == 'B':
        msisdn = parameters['b_msisdn']
    return air.getBalanceAndDate(msisdn,)

def refill(resources):
    '''
    method for doing data refills
    '''
    air = get_air(resources)
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    refill_id = parameters['refill_id']
    amount = parameters['transactionAmount']

    start = datetime.now()
    metric = "aapcn.air.refills"
    log(resources, 'Refilling ' + str([msisdn,refill_id,amount]), 'info')
    resp =  air.Refill(msisdn, refill_id, amount)

    response_time(metric, start)
    stop = datetime.now()
    duration = str((stop - start).total_seconds())
    log(resources, 'time: refill: %s' % duration, 'info')


    return resp

def updateUsageThresholdsAndCounters(resources):
    '''
    method for updating usage counters and thresholds for data
    '''
    air = get_air(resources)
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    uc  = parameters['uc_id']
    ut  = parameters['ut_id']
    thresh_value = parameters['threshold_value']

    start = datetime.now()
    metric = "aapcn.air.updateusagethreshholdandcounters"


    log(resources, 'Update Threshold ' + str([msisdn,uc, ut,thresh_value]), 'info')
    resp = air.updateUsageThresholdsAndCounters(msisdn, uc, ut, thresh_value)

    response_time(metric, start)
    
    stop = datetime.now()
    duration = str((stop - start).total_seconds())
    log(resources, 'time: update uc_ut: %s' % duration, 'info')

    return resp

def getUsageThresholdsAndCounters(resources):
    '''
    method for getting the usage threshold and counters
    '''
    air = get_air(resources)
    parameters = resources['parameters']
    msisdn = parameters['msisdn']

    start = datetime.now()
    metric = "aapcn.air.getusagethreshholdandcounters"

    resp = air.GetUsageThresholdsAndCounters(msisdn)

    response_time(metric, start)
    stop = datetime.now()
    duration = str((stop - start).total_seconds())
    log(resources, 'time: get_uc_ut: %s' % duration, 'info')

    return resp

if __name__ == '__main__':
    from datetime import datetime, timedelta
    resources = {}
    parameters = {}
    #parameters['msisdn'] = '261330998255'
    parameters['msisdn'] = '261330465390'
    #parameters['msisdn'] = '261331432473'
    #parameters['msisdn'] = '338598731'
    #parameters['msisdn'] = '330798574'
    #parameters['msisdn'] = '261330798574'
    #parameters['msisdn'] = '330798574'
    #parameters['msisdn'] = '330794671'
    parameters['transactionId'] = '020908251026200002'
    parameters['externalData1'] = 'Data Unlimited'
    parameters['externalData2'] =  'oneoff'
    parameters['price'] = 0
    parameters['refill_id'] = 'MB78'
    parameters['transactionAmount'] = '199000'
    parameters['offer_id'] = 13
    parameters['threshold_value'] = '209715200'
    parameters['ut_id']  = 1024
    parameters['uc_id']  = 1024
    parameters['service_class']  = 508
#    parameters['adjustmentAmount']  = '10485760'
#    parameters['dedicatedAccountId']  = 1115
#    parameters['daAction']  = 'adjustmentAmountRelative'
#    parameters['start_date']  = datetime.now() #+ timedelta(weeks =110)
#    parameters['end_date']  = datetime.now() + timedelta(weeks =2)
#
#
    resources['parameters'] = parameters
    #print get_sub_balance(resources)
    #print get_balance_and_date(resources)
    #print bill_subscriber(resources)
    #print get_offers(resources)
    #print refill(resources)
    #print set_service_class(resources)
    #print getUsageThresholdsAndCounters(resources)
    #print updateUsageThresholdsAndCounters(resources)
    #print update_da_account(resources)
    print get_offers(resources)
    #print delete_offers(resources)
    #print set_value_offer_id(resources)
    #print set_offer_id(resources)
 
