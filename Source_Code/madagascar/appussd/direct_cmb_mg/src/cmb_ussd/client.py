#!/usr/bin/env python
import sys
import xmlrpclib
from twisted.internet import reactor, threads
proxy = xmlrpclib.ServerProxy("http://localhost:4441/")
params = {}

ssid = 1
rstr = sys.argv[2]

if sys.argv[1]!='':
    ssid=sys.argv[1]

params['msisdn'] = "22665049281"
params['sessionId'] = ssid
params['ussdRequestString'] = rstr

def callserver(params):
    response = proxy.handleRequest(params)
    print response

callserver(params)
