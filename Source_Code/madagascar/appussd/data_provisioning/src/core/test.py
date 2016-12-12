def test_provisionPackage():
    from data_provisioning.src.core.core import processRequest
    resources = setup()
    parameters = {}
    parameters['msisdn'] = '254734091540'
    parameters['transactionId'] = '11'
    parameters['packageId'] = '12'
    resources['parameters'] = parameters
    resources = processRequest(resources)
    parameters = resources['parameters']
    print parameters
    print 'new volume: %s MB' %str(int(parameters['volume']/1024))
    print 'expiry: %s' %str(parameters['expiry'])
    print 'package name %s' %str(parameters['packageName'])

def test_billSubscriber():
    from billing_.UCIP.core import updateBalanceAndDate
    resources = setup()
    parameters = {}
    parameters['msisdn'] = '254735267974'
    parameters['transactionId'] = '11'
    parameters['packageId'] = '12'
    parameters['cost'] = '200'
    resources['parameters'] = parameters
    return updateBalanceAndDate(resources)

def test_setup():
    from server_data_provisioning import setup
    setup('test')

def setup():
    from cx_Oracle import SessionPool
    from sapc.src.common.core import createSAPCConnection
    resources = {'connection':SessionPool('pavp','pavp654','172.23.0.159:1524/fnr',10,50,5,threaded=True)}
    resources['ldap'] = createSAPCConnection(resources)
    return resources
    
if __name__ == '__main__':
    test_setup()
    #test_provisionPackage()
    #test_billSubscriber()

