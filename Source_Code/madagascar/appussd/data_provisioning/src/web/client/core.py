class ProvisioningRequestException(Exception):
    def __init__(self,value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def log(resources,msg):
    if resources.has_key('logger'):
        resources['logger'].error(msg)
    else:
        print msg

def provision_package(resources):
    '''
    wrapper with PEP8 compatible function name.
    '''
    return provisionPackage(resources)

def get_balance(resources):
    '''
    retrieves balance for given subscriber
    '''
    from urllib import urlencode
    from urllib2 import Request,urlopen
    from data_provisioning.src.configs.core import web_services_port

    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    packageId = parameters['packageId']
    requestId = parameters['requestId']
    authKey = parameters['authKey']
    accountId = parameters['accountId']
    callBack = str(parameters['callBack'])

    
    data = urlencode({'msisdn':msisdn,'authKey':authKey,'requestId':requestId,'accountId':accountId,'packageId':packageId,'callback':callBack})
    log(resources,str(data))
    try:
        response = (urlopen(Request('http://127.0.0.1:%s/submitBalance' %str(web_services_port),data)))
        log(resources,str(response.info()))
    except Exception,e:
        error = 'operation:submitBalance,desc:failed to submit balance check request,error:%s' %str(e)
        log(resources,msg)
        raise e
    else:
        parameters['Status-Code'] = (response.info()).get('Status-Code')
        if parameters['Status-Code'] == '0':
            parameters['referenceId'] = (response.info()).get('Transaction-Id')
            resources['parameters'] = parameters
            return resources
        else:
            error = (response.info()).get('Status-Msg')
            raise ProvisioningRequestException(error)



def provisionPackage(resources):
    '''passes a provisioning request to the server'''
    from urllib import urlencode
    from urllib2 import Request,urlopen
    from data_provisioning.src.configs.core import web_services_port

    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    packageId = parameters['packageId']
    requestId = parameters['requestId']
    authKey = parameters['authKey']
    accountId = parameters['accountId']
    callBack = str(parameters['callBack'])
    log(resources,parameters)
    if parameters.has_key('check'):
        check = True
        data = urlencode({'msisdn':msisdn,'authKey':authKey,'requestId':requestId,'accountId':accountId,'packageId':packageId,'callback':callBack,'check':check})
    else:
        data = urlencode({'msisdn':msisdn,'authKey':authKey,'requestId':requestId,'accountId':accountId,'packageId':packageId,'callback':callBack})
    log(resources,str(data))
    try:
        response = (urlopen(Request('http://127.0.0.1:%s/submitProvision' %str(web_services_port),data)))
        #print Request('http://127.0.0.1:9002/submitProvision',data)
    except Exception,e:
        error = 'operation:provisionPackage,desc:failed to submit provisioning request,error:%s' %str(e)
        log(resources,error)
        raise e
    else:
        parameters['Status-Code'] = (response.info()).get('Status-Code')
        if parameters['Status-Code'] == '0':
            parameters['referenceId'] = (response.info()).get('Transaction-Id')
            resources['parameters'] = parameters
            return resources
        else:
            error = (response.info()).get('Status-Msg')
            raise ProvisioningRequestException(error)
    

def processResponse(resources):
    '''retrieves the parameters from the headers'''
    print 'yes'
    print request
    request = resources['request']
    #headers = request.getAllHeaders()
    for k,v in request.args.items():
        params[k] = v[0]

    resources['parameters'] = params
    return resources


if __name__ == '__main__':
    resources = {}
    parameters = {}
    parameters['msisdn'] = '254734091540'
    parameters['packageId'] = 1
    parameters['authKey'] = 'account2'
    parameters['transactionId'] = 12
    parameters['accountId'] = 'account2'
    parameters['callBack'] = 'http://127.0.0.1:5500'
    resources['parameters'] = parameters
    print provisionPackage(resources)
