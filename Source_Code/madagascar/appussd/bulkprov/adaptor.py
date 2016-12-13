#!/usr/bin/env python

import traceback
from twisted.web import http

from bulkprov.core import process_bulk_request
from bulkprov.config import file_path
from utilities.sms.core import send_message
from datetime import datetime, timedelta, date

def get_params(request):
    ''' 
    retrieves the values of http post or get valuables
    '''
    params = {}
    for key, val in request.args.items():
        params[key] = val[0]
    return params

def process_bulk_prov(request):
    response = ""
    params = get_params(request)
    print params
    filename = params.get('filename')
    try:
        response = process_bulk_request(file_path, filename)

    except Exception, e:
        print traceback.format_exc()

    else:
        request.finish()
        info = "%s|%s"%(str(msisdn), str(response))
        print info

def process_bulk_provisioning():

    #filename = 'MG_Failed_Translated_PackageIds_%s_%s00HRS.csv'%((date.today()).strftime('%Y-%m-%d'),(datetime.now()).strftime('%H'))    
    file = 'MG_Translated_PackageIds_' + (date.today()).strftime('%Y-%m-%d')+'_'+(datetime.now()).strftime('%H')+'00HRS'+'.csv'
    filename = file.split(".")[0]
    try:
        response = process_bulk_request(file_path, filename)

    except Exception, e:
        print traceback.format_exc()

    else:
        #request.finish()
        info = "%s"%(str(response))
        print info


class requestHandler(http.Request):
    pages = {'/process':process_bulk_prov}

    def __init__(self,channel,queued):
        http.Request.__init__(self,channel,queued)

    def process(self):
        from twisted.internet import threads
        handler = self.pages[self.path]
        d = threads.deferToThread(handler,self)
        d.addErrback(catchError)
        return d


class requestProtocol(http.HTTPChannel):
    requestFactory = requestHandler


class RequestFactory(http.HTTPFactory):
    protocol = requestProtocol
    isLeaf = True

def catchError(e=''):
    resp = 'System Error. Please try again later.'
    return resp

if __name__ == '__main__':
    process_bulk_provisioning()

