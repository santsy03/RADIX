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
    import random
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
    
    if 'external_Data1' in parameters:
        params['externalData1'] = parameters['external_Data1']
        log(resources, 'updated externalData1: '+str(params['externalData1']), 'debug')

    if 'external_Data2' in parameters:
        params['externalData2'] = parameters['external_Data2']
        log(resources, 'updated externalData2: '+str(params['externalData2']), 'debug')

    log(resources, 'FINAL PARAMS..'+str(params), 'debug')
    
    host = hosts[random.randint(0,2)]
    #host = hosts[int(params['transactionId'])%2]
    log(resources, 'AIR HOST....'+str(host), 'debug') 
    return (AIRHandler(params, host), host)

def bill_subscriber(resources, transaction_id=''):
    '''
    method for billing a prepaid subscriber
    '''
    airInstance = get_air(resources)
    air = airInstance[0]
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    amount = '-%d' % (int(parameters['price'])*100)
    msisdn = parameters['msisdn']
    transaction_id = str(parameters['transactionId'])
    to_bill = '%s - util.data_ucip.core.bill_sub(). billing %s from %s- AirHost:%s' % (
            str(transaction_id), amount, msisdn, str(airInstance[1]))
    log(resources, to_bill, 'info')
    try:
        return air.updateBalanceAndDate(msisdn, amount)
    except Exception, err:
        bill_error = 'operation: utilities.ucip.core.bill_subscriber() failed. - %s -%s - %s' % (
                str(err), str(msisdn), str(airInstance[1]) )
        log(resources, bill_error, 'error')
        raise err


def set_service_class(resources):
    '''
    set the subscriber's service class
    '''
    airInstance = get_air(resources)
    air = airInstance[0]
    parameters = resources['parameters']
    service_class = parameters['service_class']
    msisdn = parameters['msisdn']
    try:
        log(resources, 'set_service_class: - %s - AirHost:%s' %(str(msisdn), str(airInstance[1])), 'info')
        return air.setServiceClass(msisdn, service_class)
    except Exception, err:
        error = "operation: set_service_class failed. - %s -%s -%s" % (
                str(err), str(msisdn), str(airInstance[1]))
        log(resources, error, 'error')
        raise err

def get_balance_and_date(resources):
    '''
    method for setting an offer_id for a given subscriber
    '''
    airInstance = get_air(resources)
    air = airInstance[0]
    parameters = resources['parameters']
    msisdn = parameters['msisdn']

    start = datetime.now()

    metric = "aapcn.air.getbalanceanddate"
    try:
        resp = air.getBalanceAndDate(msisdn,)
        response_time(metric, start)
        stop = datetime.now()
        duration = str((stop - start).total_seconds())
        log(resources, 'time: get_balance_and_date: %s - %s - AirHost:%s' %(duration, str(msisdn),str(airInstance[1])), 'info')
        return resp
    except Exception, err:
        error = 'operation: get_balance_and_date failed. - %s- %s- %s' %(
                str(err), str(msisdn), str(airInstance[1]))
        log(resources, error, 'error')
        raise err


def set_offer_id(resources):
    '''
    method for setting an offer_id for a given subscriber
    '''
    airInstance = get_air(resources)
    air = airInstance[0]
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    offer_id = parameters['offer_id']
    start_date = parameters['start_date']
    end_date = parameters['end_date']
    airHost = "AirHost:%s" %str(airInstance[1])
    log(resources, 'Update offers' + str([msisdn, offer_id, end_date, start_date, airHost]), 'info')
    try:
        resp = air.updateOffer(msisdn, offer_id, end_date, start_date)
        resp_code = int(resp['responseCode'])
        if resp_code != 0:
            print 'info-%s-Error setting Offer ID %s - Resp code - %s'%(msisdn, str(offer_id),str(resp_code))
        return resp
    except Exception, err:
        error = 'operation: set_offer_id. - %s - %s - %s' % (
                str(err), str(msisdn), str(airInstance[1]))
        log(resources, error, 'error')
        raise err

