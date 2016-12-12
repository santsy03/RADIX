#!/usr/bin/env python
from twisted.web import xmlrpc
from twisted.internet import threads
from datetime import datetime
from config import root

from utilities.memcache.sessions import SessionManager

class MenuService(xmlrpc.XMLRPC):
    def __init__(self):
        self.connectionPool = ''
        self.allowNone = 1
        self.useDateTime = 1
        self.response = {}
        self.sessions = SessionManager(expiry=240, prefix='MgdVol')

    def get_root(self, params):
        menuid = self.processShortcut(params)
        if menuid == False:
            menuid = '1-0-0-1'
        return menuid

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
    
    def processShortcut(self,params):
        from config import no_renew_menu, renew_menu, disable_renew_menu, telescopic_menu
        from config import gmg_menu
        from config import b_party_menu
        from config import device_bundles

        msisdn = params['msisdn']
        request = params['ussdRequestString']

        menu_id = False

        request = request.strip()

        request_parts = request.split('*')

        if len(request_parts) == 1:
            menu_id = no_renew_menu
            if request == '43':
                menu_id = gmg_menu
            elif request == '18':
                menu_id = telescopic_menu
            elif request == '25':
                menu_id = device_bundles
        elif len(request_parts) ==2:
            part_two = request_parts[1]
            part_one = request_parts[0]
            
            if part_one == '27':
                menu_id = device_bundles
            elif len(part_two) <= 2:
                if part_two == '1':
                    menu_id = renew_menu
                elif part_two == '2':
                    menu_id = disable_renew_menu
            elif len(part_two) > 2:
                menu_id = b_party_menu

        return menu_id

        

    def processRequest(self,params):
        from config import menus
        resources = self.getSessionState(params)
        resources['ussdRequestString']= params['ussdRequestString']
        print 'Request-%s-%s' %(params['msisdn'],params['ussdRequestString'])
        opt = '0'
        try:
            print resources['currentMenuId']
            mnu = resources['currentMenuId']
            if resources['currentMenuId'] != root or resources['new'] == False:
                resources = (resources['menus'][resources['currentMenuId']]).processAction(resources)
                opt = params['ussdRequestString']
                mnu = resources['currentMenuId']
            if self.processShortcut(params):
                cMenu = self.processShortcut(params)
                mnu = cMenu
            else:
                cMenu = resources['currentMenuId']
            resources = (resources['menus'][cMenu]).start(resources)
            #resources = (resources['menus'][resources['currentMenuId']]).start(resources)
            self.updateSessionState(resources)
            print resources['parameters']
            print 'Response-%s-%s' %(resources['parameters']['msisdn'],resources['ussdResponseString'])
            print 'cdr-%s-menu-%s-opt-%s'%(resources['parameters']['msisdn'],mnu,opt)
            return {'menu':resources['currentMenuId'],'ussdResponseString':resources['ussdResponseString'],'action':resources['action']}
        except Exception,e:
            error = 'menuServer.processRequest,desc:%s,error:%s' %(str(params),str(e),)
            print error
            print 'error-%s-menu-%s-opt-%s-error-%s'%(params['msisdn'],mnu,error)
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
            sessionState['currentMenuId'] = self.get_root(params)
            sessionState['msisdn'] = params['msisdn']
            sessionState['time'] = datetime.now()
            sessionState['ussdResponseString'] = 'System is currently unavailable. Please try again later.'
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
            return sessionState

    def updateSessionState(self,resources):
        resources['new'] = False
        self.sessions[str(resources['sessionId'])] = resources


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
