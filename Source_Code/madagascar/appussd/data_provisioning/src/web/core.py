import cx_Oracle
import traceback

class InvalidTransactionIdException(Exception):
    def __init__(self,resources):
        from data_provisioning.src.configs.core import status
        parameters = resources['parameters']
        transactionId = parameters['transactionId']
        requestId = parameters['requestId']
        statusCode = status['invalidTransactionId']
        statusMsg = 'invalid transactionId'
        self.value = statusMsg
        request = resources['request']
        request.setHeader('Status-Code',statusCode)
        request.setHeader('Status-Msg',statusMsg)
        request.setHeader('Transaction-Id',str(transactionId))
        request.setHeader('Request-Id',str(requestId))
        request.write(statusMsg)
        request.finish()

    def __str__(self):
        return repr(self.value)


class InvalidRequestIdException(Exception):
    def __init__(self,resources):
        from data_provisioning.src.configs.core import status
        parameters = resources['parameters']
        requestId = parameters['requestId']
        statusCode = status['invalidRequestId']
        statusMsg = 'invalid requestId'
        self.value = statusMsg
        request = resources['request']
        request.setHeader('Status-Code',statusCode)
        request.setHeader('Status-Msg',statusMsg)
        request.setHeader('Request-Id',str(requestId))
        request.write(statusMsg)
        request.finish()

    def __str__(self):
        return repr(self.value)

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
    if isAuthenticated(resources):
        balance = 'balance'
        parameters['action'] = 'balance_response'
        response = createRequest(resources)
        expiry = 'expiry'
        return {'requestId':requestId,'transactionId':transactionId,'balance':balance,'packageId':response[0][0],'packageDescription':response[0][1],'units':units['mb'],'expiry':expiry,'status':response[0][3]}
    else:
        print debug('authentication failed')


def retrieveBalanceResponse(resources):
    from data_provisioning.src.common.db.core import getConnection
    try:
        parameters = resources['parameters']
        transactionId = parameters['transactionId']
        accountId = parameters['accountId']
        conn = getConnection(resources)
        cursor = conn.cursor()
        sql = 'select status,balance from requests where Id = :transactionId and user_id =:accountId'
        params = {'transactionId':transactionId,'accountId':accountId}
        cursor.execute(sql,params)
        results = cursor.fetchone()
        count = cursor.rowcount
    except Exception,e:
        cursor.close()
        conn.close()
        error = 'operation:retrieveProvisioningResponse,desc: failed to retrieve provisioning response,error:%s' %(str(e),)
        print error
        print traceback.format_exc()
    else:
        cursor.close()
        conn.close()
        if count == 0:
            raise InvalidTransactionIdException(resources)
        else:
            return {'response':results[1],'statusCode':results[0]}

def retrieveProvisionResponse(resources):
    from data_provisioning.src.common.db.core import getConnection
    try:
        parameters = resources['parameters']
        transactionId = parameters['transactionId']
        accountId = parameters['accountId']
        conn = getConnection(resources)
        cursor = conn.cursor()
        sql = 'select status,response from requests where Id = :transactionId and user_id =:accountId'
        params = {'transactionId':transactionId,'accountId':accountId}
        cursor.execute(sql,params)
        results = cursor.fetchone()
        count = cursor.rowcount
    except Exception,e:
        cursor.close()
        conn.close() 
        error = 'operation:retrieveProvisioningResponse,desc: failed to retrieve provisioning response,error:%s' %(str(e),)
        print error
        print traceback.format_exc()
    else:
        cursor.close()
        conn.close()
        if count == 0:
            raise InvalidTransactionIdException(resources)
        else:
            print str(results[1])
            if results[1] != None:
                status,expiry,volume,packageName, transactionId = results[1].split('||')
                if packageName.__contains__('|'):
                    packageName, stuff,junk = packageName.split('|')
                return {'statusCode':results[0],'volume':volume,'expiry':expiry,'name':packageName}
            else:
                return {'statusCode':'0','volume':'False','expiry':'False','name':'False'}