def set_value_offer_id(resources):
    '''
    method for setting an offer_id for a given subscriber
    '''
    airInstance = get_air(resources)
    air = airInstance[0]
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    offer_id = parameters['offer_id']
    start_date = parameters['start_date']
    end_date = parameters['end_date']
    airHost = "AirHost:%s" %str(airInstance[1])
    log(resources, 'Update offers' + str([msisdn, offer_id, end_date, start_date, airHost]), 'info')
    try:
        resp = air.updateValueOffer(msisdn, offer_id, end_date, start_date)
        resp_code = int(resp['responseCode'])
        if resp_code != 0:
            print 'info-%s-Error setting Offer ID %s - Resp code - %s'%(msisdn, str(offer_id),str(resp_code))
        return resp
    except Exception, e:
        error = 'operation: set_value_offer_id. - %s - %s - %s' % (
                str(err), str(msisdn), str(airInstance[1]))
        log(resources, error, 'error')
        raise err
 
def get_accumulators(resources):
    '''
    method for retrieving accumulators for the given subscriber
    '''
    airInstance = get_air(resources)
    air = airInstance[0]
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    try:
        log(resources, 'get_accumulators: - %s - AirHost:%s'% (str(msisdn), str(airInstance[1])), 'info')
        return air.getAccumulators(msisdn)
    except Exception, err:
        error = 'operation: get_accumulators- failed:- %s -%s -%s' %(
                str(err), str(msisdn), str(airInstance[1]))
        log(resources, error, 'error')
        raise err

def get_offers(resources):
    '''
    method for retrieving currently provisioned offers
    '''
    airInstance = get_air(resources)
    air = airInstance[0]
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    start = datetime.now()
    metric = "aapcn.air.getoffers"
    try:
        resp = air.getOffers(msisdn)
        response_time(metric, start)
        stop = datetime.now()
        duration = str((stop - start).total_seconds())
        log(resources, 'time: get_offers: %s - %s - AirHost%s' % (duration, str(msisdn), airInstance[1]), 'info')
        return resp
    except Exception, err:
        error = 'operation:get_offers failed:- %s - %s - %s' % (
                str(err), str(msisdn), str(airInstance[1]))
        log(resources, error, 'error')
        raise err

def delete_offers(resources):
    '''
    method for deleting offer ids
    '''
    airInstance = get_air(resources)
    air = airInstance[0]
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    offer_id = parameters['offer_id']
    try:
        log(resources, 'delete_offers: - %s - AirHost:%s' %(str(msisdn), str(airInstance[1])), 'info')
        return air.deleteOffer(msisdn, offer_id)
    except Exception, err:
        error = 'operation:delete_offers - failed: -%s - %s - %s'% (
                str(err), str(msisdn), str(airInstance[1]))
        log(resources, error, 'error')
        raise err

def update_da_account(resources, data_unit = 6):
    '''
    method to update dedicated account
    '''
    airInstance = get_air(resources)
    air = airInstance[0]
    parameters = resources['parameters']
    amount = parameters['adjustmentAmount']
    msisdn = parameters['msisdn']
    account = parameters['dedicatedAccountId']
    action = parameters['daAction']
    expiry_date = parameters['expiryDate']
    log(resources, 'Update DA' + str([msisdn, amount, action, account, expiry_date]), 'info')
    try:
        resp = air.updateDedicatedAccount(msisdn, amount, action, account, expiry_date, data_unit)
        resp_code = int(resp['responseCode'])
        log(resources, 'update_da_account: - %s - AirHost:%s' %(str(msisdn), str(airInstance[1])), 'info')
        if resp_code != 0:
            print 'info-%s-Error updating DA %s, Amount %s, Resp code - %s'%(msisdn, str(account), str(amount), str(resp_code))
        return resp
    except Exception, err:
        error = 'operation:update_da_account - failed: -%s - %s - %s'% (
                str(err), str(msisdn), str(airInstance[1]))
        log(resources, error, 'error')
        raise err

def get_sub_balance(resources, dtype = 'A'):
    '''
    method for getting subscriber balance for self and B_party
    '''
    airInstance = get_air(resources)
    air = airInstance[0]
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    if dtype == 'B':
        msisdn = parameters['b_msisdn']
    try:
        log(resources, 'get_sub_balance: %s- AirHost:%s' %(str(msisdn), str(airInstance[1])), 'info')
        return air.getBalanceAndDate(msisdn,)
    except Exception, err:
        error = 'operation:get_sub_balance - failed: -%s - %s - %s'% (
                str(err), str(msisdn), str(airInstance[1]))
        log(resources, error, 'error')
        raise err 

