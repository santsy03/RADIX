#!/usr/bin/env python
# -*- coding: utf8 -*-
import cx_Oracle
from twisted.web import server,xmlrpc
from twisted.internet import reactor,threads
from datetime import datetime
from config import root

class MenuService(xmlrpc.XMLRPC):
    def __init__(self):
        self.connectionPool = ''
        self.allowNone = 1
        self.useDateTime = 1
        self.response = {}
        self.sessions = {}
        self.sessionTimes = {}
        reactor.callInThread(self.sessionManager)

    def getPreviousMenu(self,resources):
        navigation = resources['navigation']
        if len(navigation)>0:
            print resources['navigation']
            if len(navigation)-2 >= 0:
                resources['currentMenuId'] = str(navigation[len(navigation)-2]).strip()
            else:
                resources['currentMenuId'] = root
            resources['navigation'].pop()
            return resources
        else:
            resources['currentMenuId'] = root
            return resources

    def processRequest(self,params):
        from config import menus
        resources = self.getSessionState(params)
        resources['ussdRequestString']= params['ussdRequestString']
        print 'Request-%s-%s' %(params['msisdn'],params['ussdRequestString'])
        if type(resources['ussdRequestString']) == unicode:
            print 'Encoded text entered by subscriber'
            return {'menu':resources['currentMenuId'],'ussdResponseString':"S'il vous plait entrer option valable",'action':resources['action']}
        elif resources['ussdRequestString'] == '':
            print 'Empty String entered by subscriber'
            return {'menu':resources['currentMenuId'],'ussdResponseString':"S'il vous plait entrer option valable",'action':resources['action']}
        opt = '0'
        try:
            mnu = resources['currentMenuId']
            if resources['currentMenuId'] != root or resources['new'] == False:
                resources = (resources['menus'][resources['currentMenuId']]).processAction(resources)
                opt = params['ussdRequestString']
		mnu = resources['currentMenuId']
            resources = (resources['menus'][resources['currentMenuId']]).start(resources)
            print 'cdr-%s-menu-%s-opt-%s'%(params['msisdn'],mnu,opt)
            print 'Response-%s-%s'%(params['msisdn'],repr(resources['ussdResponseString']))
            self.updateSessionState(resources)
            return {'menu':resources['currentMenuId'],'ussdResponseString':resources['ussdResponseString'],'action':resources['action']}
        except Exception,e:
            error = 'menuServer.processRequest,desc:%s,error:%s' %(str(params),str(e),)
            print error
            print 'error-%s-menu-%s-opt-%s-desc-%s'%(params['msisdn'],mnu,opt,error)
            return {'menu':resources['currentMenuId'],'ussdResponseString':'error','action':'end'}
    
    def getSubscriberLanguage(self,msisdn):
        '''returns the language settings for the given msisdn'''
        return '1'

    def getSessionState(self,params):
        """this function returns the id of the current processing node for the subscriber"""
        from time import time
        try:
            sessionState = self.sessions[str(params['sessionId'])]
            return sessionState
        except KeyError,e:
            from config import menus
            sessionState = {}
            sessionState['params'] = params
            sessionState['connections'] = self.connectionPool
            sessionState['sessionId'] = params['sessionId']
            sessionState['currentMenuId'] = root
            sessionState['msisdn'] = params['msisdn']
            sessionState['time'] = datetime.now()
            text = "Le système est actuellement indisponible. Veuillez réessayer plus tard."
            sessionState['ussdResponseString'] = text.decode('utf8')
            sessionState['action'] = 'end'
            sessionState['parameters'] = params
            sessionState['parameters']['service'] = None
            sessionState['parameters']['package'] = None
            sessionState['navigation'] = []
            sessionState['language'] = params['language']
            sessionState['new'] = True
            sessionState['root'] = root
            sessionState['menus'] = menus
            self.sessions[str(params['sessionId'])] = sessionState
            sessionTime = str(int(time()))
            if self.sessionTimes.has_key(sessionTime):
                self.sessionTimes[sessionTime].append(params['sessionId'])
            else:
                self.sessionTimes[sessionTime]= [params['sessionId']]
            return sessionState

    def updateSessionState(self,resources):
        resources['new'] = False
        self.sessions[str(resources['sessionId'])] = resources

    def sessionManager(self):
        from time import time,sleep
        nextCheck = int(time())
        while True:
           expiredSessionsTime = str(nextCheck-240)
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
            return config.system_error
        else:
            return d

def catchError(e=''):
    resp = {}
    resp['ussdResponseString'] = 'System Error. Please try again later.'
    resp['action'] = 'end'
    return resp
