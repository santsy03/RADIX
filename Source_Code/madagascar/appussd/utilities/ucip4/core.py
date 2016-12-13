'''core methods for accessing ucip functionality'''
from utilities.logging.core import log

def get_air(resources):
    '''
    method for creating a standard air object
    '''
    from utilities.ucip4.airHandler import AIRHandler
    parameters = resources['parameters']
    params = {}
    params['transactionId'] = str(parameters['transactionId'])
    params['externalData1'] = '%s' % str(parameters['externalData1'])
    params['externalData2'] = '%s' % str(parameters['externalData2'])
    #log(resources, str(params), 'debug')
    return AIRHandler(params)

def bill_subscriber(resources):
    '''
    method for billing a prepaid subscriber
    '''
    air = get_air(resources)
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    #amount = '-%d' % (int(parameters['price'])*100)
    amount = '-%d' % (int(parameters['price']))
    msisdn = parameters['msisdn']
    to_bill = 'Billing %s from %s' % (amount, msisdn)
    log(resources, to_bill)
    try:
        return air.updateBalanceAndDate(msisdn, amount)
    except Exception, err:
        bill_error = 'operation: utilities.ucip4.core.bill_subscriber failed %s' % (
                str(err) )
        log(resources, bill_error, 'error')


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
    return air.updateOffer(msisdn, offer_id, end_date, start_date)

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
    return air.getOffers(msisdn)

def get_balance_and_date(resources):
    '''
    method for retrieving currently provisioned offers
    '''
    air = get_air(resources)
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    resp = air.getBalanceAndDate(msisdn)
    #log(resources, str(resp), 'debug')
    return resp


def update_dedicated_account(resources, da_id, da_value, expiry_date):
    '''
    updates the given dedicated account with the given values
    '''
    air = get_air(resources)
    parameters = resources['parameters']
    action = parameters['action']
    msisdn = parameters['msisdn']
    amount = '0'
    resp = air.updateDedicatedAccount(msisdn, amount, action, int(da_id), expiry_date, da_value)
    log(resources, str(resp), 'debug')
    return resp


if __name__ == '__main__':
    from datetime import timedelta
    resources={}
    parameters={}
    #parameters['msisdn'] = '250730626871'
    #parameters['msisdn'] = '250731523716'
    #parameters['msisdn'] = '250730262406'
    #parameters['msisdn'] = '250738960111'
    #their oib testing number
    parameters['msisdn'] = '261337150441'
    parameters['transactionId'] = '111326'
    parameters['service_id'] = "3"
    parameters['packageId'] = "4"
    #parameters['price'] = 300
    parameters['action'] = 'dedicatedAccountValueNew'
    parameters['externalData1'] = 'broadband'
    parameters['externalData2'] = 'testing'
    #parameters['action'] = 'adjustmentAmountRelative'
    resources['parameters'] = parameters
    import pprint
    import datetime
    fancy_printer = pprint.PrettyPrinter(indent=4)
    #fancy_printer.pprint( get_balance_and_date(resources))
    da_id_list = [10,11,12,30,31,32,33,34,41,42]
    #da_id_list = [41,42]
    da_id = 8
    da_value = 0
    expiry_date=datetime.datetime.now()
    #fancy_printer.pprint(bill_subscriber(resources))
    #print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
    #print "setting da...."
    fancy_printer.pprint(update_dedicated_account(resources, da_id, da_value, expiry_date))
    #print "**************************************************************************"
    #print "clearing ALL DAS"
    #for i in da_id_list:
    #  update_dedicated_account(resources, i, da_value, expiry_date)
    #print "ALL DAS CLEARED"
