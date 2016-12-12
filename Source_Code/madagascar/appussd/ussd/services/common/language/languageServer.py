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
    params['request'] = request
    params['msisdn'] = (params['msisdn'])[-12:]
    response = processRequest(params)
    sendResponse(response,request)

class requestHandler(http.Request):
    pages = {'/language':processMenu1}

    def __init__(self,channel,queued):
        http.Request.__init__(self,channel,queued)

    def process(self):
        if self.pages.has_key(self.path):
            handler = self.pages[self.path]
            d = threads.deferToThread(handler,self)
            return d
        else:
            self.setResponseCode(http.NOT_FOUND)
            self.write('page not found')
            self.finish()

class requestProtocol(http.HTTPChannel):
    requestFactory = requestHandler


class RequestFactory(http.HTTPFactory):
    protocol = requestProtocol
    isLeaf = True

    def __init__(self):
        http.HTTPFactory.__init__(self)
