#!/usr/bin/env python
from twisted.web import http
from string import Template
from twisted.internet import threads,reactor,defer
from config import debug
from cx_Oracle import SessionPool

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
    connectionPools = request.getConnections()
    resources['connections'] = connectionPools['core']
    resources['request'] = request
    resources['parameters'] = params
    try:
        response = processRequest(resources)
        success = 'success:%s|%s' %(str(resources['parameters']),str(response),)
        print success
    except Exception,e:
        error = 'failed:%s,error:%s' %(str(resources['parameters']),str(e),)
        print error
        response = 'error'
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

def catchError(e=''):
    resp = {}
    resp['ussdResponseString'] = 'System Error. Please try again later.'
    resp['action'] = 'end'
    print "Error %s"%(str(e))
    return resp

class RequestFactory(http.HTTPFactory):
    protocol = requestProtocol
    isLeaf = True

    def __init__(self):
        http.HTTPFactory.__init__(self)
        from ussd.configs.core import databases
        from ussd.services.common.secure.secure import decrypt
        self.connectionPools = {}
        pool = SessionPool(decrypt(databases['core']['username'])\
                ,decrypt(databases['core']['password']),\
                databases['core']['string'],10,50,5,threaded=True)
        pool.timeout = 300
        self.connectionPools['core'] = pool 
