#/usr/bin/env python
from twisted.web import http
from string import Template
from twisted.internet import threads,reactor,defer
from cx_Oracle import SessionPool
from utilities.logging.core import log

def getParams(request):
    params = {}
    for k,v in request.args.items():
        params[k] = v[0]
    return params

def sendResponse(results,request):
    log({}, 'sendResponse: results - '+str(results))
    request.write(results)
    #request.finish()

def processSms(request):
    from modular_tariffs.src.sms.core import processSmsRequest
    params = getParams(request)
    params['connections'] = request.getConnections()
    params['request'] = request
    params['sessionId'] = getSession()
    params['msisdn'] = (params['msisdn'])[-12:]
    processSmsRequest(params)
    sendResponse('processed',request)

def getSession():
    from random import randint
    return randint(1000,9999)
    
class requestHandler(http.Request):
    pages = {'/process':processSms}

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
        connections = ''
        return connections

class RequestFactory(http.HTTPFactory):
    protocol = requestProtocol
    isLeaf = True

    def __init__(self):
        http.HTTPFactory.__init__(self)

def catchError(e=''):
    results = 'System Error. Please try again later.'
    return results
