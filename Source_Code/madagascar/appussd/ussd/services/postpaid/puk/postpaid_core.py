#!/usr/bin/env python
#coding: utf8
def processOutstandingBalanceCheck(resources):
    '''processes outstanding balance request'''
    from ussd.postpaid.core import getSubscriberDetails
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    language = parameters['language']
    try:
        resources = getSubscriberDetails(resources)
    except Exception,e:
        error = 'operation:getSubscriberDetails,desc:could not retrieve balance for subscriber %s,error:%s' %(msisdn,str(e),)
        print error
        raise e
    else:
        current_month_usage = resources['parameters']['current_month_usage']
        credit_limit = resources['parameters']['credit_limit']
        try:
            credit_limit = int(credit_limit)
        except ValueError,e:
            print str(e) + " ::: not an 'int' - changed to a 'float'"
            credit_limit  = float(credit_limit)
        try:
            current_month_usage = int(current_month_usage)
        except ValueError,e:
            print str(e) + "not an 'int' - changed to a 'float'"
            current_month_usage  = float(current_month_usage)
        print str(credit_limit)+ "credit limit" + str(current_month_usage)+ "::: month usage"
        current_balance = credit_limit - current_month_usage
        from string import Template
        from ussd.services.postpaid.balance.config import responses
        response = Template(responses[language])
        print str(response.substitute(current_balance=current_balance,current_month_usage=current_month_usage,credit_limit=credit_limit)) + ":::::: Response"
        return response.substitute(current_balance=current_balance,current_month_usage=current_month_usage,credit_limit=credit_limit)

def processSMSMinutesBalanceCheck(resources):
    '''checks a subscriber's sms and minute balance'''
    from ussd.postpaid.core import getSubscriberDetails
    from string import Template
    from ussd.services.postpaid.sms_minutes_balance.config import responses
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    language = parameters['language']
    try:
        resources = getSubscriberDetails(resources)
    except Exception,e:
        error = 'operation:getSubscriberDetails,desc:could not retrieve usage for subscriber %s,error:%s' %(msisdn,str(e),)
        print error
        raise e
    else:
        try:
            free_minutes = int(resources['parameters']['free_minutes'])
        except ValueError, err:
            print str(err) + "not an 'int' - changed to a 'float'"
            free_minutes  = float(free_minutes)
        free_minutes = free_minutes/60
        total_sms_available = resources['parameters']['total_sms_available']
        gprs_discount_available = resources['parameters']['gprs_discount_available']
        with_gprs_discount = resources['parameters']['with_gprs_discount']
        if int(with_gprs_discount ) == 1:
            response = Template(unlimited_responses[language])
            response = response.substitute(free_minutes=free_minutes,total_sms_available=total_sms_available)
        else:
            response = Template(responses[language])
            response = response.substitute(free_minutes=free_minutes,total_sms_available=total_sms_available,gprs_discount_available=gprs_discount_available)
        print "response ::: %s"%(str(response))
        return response

def processCreditLimitCheck(resources):
    '''checks and returns a subscriber's credit limit'''
    from ussd.postpaid.core import getSubscriberDetails
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    language = parameters['language']
    try:
        resources = getSubscriberDetails(resources)
    except Exception,e:
        error = 'operation:getSubscriberDetails,desc:could not retrieve usage for subscriber %s,error:%s' %(msisdn,str(e),)
        print error
        raise e
    else:
        credit_limit = resources['parameters']['credit_limit']
        from string import Template
        from ussd.services.postpaid.credit_limit.config import responses
        print str(responses[language]) + "language"
        response = Template(responses[language])
        print str(response) + "response"
        return response.substitute(credit_limit=credit_limit)


def processBillAmountRequest(resources):
    '''checks and reverts the subscriber's bill amount'''
    from ussd.postpaid.core import getSubscriberDetails,getLastInvoiceAmount
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    language = parameters['language']
    try:
        resources = getSubscriberDetails(resources)
    except Exception,e:
        error = 'operation:getSubscriberDetails,desc:could not retrieve usage for subscriber %s,error:%s' %(msisdn,str(e),)
        print error
        raise e
    else:
        current_balance = resources['parameters']['current_balance']
        try:
            resources = getLastInvoiceAmount(resources)
        except Exception,e:
            error = "operation:getLastInvoiceAmount failed for msisdn - %s : error:%s"%(str(),str(e))
        else:
            previous_month_bill = resources['parameters']['last_invoice_amount']
            outstanding_balance = resources['parameters']['opening_bal']
            from string import Template
            from ussd.services.postpaid.bill_amount.config import responses
            response = Template(responses[language])
            return response.substitute(previous_month_bill=previous_month_bill,outstanding_balance=outstanding_balance)
    
