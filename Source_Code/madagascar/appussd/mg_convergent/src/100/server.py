#!/usr/bin/env python2.7

from datetime import datetime

import xmlrpclib
from time import sleep,time
from twisted.web import server,xmlrpc
from twisted.internet import reactor,threads
from twisted.protocols.policies import TimeoutMixin

from mg_data_interface.hxc_proxy.core import get_performance
from mg_data_interface.hxc_proxy.core import getSubscriberType
from mg_data_interface.hxc_proxy.core import getSubscriberLanguage

from cx_Oracle import SessionPool
from configs.config import databases
from utilities.secure.core import decrypt
from utilities.logging.core import log

from mg_data_interface.hxc_proxy.config import error_ussd
from mg_data_interface.hxc_proxy.config import MSISDNS as msisdns
from mg_data_interface.hxc_proxy.config import APPLICATIONS as applications
from mg_data_interface.hxc_proxy.config import WHITELIST

class MenuService(xmlrpc.XMLRPC):
    def __init__(self):
        username = decrypt(databases['core']['username'])
        password = decrypt(databases['core']['password'])
        string = databases['core']['string']
        self.connectionPools = {}
        self.connectionPools['core'] = SessionPool(username,password,string,10,50,5,threaded=True)
        self.allowNone = 1
        self.useDateTime = 1
        self.response = {}
        self.sessions = {}
        self.sessionTimes = {}
        reactor.callInThread(self.sessionManager)
    
    def debugging(self, txt): 
        return {'RESPONSE_CODE':'0','SESSION_ID':'1','SEQUENCE':'1','USSD_BODY':txt,'REQUEST_TYPE':'RESPONSE','END_OF_SESSION':'True'}
    
    def xmlrpc_USSD_MESSAGE(self,params):
        parameters = {}
        parameters['LANGUAGE'] = params['LANGUAGE']
        parameters['MSISDN'] = params['MOBILE_NUMBER']
        parameters['SERVICEKEY'] = params['SERVICE_KEY']
        parameters['ENDOFSESS'] = params['END_OF_SESSION']
        parameters['TRANSACTIONID'] = params['SEQUENCE']
        parameters['SESSIONID'] = params['SESSION_ID']
        if 'USSD_BODY' in params:
            parameters['INPUT'] = params['USSD_BODY']
        else:
            parameters['INPUT'] = '#'
        resources = {'parameters':parameters,'connections':self.connectionPools['core']}
        #resources = {'parameters':parameters} 
        try:
            d = threads.deferToThread(self.processRequest,resources)
            d.addErrback(catchError)
        except Exception,e:
            print str(e)
            return error_ussd
        else:
            return d

    def processRequest(self,resources):
        start_time = datetime.now()
        parameters = self.getSession(resources)
        msisdn = parameters['msisdn']
        if WHITELIST['toggle'] == 'on' and msisdn not in WHITELIST['msisdns']:
            log(resources, '%s -- NOT ON WHITELIST'%msisdn)
            return self.debugging('Desole. You are not allowed to access this service')
        sessionid = parameters['sessionId']
        sequence = parameters['transactionId']
        type = parameters['type']
        try:
            url = applications['114'][type]
            proxy = xmlrpclib.ServerProxy(url)
            response = proxy.handleRequest(parameters)
        except Exception,e:
            error = 'operation:processRequest,desc: failed to invoke %s for %s,error:%s' %(str(type),str(msisdn),str(e),)
            print error
            return self.debugging('error')
        else:
            if response['action'] != 'end':
                action = 'FALSE'
            else:
                action = 'TRUE'
            body = response['ussdResponseString']
            ubody = body 
            resp = {}
            resp['RESPONSE_CODE'] = '0'
            resp['SESSION_ID'] = sessionid
            resp['SEQUENCE'] = '0' 
            resp['USSD_BODY'] = ubody[:165] 
            resp['REQUEST_TYPE'] = 'REQUEST'
            resp['END_OF_SESSION'] = action
            resources['parameters'] = parameters
            get_performance(resources, start_time)
            return resp
    
    def sessionManager(self):
        nextCheck = int(time())
        while(1):
            expiredSessionsTime = str(nextCheck-240)
            if self.sessionTimes.has_key(expiredSessionsTime):
                    for session in self.sessionTimes[expiredSessionsTime]:
                        try:
                            del self.sessions[session]
                        except Exception,e:
                            print 'could not delete session from sessions store - '+str(e)
                        else:
                            print 'session: '+str(session)+' expired'
                    del self.sessionTimes[expiredSessionsTime]
            nextCheck += 1
            sleep(1)

    def getSession(self,resources):
        parameters = resources['parameters']
        log(resources, parameters, 'debug')
        parameters['sessionId'] = parameters['SESSIONID']
        parameters['transactionId'] = parameters['TRANSACTIONID']
        parameters['msisdn'] = parameters['MSISDN']
        if 'INPUT' in parameters:
            parameters['request'] = parameters['INPUT']
        else:
            parameters['request'] = '#'
        sessionId = parameters['sessionId']
        transactionId = parameters['transactionId']
        msisdn = parameters['msisdn']
        request = parameters['request']
        try:
            session = self.sessions[str(sessionId)]
        except KeyError,e:
            session = {}
            session['msisdn'] = msisdn
            session['sessionId'] = sessionId
            session['transactionId'] = sessionId

            resources['parameters']['externalData1'] = ''
            resources['parameters']['externalData2'] = ''
            session['language'] = getSubscriberLanguage(resources)
            session['type'] = getSubscriberType(resources)
            #session['language'] = 'txt-1'#getsubcriberlanguage(resources)
            #session['type'] = 'prepaid'#getsubscribertype(resources)
            self.sessions[str(sessionId)] = session
            sessionTime = str(int(time()))
            if self.sessionTimes.has_key(sessionTime):
                self.sessionTimes[sessionTime].append(sessionId)
            else:
                self.sessionTimes[sessionTime] = [sessionId]
        session['ussdRequestString'] = request
        session['service_key'] = parameters['SERVICEKEY']
        return session

def catchError(e=''):
    resp = {}
    resp['RESPONSE_CODE'] = '0'
    resp['SESSION_ID'] = '1'
    resp['SEQUENCE'] = '1'
    resp['USSD_BODY'] = 'System Error. Please try again later.'
    resp['REQUEST_TYPE'] = 'RESPONSE'
    resp['END_OF_SESSION'] = 'TRUE'
    return resp
