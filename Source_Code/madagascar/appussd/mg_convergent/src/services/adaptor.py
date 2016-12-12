#!/usr/bin/env python
import cx_Oracle
import traceback
from twisted.web import http
from utilities.logging.core import log
from mg_convergent.src.config import message as msg
from mg_convergent.src.core import provision_subscribers, get_sub_language

from DBUtils.PooledDB import PooledDB

def get_params(request):
    ''' 
    retrieves the values of http post or get valuables
    '''
    params = {}
    for key, val in request.args.items():
        params[key] = val[0]
    return params


def process_convergent_req(request):
    params = get_params(request)
    resources = {}
    resources['parameters'] = params
    log(resources, "Request Params - {}".format(params), 'debug')
    msisdn = params.get('msisdn')
    connection = request.getConnections()
    try:
        language = get_sub_language(msisdn, connection)
        resources['parameters']['language'] = language
        request.write(msg['wait'])
        request.finish()
        response = provision_subscribers(resources)

    except Exception, e:
        log(resources, traceback.format_exc(), 'error')

    else:
        #request.write(msg['wait'])
        #request.finish()
        info = "%s|%s"%(str(msisdn), str(response))
        log(resources, "Processed Request - {}".format(str(info)))


class requestHandler(http.Request):
    pages = {'/process':process_convergent_req}

    def __init__(self,channel,queued):
        http.Request.__init__(self,channel,queued)

    def process(self):
        from twisted.internet import threads
        handler = self.pages[self.path]
        d = threads.deferToThread(handler,self)
        d.addErrback(catchError)
        return d

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
        from configs.config import databases
        from utilities.secure.core import decrypt
        username = decrypt(databases['core']['username'])
        password = decrypt(databases['core']['password'])
        string = databases['core']['string']

        http.HTTPFactory.__init__(self)
        pool = PooledDB(cx_Oracle, maxcached=5, maxconnections=100,
                        user=username, password=password, dsn=string,
                        threaded=True)
        self.connectionPools = pool 

def catchError(e=''):
    resp = 'System Error. Please try again later.'
    return resp


