#!/usr/bin/env python
from twisted.web import resource, server
from twisted.internet import reactor, threads
from utilities.logging.core import log
from data_provisioning.src.configs.core import country_code, msisdn_length
import traceback

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


RES = setup()

class AuthenticationFailureException(Exception):
    '''this exception is raised when the request submitted has an invalid authentication key'''
    def __init__(self,resources):
        from data_provisioning.src.configs.core import status
        request = resources['request']
        statusCode = status['authenticationFailed']
        error = 'invalid credentials'
        self.value = error
        request = resources['request']
        request.setHeader('Status-Code',statusCode)
        request.setHeader('Status-Msg',error)
        request.write(error)
        request.finish()

    def __str__(self):
        return repr(self.value)

class MissingParametersException(Exception):
    '''this exception is raised when the request submitted is missing mandatory parameters'''
    def __init__(self,resources):
        from data_provisioning.src.configs.core import status
        statusCode = status['missingParameters']
        error = 'missing mandatory parameter'
        self.value = error
        request = resources['request']
        request.setHeader('Status-Code',statusCode)
        request.setHeader('Status-Msg',error)
        request.write(error)
        request.finish()

    def __str__(self):
        return repr(self.value)

class InvalidPackageIdException(Exception):
    '''this exception is raised when the request submits an unauthorized packageId'''
    def __init__(self,resources):
        from data_provisioning.src.configs.core import status
        statusCode = status['invalidPackageId']
        error = 'invalid package requested'
        self.value = error
        request = resources['request']
        request.setHeader('Status-Code',statusCode)
        request.setHeader('Status-Msg',error)
        request.write(error)
        request.finish()

    def __str__(self):
        return repr(self.value)


def get_params(request):
    params = {}
    for k,v in request.args.items():
        params[k] = v[0]
    return params

def isAuthenticated(func):
    '''this method authenticates the user submitting the request'''
    def __inner(resources):
        from  utilities.secure.core import encrypt
        from data_provisioning.src.common.db.core import getConnection
        import traceback
        parameters = resources['parameters']
        userId = 'unknown'
        requestId = 'unknown'
        try:
            userId = parameters['accountId']
            password = parameters['authKey']
            requestId = parameters['requestId']
            sql = 'select allowed_package_ids from user_profiles where name = :userId and password=:password'
            cursor = (getConnection(resources)).cursor()
            params = {'password':encrypt(password),'userId':userId}
            cursor.execute(sql,params)
            results = cursor.fetchone()
            count = cursor.rowcount
            cursor.close()
            if cursor.rowcount == 0:
                raise AuthenticationFailureException(resources)
            else:
                parameters['allowedPackages'] = (results[0]).split(',')
                resources['parameters'] = parameters
        except KeyError,e:
            raise MissingParametersException(resources)
        except Exception,e:
            error = 'operation:isAuthenticated,desc:failed to authenticate for account-id:%s request-id:%s,error:%s' %(str(userId),str(requestId),str(e),)
            print error
            print traceback.format_exc()
            try:
                cursor.close()
            except:
                pass
            raise e
        else:
            try:
                func(resources)
            except Exception,e:
                print e
                raise e
    return __inner



def debug(text):
    from data_provisioning.src.config import debug
    if debug:
        print text


def sendResponse(request):
    request.setHeader('response','done')
    request.write('done')
    request.finish()

