#!/usr/bin/env python
import sys
import xmlrpclib
from twisted.internet import reactor, threads
proxy = xmlrpclib.ServerProxy("http://127.0.0.1:7345/")
params = {}

ssid = 1
rstr = sys.argv[2]

if sys.argv[1]!='':
    ssid=sys.argv[1]

#params['msisdn'] = '250731920426'
#params['msisdn'] = '250730262406'
#params['msisdn'] = '261330465390'
params['msisdn'] = '261331100030'
#params['msisdn'] = '261330891190'
#params['msisdn'] = '261336799580'
#params['msisdn'] = '250731791057'
#params['msisdn'] = '250731754311' #oib
params['sessionId'] = ssid
params['ussdRequestString'] = str(rstr)
params['language'] = 'txt-1'

def callserver(params):
    response = proxy.handleRequest(params)
    print response
    print response['ussdResponseString']

callserver(params)

