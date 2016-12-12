#!/usr/bin/env python
# -*- coding: utf8 -*-
from datetime import datetime
from twisted.web import server, resource
from myxmlrpc import XMLRPC, withRequest
from twisted.internet import threads

from mdg_devices.src.common.subscriber import Subscriber 
from mdg_devices.src.common.core import setup
from mdg_devices.src.common.queue_client import QueueClient
from mdg_devices.src.configs.messages import MESSAGE 
from mdg_devices.src.common.whitelists import Whitelist

queue_object = QueueClient()

def get_params(request):
    '''
    Retrieves values of HTTP POST or GET variables
    '''
    params = {}
    for key, val in request.args.items():
        params[key] = val[0]
    return params


class UssdService(resource.Resource):
    def __init__(self):
        resource.Resource.__init__(self)
        self.resources = {}
        self.con = setup()
        self.queue_object = queue_object

    def getChild(self, path, request):
        """
        Override with no change just return back
        """
        return self

    def process_request(self, request):
        '''
        process ussd calls
        '''
        start_time = datetime.now()
        raw_params = get_params(request)
        try:
            params = raw_params
            print 'USSD Request PARAMS: ' + str(raw_params)
            params['connection'] = self.con
            language = params.get('language', 'FRA')
            resources = {'parameters': params}
            msisdn = params['msisdn']
            sub_request = params['input']
            assert msisdn.isdigit()
            subscriber = Subscriber(msisdn, None, con=self.con)
            code = None
            transaction_id = subscriber.transaction_id
            sub_request = sub_request.split('*')
            if sub_request[0] == '27':
                code = sub_request[1]
                action = 'retailer'
            elif sub_request[0] == '25':
                action = 'imei'
            pars = {
                'msisdn' : msisdn,
                'code': code,
                'transaction_id': transaction_id,
                'action':action,
                'language': language}
            self.queue_object.publish(pars)
            if language in MESSAGE['received']:
                resp = MESSAGE['received'][language]
            else:
                resp = MESSAGE['received']['FRA']

        except Exception, e:
            print str(e)
            resp = MESSAGE['ussd_error']
        else:
            print raw_params['msisdn'], resp
            request.write(resp)
            request.finish()
            return resp

    def render_GET(self, request):
        '''
        processes response from backend action
        '''
        try:
            deffer = threads.deferToThread(self.process_request, request)
            deffer.addErrback(self.handle_failure)
        except Exception, err:
            error = 'process_request error - %s' % (str(err),)
            print error
        else:
            return server.NOT_DONE_YET

    def handle_failure(self, error):
        '''
        returns error status to calling GUI
        '''
        print "Got an exception: %s" % (error.getTraceback(),)
        return MESSAGE['ussd_error']


class CacheService(resource.Resource):
    def __init__(self):
        resource.Resource.__init__(self)
        self.resources = {}
        self.con = setup()
        self.retailers = Whitelist('populate_retailer', None, self.con)
        self.imeis = Whitelist('populate_imei',None, self.con)
        self.load_cache()

    def getChild(self, path, request):
        """
        Override with no change just return back
        """
        return self

    def process_request(self, request):
        '''
        Process requests and return dictionary for return
        '''
        start_time = datetime.now()
        params = get_params(request)
        print 'CACHE Request Params: %s' % (str(params))
        action = params['action']
        if action == 'retailers':
            self.retailers.run_action('GUI')
        elif action == 'imeis':
            self.imeis.run_action('GUI')

    def render_GET(self, request):
        '''
        To handle GET requests for cache resync 
        '''
        deffer = threads.deferToThread(self.process_request, request)
        deffer.addErrback(self.handle_failure)
        return 'Loading Cache'

    def handle_failure(self, error):
        '''
        Output error
        '''
        print "Got an exception: %s" % (error.getTraceback(),)
        return 'error handling cache request'

    def load_cache(self):
        d = threads.deferToThread(self.preload)
        d.addErrback(self.handle_failure)

    def preload(self):
        print 'First >>> loading cache >>>>'
        self.retailers.run_action()
        self.imeis.run_action()
        print 'Cache Loaded'

class GuiService(resource.Resource):
    def __init__(self):
        resource.Resource.__init__(self)
        self.resources = {}
        self.con = setup()
        self.queue_object = queue_object

    def getChild(self, path, request):
        """
        Override with no change just return back
        """
        return self

    def process_request(self, request):
        '''
        Acquires a transaction Id and returns it to the calling GUI
        '''
        start_time = datetime.now()
        raw_params = get_params(request)
        try:
            params = raw_params
            print 'GUI Request PARAMS: ' + str(raw_params)
            params['connection'] = self.con
            resources = {'parameters': params}
            msisdn = params['msisdn']
            assert msisdn.isdigit()
            subscriber = Subscriber(msisdn, None, con=self.con)
            code = None
            transaction_id = subscriber.transaction_id
            pars = {
                    'msisdn' : msisdn,
                    'code': code,
                    'transaction_id': transaction_id,
                    'action' : 'imei',
                    'language':'FRA'}
            print subscriber.transaction_id
            request.write(subscriber.transaction_id)
            self.queue_object.publish(pars)
        except Exception, err:
            error = 'GUI Request Failed:%s, error:%s' % (
                    str(raw_params), str(err))
            print error
            request.write(MESSAGE['gui_error'])
        request.finish()

    def render_GET(self, request):
        '''
        processes response from backend action
        '''
        try:
            deffer = threads.deferToThread(self.process_request, request)
            deffer.addErrback(self.handle_failure)
        except Exception, err:
            error = 'process_request error - %s' % (str(err),)
            print error
        else:
            return server.NOT_DONE_YET

    def handle_failure(self, error):
        '''
        returns error status to calling GUI
        '''
        print "Got an exception: %s" % (error.getTraceback(),)
        return MESSAGE['gui_error'] 


class ServiceFactory(resource.Resource):
    def __init__(self):
        resource.Resource.__init__(self)
        # add url endpoints here
        self.putChild('GUI', GuiService())
        self.putChild('process', UssdService())
        self.putChild('CACHE', CacheService())
