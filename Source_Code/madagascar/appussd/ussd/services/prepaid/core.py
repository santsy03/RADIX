#!/usr/bin/env python
from twisted.internet import threads,reactor,defer

def processPrepaidTarrifCheck(resources):
    from ussd.services.prepaid.tarrif.core import getServiceClass,setServiceClass
    print 'in prepaid Tariff Check'
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    language = parameters['language']
    operation = parameters['operation']
    if str(operation) == 'get':
        try:
            response = getServiceClass(resources)
        except Exception,e:
            error = 'process:processPrepaidTarrifCheck failed for msisdn %s : error %s'%(str(msisdn),str(e))
        else:
            return response
    elif str(operation) == 'set':
        try:
            response = setServiceClass(resources)
        except Exception,e:
            error = 'process:processPrepaidTarrifCheck failed for msisdn %s : error %s'%(str(msisdn),str(e))
        else:
            return response
   
def processCallMeBackRequest(resources):
    from ussd.services.prepaid.call_me_back.core import sendCMBRequest
    return sendCMBRequest(resources)

def processBlackberryRequest(resources):
    from ussd.services.prepaid.blackberry.core import process_blackberry
    try:
        resp = process_blackberry(resources)

    except Exception, e:
        print traceback.format_exc()

    else:
        return resp

def processPUKRequest(resources):
    from ussd.services.prepaid.puk.core import process_puk
    try:
        resp = process_puk(resources)

    except Exception, e:
        print traceback.format_exc()

    else:
        return resp


def processPrepaidRecharge(resources):
    from ussd.services.prepaid.recharge.core import refill_subscriber_number
    try:
        resp = refill_subscriber_number(resources)

    except Exception, e:
        print traceback.format_exc()

    else:
        return resp

def processBalanceCheckRequest(resources):
    from ussd.services.prepaid.balance.core import segregate_balance
    try:
        resp = segregate_balance(resources)

    except Exception, e:
        print traceback.format_exc()

    else:
        return resp


def processMCAProvisionRequest(resources):
    try:
        from ussd.services.prepaid.missed_call_alert.core import provision
        from ussd.services.prepaid.missed_call_alert.config import responses
	parameters = resources['parameters']
	msisdn = parameters['msisdn']
        language = parameters['language']
        package = parameters['package']
	response = provision(resources)
    except Exception,e:
        error = 'operation:processMCAProvisionRequest,desc:%s-%s,error:%s' %(msisdn,str(package),str(e),)
        print error
        raise e
    else:
        resp = (responses[str(package)])[str(response)][language]
        return resp


def processModularTarrifProvisionRequest(resources):
    '''processes service provision request'''
    from ussd.services.prepaid.modular_tarrif.core import subscribeServicePlan,subscribeDataPlan
    from ussd.services.prepaid.modular_tarrif.config import service_keys
    print 'in modular Tariff'
    msisdn = resources['parameters']['msisdn']
    shortcode = resources['parameters']['shortcode']
    code = shortcode.split('*')
    resources['parameters']['key'] = code[1]
    resources['parameters']['code'] = code[2]
    key = resources['parameters']['key']
    print 'key ::: %s'%(str(key))
    if str(key) in service_keys:
        if resources['parameters'].has_key('recipient'):
            resources['parameters']['code'] = str(code[2])+"*"+str(resources['parameters']['recipient'])
        else:
            resources['parameters']['code'] = code[2]
        print str(resources['parameters']['code'])+ ":::: code"
        try:
            response = subscribeServicePlan(resources)
        except Exception,e:
            error = 'operation:processModularTarrifProvisionRequest,desc:%s,error:%s' %(msisdn,str(e),)
            print error
            raise e
        else:
            return response
    else:
        try:
            response = subscribeDataPlan(resources)
        except Exception,e:
            error = 'operation:processModularTarrifProvisionRequest,desc:%s,error:%s' %(msisdn,str(e),)
            print error
            raise e
        else:
            return response

def processFamilyAndFriendRequest(resources):
    '''processes family and friends requests'''
    from ussd.services.prepaid.family_and_friends.core import processGetFafList,setFaf
    #resources = setup(resources)
    parameters = resources['parameters']
    fafAction = parameters['fafAction']
    msisdn = parameters['msisdn']
    try:
        if fafAction == 'ADD' or fafAction == 'DELETE':
            resources = setFaf(resources)
        else:
            resources = processGetFafList(resources)
    except Exception,e:
        print 'FAF - for msisdn %s -error- %s'%(str(msisdn),str(e))
    else:
        return resources
  

