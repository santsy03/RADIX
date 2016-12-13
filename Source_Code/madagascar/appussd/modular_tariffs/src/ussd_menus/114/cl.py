#!/usr/bin/env python2.7
import sys
import xmlrpclib
from twisted.internet import reactor, threads
from modular_tariffs.src.configs import PORTS
proxy = xmlrpclib.ServerProxy("http://localhost:%s/" % PORTS['ussd']['114'])
params = {}

ssid = 1
rstr = sys.argv[2]

if sys.argv[1]!='':
    ssid=sys.argv[1]

#params['msisdn'] = "261336173681"
params['msisdn'] = "261337272618"
params['sessionId'] = ssid
params['ussdRequestString'] = rstr
params['language'] = 'txt-1'
params['service_key'] = '177'

def callserver(params):
    response = proxy.handleRequest(params)
    print response

callserver(params)