def processCallMeBackRequest(resources):
    from ussd.services.postpaid.call_me_back.core import sendCMBRequest
    return sendCMBRequest(resources) 


def processIncreaseCreditLimit(resources):
    '''processes increase credit limit request'''
    from ussd.services.postpaid.increase_credit_limit.core import sendEmail
    from ussd.services.postpaid.increase_credit_limit.config import responses
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    text = parameters['amount']
    language = parameters['language']
    print 'text - %s'%(str(text))
    try:
        resources = sendEmail(resources)
    except Exception,e:
        print 'operation: processIncreaseCreditLimit for msisdn %s : error %s'%(str(msisdn),str(e),)
    else:
        if resources['parameters']['email_status']:
            resp = responses[language]['confirmation_text']
        else:
            resp = responses[language]['error']
        return resp

def processPUKRequest(resources):
    '''processes puk requests'''
    from ussd.services.postpaid.puk.core import process_puk
    msisdn = resources['parameters']['msisdn']
    try:
        resp = process_puk(resources)
    except Exception, err:
        error = ("operation:processPUKRequest failed for msisdn: %s" +
            "failed error : %s") % (str(msisdn), str(err))
    else:
        return resp



def sendMessage(msisdn,recipient,message):
    '''sends the call me back message'''
    from urllib import urlopen,urlencode
    recipient = '254%s' %(str(recipient)[-9:],)
    args = urlencode({'to':str(recipient),'from':msisdn,'text':str(message)})
    try:
        resp = urlopen('http://10.10.32.65:13013/cgi-bin/sendsms?username=radix&pass=radix&'+str(args)).read()
    except Exception,e:
        error = 'operation:callMeBack.sendMessage,desc:%s-%s,error:%s' %(str(msisdn),str(recipient),str(e))
        print error
        raise e
    else:
        return resp



def processRequest(resources):
    parameters = resources['parameters']
    action = str(parameters['action']).strip()
    msisdn = parameters['msisdn']
    requestId = parameters['sessionId']
    language = parameters['language']
    from string import Template
    if action == 'outstanding':
        return processOutstandingBalanceCheck(resources)
    elif action == 'vuka':
        pass
    elif action == 'cmb':
        return processCallMeBackRequest(resources)
    elif action == 'mca':
        return processMCAProvisionRequest(resources)
    elif action == 'sms':
        pass
    elif action == 'smsminutesbalance':
        return processSMSMinutesBalanceCheck(resources)
    elif action == 'creditLimitCheck':
        return processCreditLimitCheck(resources)
    elif action == 'increasecreditlimit':
        return processIncreaseCreditLimit(resources)
    elif action == 'billamount':
        return processBillAmountRequest(resources)
    elif action == 'language':
        return processChangeLanguageRequest(resources)
    elif action == 'puk':
        return processPUKRequest(resources)
    else:
        return 'error:invalid service request'

def setup():
    from cx_Oracle import SessionPool
    from ussd.services.common.secure.secure import decrypt
    from ussd.configs.core import databases
    resources = {}
    resources['connections'] = SessionPool(decrypt(databases['core']['username']),decrypt(databases['core']['password']),databases['core']['string'],10,50,5,threaded=True)
    return resources

if __name__ == '__main__':
    pass
    resources = setup()
    resources['parameters'] = {}
    (resources['parameters'])['recipient'] = '254735096212'
    (resources['parameters'])['msisdn'] = '261333766314'
    (resources['parameters'])['language'] = 'txt-1'
    (resources['parameters'])['inputs'] = '1'
    (resources['parameters'])['action'] = 'smsminutesbalance'
    (resources['parameters'])['sessionId'] = '1244'
    print processRequest(resources)
    #print processMobileInternetRequest(resources)
    #print processBundlesProvisionRequest(resources)
    #print processInternetStatusCheckRequest(resources)
    #print processPostpaidBalanceCheck(resources)
    #print processPrepaidTarrifCheck(resources)
    #print processPostpaidRegistrationStatus(resources)
    #print processBlackberryCompleteProvisionRequest(resources)
    #print processBlackberrySocialProvisionRequest(resources)
    #print processBlackberryBISProvisionRequest(resources)
    #print processMCAProvisionRequest(resources)
    #print processPostpaidBalanceCheck(resources)
    #print  processCallMeBackRequest(resources)
    #print processPostpaidUsageCheck(resources)
    #print processPostpaidPlanCheck(resources)
