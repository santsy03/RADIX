#!/usr/bin/env python2.7
import sys
import xmlrpclib
from twisted.internet import reactor, threads
from modular_tariffs.src.configs import PORTS
proxy = xmlrpclib.ServerProxy("http://localhost:%s/" % PORTS['ussd']['100'])
params = {}

ssid = 1
rstr = sys.argv[2]

if sys.argv[1]!='':
    ssid=sys.argv[1]

params['msisdn'] = "261331000643"
params['sessionId'] = ssid
params['ussdRequestString'] = rstr

def callserver(params):
    response = proxy.handleRequest(params)
    print response

callserver(params)