@isAuthenticated
def submitProvision(resources):
    from core import createRequest
    import traceback
    parameters = resources['parameters']
    if not parameters.has_key('packageId'):
        raise MissingParametersException(resources)
    if not parameters.has_key('msisdn'):
        raise MissingParametersException(resources)
    else:
        parameters['msisdn'] = '%s%s' %(country_code, parameters['msisdn'][-msisdn_length:])
        resources['parameters'] = parameters
        if parameters['allowedPackages'].__contains__(str(parameters['packageId']).strip()):
            try:
                transactionId = createRequest(resources)
            except Exception,e:
                error = 'operation:submitProvisionFailed,desc: failed to provision %s' %str(e)
                print error
                print traceback.format_exc()
            else:
                from data_provisioning.src.configs.core import status
                parameters = resources['parameters']
                requestId = parameters['requestId']
                statusMsg = 'queued'
                try:
                    request = resources['request']
                    request.setHeader('Status-Code',str(status['queued']))
                    request.setHeader('Status-Msg',str(statusMsg))
                    request.setHeader('Request-Id',str(requestId))
                    request.setHeader('Transaction-Id',str(transactionId))
                    request.write(statusMsg)
                    request.finish()
                except Exception, err:
                    log(resources, str(err), 'error')
                    print traceback.format_exc()
        else:
            raise InvalidPackageIdException(resources)



@isAuthenticated
def retrieveProvision(resources):
    from data_provisioning.src.configs.core import statusMsgs
    from core import retrieveProvisionResponse
    parameters = resources['parameters']
    if not parameters.has_key('transactionId'):
        raise MissingParametersException(resources)
    transactionId = parameters['transactionId']
    requestId = parameters['requestId']
    response = retrieveProvisionResponse(resources)
    print response
    statusCode = response['statusCode']
    statusMsg = statusMsgs[str(statusCode)]
    request = resources['request'] 
    request.setHeader('Status-Code',str(statusCode))
    request.setHeader('Status-Msg',str(statusMsg))
    request.setHeader('Request-Id',str(requestId))
    request.setHeader('Transaction-Id',str(transactionId))
    if response.has_key('name'):
        name = response['name']
        request.setHeader('Name',str(name))
    if response.has_key('expiry'):
        expiry = response['expiry']
        request.setHeader('Expiry',str(expiry))
    if response.has_key('volume'):
        volume = response['volume']
        request.setHeader('Volume',str(volume))
    request.write(statusMsg)
    request.finish()

@isAuthenticated
def retrieveProvisionByRequestId(resources):
    from data_provisioning.src.configs.core import statusMsgs
    from core import retrieve_provision_response_request_id
    parameters = resources['parameters']
    if not parameters.has_key('requestId'):
        raise MissingParametersException(resources)
    requestId = parameters['requestId']
    try:
        response = retrieve_provision_response_request_id(resources)
    except InvalidRequestIdException, err:
        msg = 'invalid request_id %s' %str(parameters['requestId'])
        log(resources, msg, 'error')
    except Exception, err:
        log(resources, str(err), 'error')
    statusCode = response['statusCode']
    statusMsg = statusMsgs[str(statusCode)]
    request = resources['request'] 
    request.setHeader('Status-Code',str(statusCode))
    request.setHeader('Status-Msg',str(statusMsg))
    request.setHeader('Request-Id',str(requestId))
    if response.has_key('name'):
        name = response['name']
        request.setHeader('Name',str(name))
    if response.has_key('expiry'):
        expiry = response['expiry']
        request.setHeader('Expiry',str(expiry))
    if response.has_key('volume'):
        volume = response['volume']
        request.setHeader('Volume',str(volume))
    request.write(statusMsg)
    request.finish()

@isAuthenticated
def submitBalanceCheck(resources):
    from core import createRequest
    import traceback
    parameters = resources['parameters']
    if not parameters.has_key('msisdn'):
        raise MissingParametersException(resources)
    parameters['msisdn'] = '%s%s' %(country_code, parameters['msisdn'][-msisdn_length:])
    resources['parameters'] = parameters
    resources['parameters']['packageId'] = '0'
    try:
        transactionId = createRequest(resources)
    except Exception,e:
        error = 'operation:submitBalanceRequestFailed,desc: failed to submit balance check request,error:%s' %(str(e),)
        print error
        print traceback.format_exc()
    else:
        from data_provisioning.src.configs.core import status
        parameters = resources['parameters']
        requestId = parameters['requestId']
        statusMsg = 'queued'
        request = resources['request']
        request.setHeader('Status-Code',str(status['queued']))
        request.setHeader('Status-Msg',str(statusMsg))
        request.setHeader('Request-Id',str(requestId))
        request.setHeader('Transaction-Id',str(transactionId))
        request.write(statusMsg)
        request.finish()


