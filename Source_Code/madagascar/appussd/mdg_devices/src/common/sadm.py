#!/usr/bin/env python
from suds.client import Client
from urllib2 import urlopen, Request
from urllib import urlencode
from mdg_devices.src.configs.sadm import BASE_URL
from mdg_devices.src.configs.sadm import TIP_SERVICE_URL
from mdg_devices.src.configs.sadm import URL_ROOT
from mdg_devices.src.configs.sadm import USER_NAME
from mdg_devices.src.configs.sadm import PASSWORD
from mdg_devices.src.configs.sadm import SADM_TIMEOUT
from mdg_devices.src.configs.sadm import CONTEXT as context

import logging

import traceback
import sys

sys.setrecursionlimit(500)
class SoapConnector(object):

    def __init__(self):
        self.base_url = BASE_URL
        self.user_name = USER_NAME
        self.password = PASSWORD
        self.root = URL_ROOT
        self.tip_url = TIP_SERVICE_URL


    def get_subscriber_info(self, params):
        '''
        gets subscriber info
        '''
        action = 'getSubInfo'

        try:
            url = self.tip_url + self.root
            print url
            client = Client(url, timeout = SADM_TIMEOUT)
            client.set_options(service = (context[action])['service'],
                    port = (context[action])['port'])
        except Exception, err:
            raise err
        else:
            return client.service.getSubscriberInfo(params['msisdn'])

    def get_previous_imei(self, params):
        '''
        gets previous imei
        '''
        
        action = 'getSubInfo'

        try:
            url = self.tip_url + self.root
            print url
            client = Client(url)
            client.set_options(service = (context[action])['service'], 
                    port = (context[action])['port'])
            print client
        except Exception, err:
            raise err
        else:
            return client.service.getPreviousImeiOfSubscriber(params['msisdn'])


    def provision(self, params):
        '''
        enrolls a subscriber
        '''
        sub_info = self.get_subscriber_info(params)
        print "msisdn: %s sub_info: %s" % (params['msisdn'], str(sub_info))
        action = 'provision'
        try:
            url = self.base_url + self.root
            print url
            client = Client(url)
            client.set_options(service = (context[action])['service'],
                    port = (context[action])['port'])
        except Exception, err:
            print traceback.format_exc()
            raise err
        else:
            return client.service.submitProvisioningRequest(self.user_name, 
                    self.password, (params['msisdn']))


if __name__ == '__main__':
    test = {}
    test['msisdn'] = '+261332473466'
    test['imsi'] = '9031323268222'
    soap = SoapConnector()
    resp = soap.get_subscriber_info(test)
    resp = dict(resp)
    print resp
    print type(resp)
