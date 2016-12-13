#!/usr/bin/env python2.7
from datetime import datetime
import xmlrpclib

from twisted.internet import threads
from twisted.web import xmlrpc

from cx_Oracle import SessionPool

from ussd.configs.core import databases
from ussd.services.common.secure.secure import decrypt
from utilities.memcache.sessions import SessionManager

from config import errorMsg, applications, debug, msisdns, USE_WHITELIST
from core import getSubscriberLanguage, getSubscriberType


class MenuService(xmlrpc.XMLRPC):
    def __init__(self):
        username = decrypt(databases['core']['username'])
        password = decrypt(databases['core']['password'])
        string = databases['core']['string']
        self.connectionPools = {}
        self.connectionPools['core'] = SessionPool(username,password,string,1,50,5,threaded=True)
        self.allowNone = 1
        self.useDateTime = 1
        self.response = {}
        self.sessions = SessionManager(expiry=240, prefix='UsHxc')
    
    def debugging(self, txt): 
        return {'RESPONSE_CODE':'0','SESSION_ID':'1','SEQUENCE':'1','USSD_BODY':txt,'REQUEST_TYPE':'RESPONSE','END_OF_SESSION':'True'}
    
    def xmlrpc_USSD_MESSAGE(self,params):
        print 'time at the beginning - %s'%(datetime.now())
        print 'Parameters from GW :: %s' % str(params)
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
        try:
            d = threads.deferToThread(self.processRequest,resources)
            d.addErrback(catchError)
        except Exception,e:
            print str(e)
            return errorMsg
        else:
            return d

    def processRequest(self,resources):
        print 'in processRequest'
        from core import get_performance
        import socket
        start_time = datetime.now()
        parameters = self.getSession(resources)
        msisdn = parameters['msisdn']
        sessionid = parameters['sessionId']
        sequence = parameters['transactionId']
        type = parameters['type']
        try:
            if (USE_WHITELIST and msisdn not in msisdns):
                print "not whitelisted"
                return {'USSD_BODY':'UNKNOWN APPLICATION','action':'end'}
            url = applications[type]
            proxy = xmlrpclib.ServerProxy(url)
            # socket.setdefaulttimeout(11)
            response = proxy.handleRequest(parameters)
            print 'time at the end - %s'%(datetime.now())
            print 'response is: %s' %(response)
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
            resp['SESSION_ID'] = sessionid.split('T')[0]
            resp['SEQUENCE'] = '0' 
            resp['USSD_BODY'] = ubody[:165] 
            resp['REQUEST_TYPE'] = 'REQUEST'
            resp['END_OF_SESSION'] = action
            resources['parameters'] = parameters
            get_performance(resources, start_time)
            print "Reponse returned to the subscriber- %s"%(str(resp),)
            return resp

    def getSession(self,resources):
        parameters = resources['parameters']
        msisdn = parameters['MSISDN']
        parameters['sessionId'] = parameters['SESSIONID'] + 'T' + str(msisdn)
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
            session['language'] = getSubscriberLanguage(resources)
            session['type'] = getSubscriberType(resources)
            self.sessions[str(sessionId)] = session
        session['ussdRequestString'] = request
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
