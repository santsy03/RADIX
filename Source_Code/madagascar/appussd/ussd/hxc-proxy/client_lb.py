#!/usr/bin/env python2.7

import sys
def emulateTangoGW(resources):
    from xmlrpclib import ServerProxy,Error
    url = 'http://172.25.128.108:8343/'
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    inputs = str(parameters['inputs'])
    sessionid = parameters['sessionid']
    params = {}
    params['MOBILE_NUMBER'] = msisdn
    params['SESSION_ID'] = sessionid
    params['SERVICE_KEY'] = '307'
    params['SEQUENCE'] = '0'
    params['LANGUAGE'] = 'FRA'
    params['USSD_BODY'] = inputs
    params['END_OF_SESSION'] = 'FALSE'
    params['RESPONSE_CODE'] = '0'
    try:
        server = ServerProxy(url)
        response = server.USSD_MESSAGE(params)
    except Error, v:
        error = 'Failed to emulate GW requests for %s with error %s' %(msisdn,str(v))
        print error
    else:
        message = response['USSD_BODY']
        return message

if __name__ == '__main__':
    ssid = 134356
    rstr = sys.argv[2]
    if sys.argv[1] != '':
        ssid = sys.argv[1]
    #resources = {'parameters':{'msisdn':'23562931125','sessionid':ssid,'inputs':rstr}}#postpaid
    #resources = {'parameters':{'msisdn':'261337150441','sessionid':ssid,'inputs':rstr}}#prepaid
    resources = {'parameters':{'msisdn':'261330891190','sessionid':ssid,'inputs':rstr}}#prepaid
    print emulateTangoGW(resources)
