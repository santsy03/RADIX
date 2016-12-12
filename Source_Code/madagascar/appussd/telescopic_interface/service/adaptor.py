#!/usr/bin/env python

import traceback
from twisted.web import http

from telescopic_interface.config import message as msg
from telescopic_interface.core import (enqueue_provision_request,
        get_sub_language, get_subscription_count)
from utilities.sms.core import send_message

def get_params(request):
    ''' 
    retrieves the values of http post or get valuables
    '''
    params = {}
    for key, val in request.args.items():
        params[key] = val[0]
    return params

def process_telescopic_req(request):
    params = get_params(request)
    print params
    msisdn = params.get('msisdn')
    package = params.get('package_id')
    can_renew = params.get('can_renew')
    try:
        response = enqueue_provision_request(package, msisdn, can_renew)

    except Exception, e:
        print traceback.format_exc()

    else:
        request.write(msg['txt-1']['wait'])
        request.finish()
        info = "%s|%s"%(str(msisdn), str(response))
        print info


class requestHandler(http.Request):
    pages = {'/process':process_telescopic_req}

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