@isAuthenticated
def retrieveBalance(resources):
    from data_provisioning.src.configs.core import statusMsgs
    from core import retrieveBalanceResponse
    parameters = resources['parameters']
    print resources
    if not parameters.has_key('transactionId'):
        raise MissingParametersException(resources)
    transactionId = parameters['transactionId']
    requestId = parameters['requestId']
    response = retrieveBalanceResponse(resources)
    statusCode = response['statusCode']
    msg = response['response']
    statusMsg = statusMsgs[str(statusCode)]
    request = resources['request'] 
    request.setHeader('Status-Code',str(statusCode))
    request.setHeader('Status-Msg',str(statusMsg))
    request.setHeader('Transaction-Id',str(transactionId))
    request.setHeader('Request-Id',str(requestId))
    request.setHeader('balance',str(msg))
    request.write(statusMsg)
    request.finish()


class SubmitProvision(resource.Resource):
    '''class for handling new provisioning request submissions'''
    def __init__(self):
        resource.Resource.__init__(self)
        self.resources = RES

    def render_POST(self, request):
        resources = {}
        resources['connections'] = self.resources['connections']
        resources['request'] = request

        parameters = get_params(request)
        print parameters

        if not parameters.has_key('transaction_type'):
            parameters['transaction_type'] = 'a'

        if not parameters.has_key('b_msisdn'):
            parameters['b_msisdn'] = parameters['msisdn']

        if not parameters.has_key('channel'):
            parameters['channel'] = 'ussd'

        if not parameters.has_key('args'):
            args = {}
            if parameters['packageId'] in ['1','60','179']:
                args['routing_key'] = 'meg_fiftn'
            else:
                args['routing_key'] = 'mg_data'
            args = str(args)
            parameters['args'] = args


        resources['parameters'] = parameters
        request_id = parameters['requestId']
        msisdn = parameters['msisdn']
        account_id = parameters['accountId']
        try:
            d = threads.deferToThread(submitProvision, resources)
            return server.NOT_DONE_YET
        except Exception, err:
            error = ('operation: submitProvision, error: failed to submit'+
                    ' provisioning request,'+
                    'desc: %s %s %s' %(account_id, request_id, msisdn))
            log(resources, error, 'error')
            log(resources, traceback.format_exc(), 'error')

    def render_GET(self, request):
        return server.UnsupportedMethod

class RetrieveProvision(resource.Resource):
    '''class for handling new provisioning request retrievals'''
    def __init__(self):
        resource.Resource.__init__(self)
        self.resources = RES

    def render_POST(self, request):
        resources = {}
        resources['connections'] = self.resources['connections']
        resources['request'] = request

        parameters = get_params(request)
        resources['parameters'] = parameters
        transaction_id = parameters['transactionId']
        request_id = parameters['requestId']
        account_id = parameters['accountId']
        try:
            d = threads.deferToThread(retrieveProvision, resources)
            return server.NOT_DONE_YET
        except Exception, err:
            error = ('operation: retrieveProvision, error: failed to retrieve'+
                    ' provisioning request,'+
                    'desc: %s %s %s' %(account_id, transaction_id, request_id))
            log(resources, error, 'error')
            log(resources, traceback.format_exc(), 'error')

    def render_GET(self, request):
        return server.UnsupportedMethod

