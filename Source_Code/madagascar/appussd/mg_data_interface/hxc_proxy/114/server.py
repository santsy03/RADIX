#!/usr/bin/env python2.7

from datetime import datetime

import xmlrpclib
from twisted.web import xmlrpc
from twisted.internet import threads

from mg_data_interface.hxc_proxy.core import get_performance
from mg_data_interface.hxc_proxy.core import getSubscriberType
from mg_data_interface.hxc_proxy.core import getSubscriberLanguage

from configs.config import databases
from utilities.secure.core import decrypt
from utilities.logging.core import log
from utilities.memcache.sessions import SessionManager

from mg_data_interface.hxc_proxy.config import error_ussd
from mg_data_interface.hxc_proxy.config import MSISDNS as msisdns
from mg_data_interface.hxc_proxy.config import APPLICATIONS as applications
from mg_data_interface.hxc_proxy.config import WHITELIST
import cx_Oracle
from DBUtils.PooledDB import PooledDB

class MenuService(xmlrpc.XMLRPC):
    def __init__(self):
        username = decrypt(databases['core']['username'])
        password = decrypt(databases['core']['password'])
        string = databases['core']['string']
        self.connectionPools = {}
        self.connectionPools['core'] =PooledDB(
                cx_Oracle,
                maxcached = 5,
                maxconnections = 200,
                user = username,
                password = password,
                dsn = string,
                threaded = True
                )
  
        self.allowNone = 1
        self.useDateTime = 1
        self.response = {}
	self.sessions = SessionManager(expiry=240, prefix='Mgd114Hxc')
    
    def debugging(self, txt): 
        return {'RESPONSE_CODE':'0','SESSION_ID':'1','SEQUENCE':'1','USSD_BODY':txt,'REQUEST_TYPE':'RESPONSE','END_OF_SESSION':'True'}
    
    def xmlrpc_USSD_MESSAGE(self,params):
        parameters = {}
        print 'PARAMS FROM GW:: ' + str(params)
        parameters['LANGUAGE'] = params['LANGUAGE']
        parameters['MSISDN'] = params['MOBILE_NUMBER']
        parameters['SERVICEKEY'] = params['SERVICE_KEY']
        parameters['ENDOFSESS'] = params['END_OF_SESSION']
        parameters['TRANSACTIONID'] = params['SEQUENCE']
        parameters['SESSIONID'] = params['SESSION_ID']
        if 'USSD_BODY' in params and str(params['SEQUENCE']) == '0':
            if len(params['USSD_BODY'].split('*')) == 2:
                b_msisdn = params['USSD_BODY'].split('*')[1]
                package = params['USSD_BODY'].split('*')[0]
                parameters['INPUT'] = '%s||%s' %(package, b_msisdn)
            else:
                parameters['INPUT'] = '*%s#' %params['USSD_BODY'].replace('*', '').replace('#','')
        elif 'USSD_BODY' in params:
            parameters['INPUT'] = params['USSD_BODY']
        else:
            parameters['INPUT'] = '#'
        '''
        if parameters['INPUT'] == '#' or int(params['SEQUENCE']) > 0:
            proxy = xmlrpclib.ServerProxy("http://127.0.0.1:9343/")
            params = {}
            params['msisdn'] = parameters['MSISDN']
            params['sessionId'] = parameters['SESSIONID']
            params['ussdRequestString'] = parameters['INPUT']
            params['language'] = 'txt-2' #HACK!!!!!FIX this later 
            response = proxy.handle_request(params)
            
            if response['action'] != 'end':
                action = 'FALSE'
            else:
                action = 'TRUE'
                print "session ended"

            body = response['ussdResponseString']
            ubody = body
            resp = {}
            resp['RESPONSE_CODE'] = '0'
            resp['SESSION_ID'] = str(params['sessionId']).split('T')[0]
            resp['SEQUENCE'] = '0'
            resp['USSD_BODY'] = ubody[:165]
            resp['REQUEST_TYPE'] = 'REQUEST'
            resp['END_OF_SESSION'] = action
            print "resp returned: %s" % str(resp)
            return resp
        '''

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
            print url
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
                print "session ended"
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
            #print "resp returned: %s-%s" % str(str(params['msisdn']), resp)
            print "resp returned: %s" % str(resp)
            return resp
    
    def getSession(self,resources):
        parameters = resources['parameters']
        log(resources, parameters, 'debug')
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

            resources['parameters']['externalData1'] = ''
            resources['parameters']['externalData2'] = ''
            session['language'] = getSubscriberLanguage(resources)
            session['type'] = getSubscriberType(resources)
            #session['language'] = 'txt-1'#getsubcriberlanguage(resources)
            #session['type'] = 'prepaid'#getsubscribertype(resources)
            self.sessions[str(sessionId)] = session
        session['ussdRequestString'] = request
        session['service_key'] = parameters['SERVICEKEY']
        return session

def catchError(e=''):
    print "ERROR: %r" % e
    resp = {}
    resp['RESPONSE_CODE'] = '0'
    resp['SESSION_ID'] = '1'
    resp['SEQUENCE'] = '1'
    resp['USSD_BODY'] = 'System Error. Please try again later.'
    resp['REQUEST_TYPE'] = 'RESPONSE'
    resp['END_OF_SESSION'] = 'TRUE'
    return resp
