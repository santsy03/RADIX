#!/usr/bin/env python
from twisted.web import http
from string import Template
from twisted.internet import threads,reactor,defer
from config import debug,errorMsg
import cx_Oracle
from DBUtils.PooledDB import PooledDB

def getParams(request):
    params = {}
    for k,v in request.args.items():
        params[k] = v[0]

    return params

def sendResponse(results,request):
    if debug:
        print 'sendResponse: results - '+str(results)
    request.write(results)
    request.finish()

def processMenu1(request):
    from core import processRequest
    params = getParams(request)
    resources = {}
    resources['request'] = request
    params['connections'] = request.getConnections()
    resources['parameters'] = params
    try:
        response = processRequest(resources)
        success = 'success:%s|%s' %(str(resources['parameters']),str(response),)
        print success
    except Exception,e:
        error = 'failed:%s,error:%s' %(str(resources['parameters']),str(e),)
        print error
        response = errorMsg
    sendResponse(response,request)

class requestHandler(http.Request):
    pages = {'/process':processMenu1}

    def __init__(self,channel,queued):
        http.Request.__init__(self,channel,queued)

    def process(self):
        if self.pages.has_key(self.path):
            handler = self.pages[self.path]
            d = threads.deferToThread(handler,self)
            d.addErrback(catchError)
            return d
        else:
            self.setResponseCode(http.NOT_FOUND)
            self.write('page not found')
            self.finish()

    def getConnections(self):
        return self.channel.getDbConnection()


class requestProtocol(http.HTTPChannel):
    requestFactory = requestHandler

    def getDbConnection(self):
        connections = self.factory.connectionPools
        return connections

class RequestFactory(http.HTTPFactory):
    protocol = requestProtocol
    isLeaf = True

    def __init__(self):
        from ussd.configs.core import databases
        from ussd.services.common.secure.secure import decrypt
        username = decrypt(databases['core']['username'])
        password = decrypt(databases['core']['password'])
        string = databases['core']['string']

        http.HTTPFactory.__init__(self)
        pool = PooledDB(cx_Oracle, maxcached=5, maxconnections=100,
                        user=username, password=password, dsn=string,
                        threaded=True)
        self.connectionPools = pool

def catchError(e=''):
    resp = {}
    resp['ussdResponseString'] = 'System Error. Please try again later.'
    resp['action'] = 'end'
    print "Error %s"%(str(e))
    return resp

