#!/usr/bin/env python

def log(resources,error):
    if resources.has_key('logger'):
        resources['logger'].error(error)
    else:
        print error

def getSubscriberType(resources):
    from airHandler import AIRHandler
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    air = AIRHandler()
    resp = air.getBalanceAndDate(msisdn)
    if resp['responseCode'] == 102:
        return 'postpaid'
    else:
        return 'prepaid'