def retrieve_provision_response_request_id(resources):
    '''
    retrieves provisioning details using the request_id as the main key
    '''
    from data_provisioning.src.common.db.core import getConnection
    try:
        parameters = resources['parameters']
        requestId = parameters['requestId']
        accountId = parameters['accountId']
        conn = getConnection(resources)
        cursor = conn.cursor()
        sql = 'select status,response from requests where request_id = :requestId and user_id =:accountId'
        params = {'requestId':int(requestId),'accountId':accountId}
        cursor.execute(sql,params)
        results = cursor.fetchone()
        count = cursor.rowcount
    except Exception,e:
        cursor.close()
        conn.close()
        error = 'operation:retrieveProvisioningResponse,desc: failed to retrieve provisioning response,error:%s' %(str(e),)
        print error
        print traceback.format_exc()
    else:
        cursor.close()
        conn.close()
        if count == 0:
            raise InvalidRequestIdException(resources)
        else:
            print str(results[1])
            if results[1] != None:
                transactionId,status,volume,expiry,packageName = results[1].split('||')
                if packageName.__contains__('|'):
                    packageName, stuff = packageName.split('|')
                return {'statusCode':results[0],'volume':volume,'expiry':expiry,'name':packageName}
            else:
                return {'statusCode':'0','volume':'False','expiry':'False','name':'False'}

def enqueueForProvisioning(resources):
    subscriberType = 'prepaid'
    
    if subscriberType == 'postpaid':
        from data_provisioning.src.core.postpaid.client import DataProvisionClient
    elif subscriberType == 'prepaid':
        from data_provisioning.src.core.client import DataProvisionClient

    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    transactionId = parameters['transactionId']
    packageId = parameters['packageId']
    account = parameters['accountId']
    b_msisdn = parameters['b_msisdn']
    transaction_type = parameters['transaction_type']
    args = parameters['args']

    try:
        callBack = parameters['callBack']
    except KeyError,e:
        callBack = ''

    if parameters.has_key('check'):
        check = True
    else:
        check = False

    msg = {}
    msg['msisdn'] = msisdn
    msg['package_id'] = packageId
    msg['transaction_id'] = transactionId
    msg['b_msisdn'] = b_msisdn
    msg['transaction_type'] = transaction_type
    msg['args'] = parameters['args']
    msg['callBack'] = callBack
    if 'externalData1' in parameters:
        msg['external_Data1'] = parameters['externalData1']
        msg['external_Data1_ThirdParty'] = parameters['externalData1']
    if 'externalData2' in parameters:
        msg['external_Data2'] = parameters['externalData2']
        msg['external_Data2_ThirdParty'] = parameters['externalData2']

    try:
        DataProvisionClient(str(msg))
    except Exception,e:
        print str(e)
        pass

def createRequest(resources):
    '''queues a request in the request table'''
    from data_provisioning.src.common.db.core import getConnection
    import cx_Oracle
    try:
        parameters = resources['parameters']
        conn = getConnection(resources)
        cursor = conn.cursor()
        userId = parameters['accountId'] 
        requestId = parameters['requestId']
        msisdn = parameters['msisdn']
        packageId = parameters['packageId']
        callback = '-'
        channel = parameters['channel']
        b_msisdn = parameters['b_msisdn']
        transaction_type = parameters['transaction_type']
        args = parameters['args']

        if parameters.has_key('callback'):
            callback = parameters['callback']
        status = 0
        transactionId = int(cursor.callfunc('generate_TransactionId',
            cx_Oracle.NUMBER, [userId, int(requestId), msisdn, 
                int(packageId), int(status), str(callback), str(b_msisdn),
                str(transaction_type), str(channel), str(args)]))
        cursor.connection.commit()
    except Exception,e:
        error = 'operation:createRequest,desc: failed to queue request,error:%s' %str(e)
        print error
        cursor.close()
        conn.close()
        print traceback.format_exc()
    else:
        (resources['parameters'])['transactionId'] = str(transactionId)
        cursor.close()
        conn.close()
        try:
            enqueueForProvisioning(resources)
        except Exception:
            pass
        else:
            return int(transactionId)

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
