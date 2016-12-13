#!/usr/bin/env python
import sys
import xmlrpclib
from twisted.internet import reactor, threads
from me2u.src.config import PORTS
url = 'http://localhost:%s/' % PORTS['ussd']
proxy = xmlrpclib.ServerProxy(url)
params = {}

ssid = 1
rstr = sys.argv[2]

if sys.argv[1]!='':
    ssid=sys.argv[1]

params['msisdn'] = "261337150441"
params['sessionId'] = ssid
params['language'] = 'txt-2'
params['ussdRequestString'] = str(rstr)

def callserver(params):
    response = proxy.handleRequest(params)
    print response
    print response['ussdResponseString']

callserver(params)
