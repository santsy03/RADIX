#!/usr/bin/env python2.7
from datetime import datetime

from twisted.web import xmlrpc
from twisted.internet import threads

from menus import menus
from utilities.memcache.sessions import SessionManager


class MenuService(xmlrpc.XMLRPC):
    def __init__(self):
        self.allowNone = 1
        self.useDateTime = 1
        self.response = {}
        self.sessions = SessionManager(expiry=240, prefix='CmbUS')
        self.connectionPool = {}

    def processRequest(self,params):
        sessionState = self.getSessionState(params)
        sessionState['ussdRequestString']= params['ussdRequestString']
        try:
            resources = menus[sessionState['currentMenu']]().processAction(sessionState)
            resources = menus[resources['currentMenu']]().start(resources)
            #self.updateSessionState(resources)
            return {'ussdResponseString':resources['ussdResponseString'],'action':resources['action'],'current':resources['currentMenu']}
        except Exception,e:
            print str(e)
            return {'ussdResponseString':'Error. Please try again later','action':'end'}
        


    def getSessionState(self,params):
        """this function returns the id of the current processing node for the subscriber"""
        try:
            sessionState = self.sessions[str(params['sessionId'])]
            (sessionState['parameters'])['ussdRequestString'] = params['ussdRequestString']
            return sessionState
        except KeyError,e:
            sessionState = {}
            sessionState['connections'] = self.connectionPool
            sessionState['sessionId'] = params['sessionId']
            sessionState['currentMenu'] = 'start'
            sessionState['msisdn'] = params['msisdn']
            sessionState['time'] = datetime.now()
            sessionState['ussdResponseString'] = 'error'
            sessionState['action'] = 'end'
            sessionState['parameters'] = params
            self.sessions[str(params['sessionId'])] = sessionState
            return sessionState

    def updateSessionState(self,resources):
           self.sessions[str(resources['sessionId'])] = resources

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
