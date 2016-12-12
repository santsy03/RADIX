#!/usr/bin/env python2.7
from time import sleep
import socket
from xmlrpclib import ServerProxy,Error
from ussd.metrics.config import dataPlanSubscriptionTemplate,dataPlanSubscriptionTimeTemplate,servicePlanSubscriptionTemplate,servicePlanSubscriptionTimeTemplate
from ussd.metrics.sendmetric import  sendMetric
from ussd.services.prepaid.modular_tarrif.xml_core import getModularTariffStatus
from datetime import datetime

def subscribeDataPlan(resources):
    '''
    subscribes subs to prepaid data services(mymeg) 
    '''
    resources['type'] =  'timer'
    url = 'http://172.25.128.100:80/modular-data3G/process.do?'
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    sessionId = parameters['sessionId']
    key = parameters['key']
    code = parameters['code']
    params = {}
    params['MOBILE_NUMBER'] = msisdn
    params['SESSION_ID'] = sessionId
    params['SERVICE_KEY'] = key #Existing USSD shortcode for service 
    params['SEQUENCE'] = '0'
    params['LANGUAGE'] = 'FRA'
    params['END_OF_SESSION'] = 'FALSE'
    params['USSD_BODY'] = code
    resources['start'] = datetime.now()
    resources['nameSpace'] = dataPlanSubscriptionTimeTemplate.substitute(key=key)

    try:
        server = ServerProxy(url)
        socket.setdefaulttimeout(5)
        response = server.USSD_MESSAGE(params)
        socket.setdefaulttimeout(5)
        sendMetric(resources)
    except Exception, e:
        resources['type'] =  'beat'
        action = 'failure'
        request = 'provision'
        nameSpace = dataPlanSubscriptionTemplate.substitute(package=action,request=request,key=key)
        resources['nameSpace'] = nameSpace
        sendMetric(resources)
        error = 'service:subscribeModularTariffPlan desc: Failed to subscribe for %s with error: %s' %(msisdn,str(e))
        error
    else:
        resources['type'] =  'beat'
        action = 'success'
        request = 'provision'
        nameSpace = dataPlanSubscriptionTemplate.substitute(package=action,request=request,key=key)
        resources['nameSpace'] = nameSpace
        sendMetric(resources)
        msg = response['USSD_BODY']
        
        print "Message from the first url" + str(msg)
        try:
            if  msg != 'null':
                return msg
            else:
                sleep(5)
                resp = getModularTariffStatus(resources)
                return resp
        except Exception,e:
            error = 'operation getServicePlan failed for msisdn %s : error %s'%(str(msisdn),str(e))
            print error

def subscribeServicePlan(resources):
    '''
    subscribes subs to prepaid services Plan
    '''
    from config import urls,responses
    parameters = resources['parameters']
    key = parameters['key']
    url = urls[key]
    msisdn = parameters['msisdn']
    sessionId = parameters['sessionId']
    key = parameters['key']
    code = parameters['code']
    language = parameters['language']
    print 'key :::: %s - code :::: %s'%(str(key),str(code))
    params = {}
    params['MOBILE_NUMBER'] = msisdn
    params['SESSION_ID'] = sessionId
    params['SERVICE_KEY'] = key #Existing USSD shortcode for service 
    params['SEQUENCE'] = '0'
    params['LANGUAGE'] = 'FRA'
    params['END_OF_SESSION'] = 'FALSE'
    params['USSD_BODY'] = code
    resources['type'] =  'timer'
    resources['start'] = datetime.now()
    resources['nameSpace'] = servicePlanSubscriptionTimeTemplate.substitute(key=key)
    try:
        server = ServerProxy(url)
        socket.setdefaulttimeout(5)
        response = server.USSD_MESSAGE(params)
        sendMetric(resources)
    except Exception, e:
        action = 'failure'
        request = 'provision'
        nameSpace = servicePlanSubscriptionTemplate.substitute(package=action,request=request,key=key)
        resources['nameSpace'] = nameSpace
        sendMetric(resources)
        error = 'service:subscribeModularTariffPlan desc: Failed to subscribe for %s with error: %s' %(msisdn,str(e))
        print error
    else:
        action = 'success'
        request = 'provision'
        nameSpace = servicePlanSubscriptionTemplate.substitute(package=action,request=request,key=key)
        resources['nameSpace'] = nameSpace
        sendMetric(resources)
        msg = response['USSD_BODY']
        
        print "Message from the first url" + str(msg)
        if not msg == 'null':
            if str(language) == 'txt-2':
                return msg
            else:
                return responses[language]
        else:
            return 'An error occured while processing subscribeRescuePlan'
def getStatus(resources):
    '''gets the status of the provisioning request sent by the first url'''
    try:
        resp = getModularTariffStatus(resources)
    except Exception,e:
        error = 'operation getStatus failed for msisdn %s : error %s'%(str(msisdn),str(e))
    else:
        return resp

if __name__ == '__main__':
    resources = {'parameters':{'msisdn':'261330465390','key':'100','code':'22','package':'500','sessionId':'99098'}}
    resp =  subscribeDataPlan(resources)
    print resp
