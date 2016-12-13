def test_bill_subscriber():
    '''tests the bill_subscriber function'''
    from utilities.ucip.core import bill_subscriber

    resources = {}
    parameters = {}
    parameters['msisdn'] = '254735267974'
    parameters['transactionId'] = 1
    parameters['externalData1'] = 'test'
    parameters['externalData2'] = 'test'
    parameters['price'] = '1'
    resources['parameters'] = parameters

    resp = bill_subscriber(resources)
    print resp

    
    
def test_get_balance():
    '''tests the get_balance function'''
    from utilities.ucip.core import get_balance

    resources = {}
    parameters = {}
    parameters['msisdn'] = '254735267974'
    parameters['transactionId'] = 1
    parameters['externalData1'] = 'test'
    parameters['externalData2'] = 'test'
    parameters['price'] = '1'
    resources['parameters'] = parameters

    resp = get_balance(resources)
    print resp

if __name__ == '__main__':
    pass
    #test_bill_subscriber()
    #test_get_balance()