class SubmitBalance(resource.Resource):
    '''class for handling new balance request submissions'''
    def __init__(self):
        resource.Resource.__init__(self)
        self.resources = RES

    def render_POST(self, request):
        resources = {}
        resources['connections'] = self.resources['connections']
        resources['request'] = request

        parameters = get_params(request)
        
        if not parameters.has_key('transaction_type'):
            parameters['transaction_type'] = 'a'

        if not parameters.has_key('b_msisdn'):
            parameters['b_msisdn'] = parameters['msisdn']

        if not parameters.has_key('channel'):
            parameters['channel'] = 'ussd'

        if not parameters.has_key('args'):
            args = {}
            args['routing_key'] = 'mg_data'
            args['is_night'] = False
            args['can_renew'] = '0'
            args = str(args)
            parameters['args'] = args

 
        resources['parameters'] = parameters
        request_id = parameters['requestId']
        msisdn = parameters['msisdn']
        account_id = parameters['accountId']
        try:
            d = threads.deferToThread(submitBalanceCheck, resources)
            return server.NOT_DONE_YET
        except Exception, err:
            error = ('operation: submitBalanceCheck, error: failed to submit'+
                    ' provisioning request,'+
                    'desc: %s %s %s' %(account_id, request_id, msisdn))
            log(resources, error, 'error')
            log(resources, traceback.format_exc(), 'error')

    def render_GET(self, request):
        return server.UnsupportedMethod

class RetrieveBalance(resource.Resource):
    '''class for handling balance request retrievals'''
    def __init__(self):
        resource.Resource.__init__(self)
        self.resources = RES

    def render_POST(self, request):
        resources = {}
        resources['connections'] = self.resources['connections']
        resources['request'] = request

        parameters = get_params(request)
        resources['parameters'] = parameters
        transaction_id = parameters['transactionId']
        request_id = parameters['requestId']
        account_id = parameters['accountId']
        try:
            d = threads.deferToThread(retrieveBalance, resources)
            return server.NOT_DONE_YET
        except Exception, err:
            error = ('operation: retrieveProvision, error: failed to retrieve'+
                    ' balance check request,'+
                    'desc: %s %s %s' %(account_id, transaction_id, request_id))
            log(resources, error, 'error')
            log(resources, traceback.format_exc(), 'error')

    def render_GET(self, request):
        return server.UnsupportedMethod

class RetrieveRequest(resource.Resource):
    '''class for handling provisioning request retrievals based on request_id'''
    def __init__(self):
        resource.Resource.__init__(self)
        self.resources = RES

    def render_POST(self, request):
        resources = {}
        resources['connections'] = self.resources['connections']
        resources['request'] = request

        parameters = get_params(request)
        resources['parameters'] = parameters
        request_id = parameters['requestId']
        account_id = parameters['accountId']
        try:
            d = threads.deferToThread(retrieveProvisionByRequestId, resources)
            return server.NOT_DONE_YET
        except Exception, err:
            error = ('operation: retrieveProvisionByRequestID, error: failed to retrieve'+
                    ' provision request,'+
                    'desc: %s %s %s' %(account_id, request_id))
            log(resources, error, 'error')
            log(resources, traceback.format_exc(), 'error')

    def render_GET(self, request):
        return server.UnsupportedMethod

class TestService(resource.Resource):
    def __init__(self):
        resource.Resource.__init__(self)
        self.count = 0 #test to see if stuff is beign cached across requests
 
    def getChild(self, path, request):
        """ """
        return self

    def render_GET(self, request):
        print request.__dict__
        print "----------------------------------"
        print self.__dict__
        self.count+=1
        print "count::",self.count
        return "CON: test"

class Factory(resource.Resource):
    def __init__(self):

        resource.Resource.__init__(self)
        #self.putChild('test', TestService())
        self.putChild('submitProvision', SubmitProvision())
        self.putChild('retrieveProvision', RetrieveProvision())
        self.putChild('submitBalance', SubmitBalance())
        self.putChild('retrieveBalance', RetrieveBalance())
        self.putChild('retrieveRequest', RetrieveRequest())
