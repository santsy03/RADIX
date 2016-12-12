def setup():
    from cx_Oracle import SessionPool
    from configs.config import databases
    from utilities.secure.core import decrypt
    user = decrypt(databases['core']['username'])
    password = decrypt(databases['core']['password'])
    string = databases['core']['string']

    resources = {'connections':SessionPool(user,password,string,10,50,5,threaded=True)}
    return resources

def test_setup():
    import pprint
    import datetime
    from sacc.src.common.core import get_subscriber_profile,get_dedicated_account_ids,get_dedicated_account_values
    from sacc.src.volume.core import package_category
    fancy_printer = pprint.PrettyPrinter(indent=4)
    resources = setup()
    resources['printer'] = fancy_printer
    parameters={}
    #parameters['msisdn'] = '250738960111'
    parameters['msisdn'] = '250730262406'
    parameters['transactionId'] = '2345789'
    parameters['service_id'] = "3"
    parameters['packageId'] = "4"
    parameters['volumeString'] =1024
    parameters['packageName']= 'daily internet'
    parameters['action'] = 'dedicatedAccountValueNew'
    parameters['expiry'] = datetime.datetime.now()
    parameters['group'] = "30"
    parameters['balanceInfo'] = {}
    parameters['da_details'] = {}
    parameters['volume'] = '1'
    parameters['validity'] =  2
    parameters['externalData1'] = 'broadband'
    parameters['externalData2'] = 'balance'
    parameters['currentBundleDetails'] = {}
    balance={}
    #balance['volume']=10000000
    #parameters['balance'] = balance
    resources['parameters'] = parameters
    #fancy_printer.pprint(set_bundle_details(resources))
    #fancy_printer.pprint(get_subscriber_profile(resources))
    resources = get_subscriber_profile(resources)
    return resources

def test_getBalance():
    from lib_modular.src.offers.core import getBalance
    resources = setup()
    parameters = {}
    parameters['msisdn'] = '261336173681'
    parameters['transactionId'] = '10'
    parameters['externalData1'] = 'broadband'
    parameters['externalData2'] = 'balance'
    resources['parameters'] = parameters
    print getBalance(resources)['parameters']['balance']

def test_provision():
    from lib_modular.src.offers.core import provisionBundle
    from data_provisioning.src.core.core import getPackageDetails
    resources = setup()
    parameters = {}
    parameters['msisdn'] = '261336173681'
    parameters['transactionId'] = '10'
    parameters['packageId'] = '4'
    parameters['externalData1'] = 'broadband'
    parameters['externalData2'] = parameters['packageId']
    resources['parameters'] = parameters
    getPackageDetails(resources)
    provisionBundle(resources)

     
if  __name__=='__main__':
    #test_getBalance()
    #test_check_conflicting_bundles()
    test_provision()