def sendSMS(resources):
    from ussd.configs.core import kannel
    from ussd.services.common.secure.secure import decrypt
    from datetime import datetime

    '''sends the subscriber text messages'''
    import urllib
    text = resources['parameters']['message']
    msisdn = resources['parameters']['msisdn']
    params = urllib.urlencode({'smsc':'ussd2mg','username':decrypt(kannel['username']),'password':decrypt(kannel['password']), 'from': 'Airtel','to':msisdn,'text':text,'charset':'utf-8','coding':'2'})
    url = "http://127.0.0.1:14020/cgi-bin/sendsms?%s" % params
    print url
    now = datetime.now()
    f = urllib.urlopen(url)
    endtime = datetime.now()
    elapsed_time = endtime - now
    print 'Time taken in smsc -%s '%(str(elapsed_time))
    print f.read()



def processRequest(resources):
    resources['connections'] = resources['parameters']['connections']
    parameters = resources['parameters']
    if 'action' not in  parameters:
        return ('Dear customer the service is currently unavailable. '
                'Please try again later or contact customer care. Airtel')
    action = str(parameters['action']).strip()
    msisdn = parameters['msisdn']
    requestId = parameters['sessionId']
    language = parameters['language']
    print "RESOURCES %s"%(str(resources))
    from string import Template
    if action == 'balance':
        return processBalanceCheckRequest(resources)
    elif action == 'recharge':
        return processPrepaidRecharge(resources) 
    elif action == 'tarrif':
        return processPrepaidTarrifCheck(resources)
    elif action == 'fnf':
        from ussd.services.prepaid.family_and_friends.config import response
        language = resources['parameters']['language']
        d = threads.deferToThread(processFamilyAndFriendRequest,resources)
        d.addErrback(catchError)
        return response[language]['confirmationText'] 
    elif action == 'registration':
        return processPrepaidRegistrationStatus(resources)
    elif action == 'cmb':
        return processCallMeBackRequest(resources)
    elif action == 'mca':
        return processMCAProvisionRequest(resources)
    elif action == 'status':
        return processInternetStatusCheckRequest(resources)
    elif action == 'vuka':
        return processVukaProvisionRequest(resources)
    elif action == 'modular':
        print 'processing modular'
        return processModularTarrifProvisionRequest(resources)
    elif action == 'blackberry':
        return processBlackberryRequest(resources) 
    elif action == 'puk':
        return processPUKRequest(resources)
    else:
        return 'error:invalid service request'

def setup(resources):
    from cx_Oracle import SessionPool
    from ussd.configs.core import databases
    from ussd.services.common.secure.secure import decrypt
    try:
	resources['connections'] = SessionPool(decrypt(databases['core']['username']),decrypt(databases['core']['password']),databases['core']['string'],10,200,5,threaded=True)
    except:
	pass
    return resources

def catchError(e=''):
    resp = {}
    resp['ussdResponseString'] = 'System Error. Please try again later.'
    resp['action'] = 'end'
    print "Error %s"%(str(e))
    return resp

if __name__ == '__main__':
    
    #resources = setup()
    #print resources
    resources = {}
    resources['parameters'] = {}
    (resources['parameters'])['receiver'] = '254735096212'
    #(resources['parameters'])['msisdn'] = '2617272618'
    (resources['parameters'])['msisdn'] = '261331005578'
    (resources['parameters'])['recipient'] = '254735449662'
    (resources['parameters'])['language'] = 'txt-1'
    (resources['parameters'])['action'] = 'registration'
    (resources['parameters'])['package'] = 'status'
    (resources['parameters'])['sessionId'] = '11121111876'
    (resources['parameters'])['request'] = '1'
    (resources['parameters'])['points'] = '50'
    (resources['parameters'])['ussd_body'] = '8'
    #print sendSMS(resources)
    print  processBlackberryRequest(resources)
    #print  processBalanceCheckRequest(resources)
    #print processModularTarrifProvisionRequest(resources)
    #print processVukaProvisionRequest(resources)
    #print processBundlesProvisionRequest(resources)
    #print processInternetStatusCheckRequest(resources)
