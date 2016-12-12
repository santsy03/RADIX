def isAuthenticated(resources):
    '''this method authenticates the given userid'''
    parameters['userId'] = 8
    return True

def submitBalanceCheckRequest(resources):
    parameters = resources['parameters']
    requestId = parameters['requestId']
    msisdn = parameters['msisdn']
    authKey = parameters['authKey']
    if isAuthenticated(resources):
        try:
            '''send request for balance'''
            parameters['action'] = 'balance_request'
            transactionId = createRequest(resources)
        except Exception,e:
            error = 'operation:submitBalanceCheckRequest. Failed to send balance check request for %s.RequestId: %s, authKey: %s Error: %s'%(msisdn,requestId,authKey,str(e),)
            print error
            raise e
        else:
            return [requestId,transactionId]
    else:
        print debug('failed authentication')


def submitProvisionRequest(resources):
    from data_provisioning.src.configs.core import status
    parameters = resources['parameters']
    requestId = parameters['requestId']
    msisdn = parameters['msisdn']
    authKey = parameters['authKey']
    packageId = parameters['packageId']
    if isAuthenticated(resources):
        userId = parameters['userId']
        parameters['status'] = status['pending']
        parameters['action'] = 'provision_request'
        transactionId = createRequest(resources)
        print debug('%s | %s | %s'%(msisdn,transactionId,packageId))
        return {'requestId':requestId,'transactionId':transactionId}
    else:
        print debug('authentication failure')


def retrieveBalanceCheckResponse(resources):
    from data_provisioning.src.configs.core import units
    from database import dbHandler
    parameters = resources['parameters']
    requestId = parameters['requestId']
    transactionId = parameters['transactionId']
    authKey = parameters['authKey']
    #callBack = 
    if isAuthenticated(resources):
        balance = 'balance'
        parameters['action'] = 'balance_response'
        response = createRequest(resources)
        expiry = 'expiry'
        return {'requestId':requestId,'transactionId':transactionId,'balance':balance,'packageId':response[0][0],'packageDescription':response[0][1],'units':units['mb'],'expiry':expiry,'status':response[0][3]}
    else:
        print debug('authentication failed')


def retrieveProvisionResponse(resources):
    from database import dbHandler
    from data_provisioning.src.configs.core import units
    parameters = resources['parameters']
    requestId = parameters['requestId']
    transactionId = parameters['transactionId']
    authKey = parameters['authKey']
    #callBack =
    if isAuthenticated(resources):
        parameters['action'] = 'provision_response'
        balance = 'balance'
        expiry = 'expiry'
        units = units['mb']
        response = createRequest(resources)
        return {'requestId':requestId,'transactionId':transactionId,'balance':balance,'packageId':response[0][0],'packageDescription':response[0][1],'units':units,'expiry':expiry,'status':response[0][3]}
    else:
        print debug('authentication failure')

def createRequest(resources):
    from database import dbHandler
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    requestId = parameters['requestId']
    #packageId = parameters['packageId']
    #callBack =
    try:
        action = parameters['action']
        transactionId = dbHandler(resources,action)
    except Exception,e:
        error = 'operation:createRequest. Error: %s'%(str(e),)
        raise e
    else:
        return transactionId


def retrieveRequestStatus(resources):
    from database import dbHandler
    requestId = parameters['requestId']
    status = dbHandler(resources,'request_status')
    return status

def updateRequestStatus(resources):
    requestId = parameters['requestId']
    status = retrieveRequestStatus(resources)
    '''sql to update table with most recent status'''

def retrieveCatalog(resources):
    '''fetch catalog from db table'''
    parameters = resources['parameters']
    response = createRequest(resources)
    catalog = dbHandler(resources,'packages')
    return catalog

def debug(text):
    from data_provisioning.src.configs.core import debug
    if debug:
        print text


if __name__ == '__main__':
    resources = {}
    parameters = {}
    parameters['msisdn'] = '254735449662'
    parameters['requestId'] = '2'
    parameters['authKey'] = '123'
    parameters['transactionId'] = 1
    parameters['packageId'] = 3
    resources['parameters'] = parameters
    #print submitBalanceCheckRequest(resources)
    #print retrieveProvisionResponse(resources)
    #print retrieveBalanceCheckResponse(resources)
    #print submitProvisionRequest(resources)