def refill(resources):
    '''
    method for doing data refills
    '''
    airInstance = get_air(resources)
    air = airInstance[0]
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    refill_id = parameters['refill_id']
    amount = parameters['transactionAmount']

    start = datetime.now()
    metric = "aapcn.air.refills"
    log(resources, 'Refilling ' + str([msisdn,refill_id,amount]), 'info')
    try:
        resp =  air.Refill(msisdn, refill_id, amount)
        response_time(metric, start)
        stop = datetime.now()
        duration = str((stop - start).total_seconds())
        log(resources, 'time: refill: %s - %s - AirHost:%s' % (duration, str(msisdn), airInstance[1]), 'info')
        return resp
    except Exception, err:
        error = 'operation:refill - failed: -%s - %s - %s'% (
                str(err), str(msisdn), str(airInstance[1]))
        log(resources, error, 'error')
        raise err

def updateUsageThresholdsAndCounters(resources):
    '''
    method for updating usage counters and thresholds for data
    '''
    airInstance = get_air(resources)
    air = airInstance[0]
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    uc  = parameters['uc_id']
    ut  = parameters['ut_id']
    thresh_value = parameters['threshold_value']
    start = datetime.now()
    metric = "aapcn.air.updateusagethreshholdandcounters"
    log(resources, 'Update Threshold ' + str([msisdn,uc, ut,thresh_value]), 'info')
    try:
        resp = air.updateUsageThresholdsAndCounters(msisdn, uc, ut, thresh_value)
        response_time(metric, start)
        stop = datetime.now()
        duration = str((stop - start).total_seconds())
        log(resources, 'time: update uc_ut: %s - %s - AirHost:%s' % (duration, str(msisdn), str(airInstance[1])), 'info')
        return resp
    except Exception, err:
        error = 'operation:updateUsageThresholdsAndCounters - failed: -%s - %s - %s'% (
                str(err), str(msisdn), str(airInstance[1]))
        log(resources, error, 'error')
        raise err

def getUsageThresholdsAndCounters(resources):
    '''
    method for getting the usage threshold and counters
    '''
    airInstance = get_air(resources)
    air = airInstance[0]
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    start = datetime.now()
    metric = "aapcn.air.getusagethreshholdandcounters"
    try:
        resp = air.GetUsageThresholdsAndCounters(msisdn)
        response_time(metric, start)
        stop = datetime.now()
        duration = str((stop - start).total_seconds())
        log(resources, 'time: get_uc_ut: %s - %s - AirHost:%s' % (duration, str(msisdn), airInstance[1]), 'info')
        return resp
    except Exception, err:
        error = 'operation:getUsageThresholdsAndCounters - failed: -%s - %s - %s'% (
                str(err), str(msisdn), str(airInstance[1]))
        log(resources, error, 'error')
        raise err

if __name__ == '__main__':
    from datetime import datetime, timedelta
    resources = {}
    parameters = {}
    #parameters['msisdn'] = '261330998255'
    parameters['msisdn'] = '261330722156'
    #parameters['offer_id'] = 1212
    #parameters['msisdn'] = '261331432473'
    #parameters['msisdn'] = '338598731'
    #parameters['msisdn'] = '330798574'
    #parameters['msisdn'] = '261330798574'
    #parameters['msisdn'] = '330798574'
    #parameters['msisdn'] = '330794671'
    parameters['transactionId'] = '020908251026200001'
    parameters['externalData1'] = 'Test'
    parameters['externalData2'] =  'Test'
    parameters['price'] = 0
    parameters['refill_id'] = 'OT1'
    parameters['transactionAmount'] = '0'
    parameters['offer_id'] = 901
    parameters['threshold_value'] = '31457280'
    parameters['ut_id']  = 902
    parameters['uc_id']  = 902
    parameters['service_class']  = 508
    parameters['adjustmentAmount']  = '31457280'
    parameters['dedicatedAccountId']  = 901
    parameters['daAction']  = 'adjustmentAmountRelative'
    parameters['start_date']  = datetime.now() #+ timedelta(weeks =110)
    parameters['end_date']  = datetime.now() + timedelta(weeks =2)
    parameters['expiryDate'] = datetime.now() + timedelta(weeks =2)


    resources['parameters'] = parameters
    #print get_sub_balance(resources)
    print get_balance_and_date(resources)
    #print bill_subscriber(resources)
    #print get_offers(resources)
    #print refill(resources)
    #print set_service_class(resources)
    #print getUsageThresholdsAndCounters(resources)
    #print updateUsageThresholdsAndCounters(resources)
    #print update_da_account(resources, data_unit = 1)
    #print get_offers(resources)
    #print delete_offers(resources)
    #print set_value_offer_id(resources)
    #print set_offer_id(resources)
 
