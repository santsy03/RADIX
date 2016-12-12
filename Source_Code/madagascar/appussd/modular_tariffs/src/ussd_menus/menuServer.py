#!/usr/bin/env python2.7
import cx_Oracle
from twisted.web import server,xmlrpc
from twisted.internet import reactor,threads
from datetime import datetime
from menus import menus
from modular_tariffs.src.configs import MSISDNS as whitelist
from utilities.logging.core import log

class MenuService(xmlrpc.XMLRPC):
    def __init__(self):
        self.allowNone = 1
        self.useDateTime = 1
        self.response = {}
        self.sessions = {}
        self.sessionTimes = {}
        self.connectionPool = {}
        from configs.config import databases
        from utilities.secure.core import decrypt
        core = databases['core']
        username = decrypt(core['username'])
        password = decrypt(core['password'])
        string = core['string']
        self.connectionPool = cx_Oracle.SessionPool(username,password,string,10,200,5,threaded=True)
        reactor.callInThread(self.sessionManager)

    def processRequest(self,params):
        sessionState = self.getSessionState(params)
        log( {}, sessionState, 'debug' )
        try:
            sessionState['sequence'] = sessionState['ussdRequestString']
        except:
            # pass for new sessions - without the key
            pass
        sessionState['ussdRequestString']= params['ussdRequestString']
        try:
            resources = menus[sessionState['currentMenu']]().processAction(sessionState)
            resources = menus[resources['currentMenu']]().start(resources)
            #self.updateSessionState(resources)
            return {'status':resources['status'],'ussdResponseString':resources['ussdResponseString'],'action':resources['action'],'current':resources['currentMenu']}
        except Exception,e:
            log(resources, str(e), 'error')
            return {'ussdResponseString':'Error. Please try again later','action':'end','status':'1'}
        


    def getSessionState(self,params):
        """this function returns the id of the current processing node for the subscriber"""
        from time import time
        #log({}, params, 'debug')
        try:
            sessionState = self.sessions[str(params['sessionId'])]
            (sessionState['parameters'])['ussdRequestString'] = params['ussdRequestString']
            return sessionState
        except KeyError,e:
            sessionState = {}
            sessionState['connections'] = self.connectionPool
            sessionState['sessionId'] = params['sessionId']
            sessionState['currentMenu'] = 'home'
            sessionState['msisdn'] = params['msisdn']
            sessionState['time'] = datetime.now()
            sessionState['ussdResponseString'] = 'error'
            sessionState['action'] = 'end'
            sessionState['parameters'] = params
            self.sessions[str(params['sessionId'])] = sessionState
            sessionTime = str(int(time()))
            if self.sessionTimes.has_key(sessionTime):
                self.sessionTimes[sessionTime].append(params['sessionId'])
            else:
                self.sessionTimes[sessionTime]= [params['sessionId']]
            log({}, sessionState, 'debug')
            return sessionState

    def updateSessionState(self,resources):
           self.sessions[str(resources['sessionId'])] = resources

    def sessionManager(self):
        from time import time,sleep
        nextCheck = int(time())
        while True:
           expiredSessionsTime = str(nextCheck-15)
           if self.sessionTimes.has_key(expiredSessionsTime):
                    for session in self.sessionTimes[expiredSessionsTime]:
                        try:
                            del self.sessions[str(session)]
                        except Exception,e:
                            print 'could not delete session from sessions store - '+str(e)
                        else:
                            print 'session: '+str(session)+' expired'
                    del self.sessionTimes[expiredSessionsTime]
           nextCheck += 1
           sleep(1)

    def xmlrpc_handleRequest(self,params):
        try:
            d = threads.deferToThread(self.processRequest,params)
            d.addErrback(catchError)
        except Exception,e:
            print str(e)
            return 'System Error. Please try again later.'
        else:
            return d

def catchError(e=''):
    resp = {}
    resp['ussdResponseString'] = 'System Error. Please try again later.'
    resp['action'] = 'end'
    return resp
