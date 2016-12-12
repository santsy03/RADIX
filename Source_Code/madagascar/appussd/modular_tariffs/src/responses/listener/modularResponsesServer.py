#!/usr/bin/env python

from twisted.web import http
from string import Template
from twisted.internet import threads,reactor,defer
from cx_Oracle import SessionPool
from utilities.logging.core import log

def getParams(request):
    params = {}
    for k,v in request.args.items():
        params[k] = v[0]
	log({}, params)

    return params

def sendResponse(results,request):
    log({}, 'sendResponse: results - '+str(results))
    request.write(results)
    request.finish()

def processResponse(request):
    from core import queue_response
    params = getParams(request)
    resources = {}
    resources['request'] = request
    resources['parameters'] = params
    stuff = str(request).split('/')[2].split(' ')[0]
    parameters = resources['parameters']
    parameters['package_requested'], \
            parameters['modular_id'], \
            parameters['renew'], \
            parameters['da_id'], \
            parameters['channel'] = \
            stuff.split('|')
    resources['parameters'] = parameters
    try:
        response = queue_response(resources)
        success = 'success:%s|%s' %(str(resources['parameters']),str(response),)
        log(resources, success)
    except Exception,e:
        q_error = 'failed:%s,error:%s' %(str(resources['parameters']),str(e),)
        log(resources, q_error, error=True)
        response = 'error'
    sendResponse(response,request)

class requestHandler(http.Request):
    pages = {'/process':processResponse}

    def __init__(self,channel,queued):
        http.Request.__init__(self,channel,queued)

    def process(self):
        if self.pages.has_key(self.path):
            handler = self.pages[self.path]
            d = threads.deferToThread(handler,self)
	    d.addErrback(self.catchError)
            return d
        else:
            self.setResponseCode(http.NOT_FOUND)
            self.write('page not found')
            self.finish()

    def getConnections(self):
        return self.channel.getDbConnection()

    def catchError(self,request):
	return 'Error'


class requestProtocol(http.HTTPChannel):
    requestFactory = requestHandler

    def getDbConnection(self):
        connections = self.factory.connectionPools
        return connections

class RequestFactory(http.HTTPFactory):
    protocol = requestProtocol
    isLeaf = True

    def __init__(self):
        http.HTTPFactory.__init__(self)
        self.connectionPools = {}
