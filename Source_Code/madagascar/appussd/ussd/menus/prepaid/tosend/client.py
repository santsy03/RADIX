#!/usr/bin/env python
import sys
import xmlrpclib
from twisted.internet import reactor, threads
proxy = xmlrpclib.ServerProxy("http://127.0.0.1:7190/")
params = {}

ssid = 1
rstr = sys.argv[2]

if sys.argv[1]!='':
    ssid=sys.argv[1]

params['msisdn'] = "261330770007"
params['sessionId'] = ssid
params['ussdRequestString'] = str(rstr)
params['language'] = 'txt-1'

def callserver(params):
    response = proxy.handleRequest(params)
    print response
    print response['ussdResponseString']

callserver(params)

