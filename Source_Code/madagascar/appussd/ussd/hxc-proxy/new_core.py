#!/usr/bin/env python2.7
import socket

def getSubscriberType(resources):
    '''checks the the type for the given subscriber'''
    from ussd.prepaid.core import check_sub_type
    msisdn = resources['parameters']['msisdn']
    try:
        socket.setdefaulttimeout(3)
        type = check_sub_type(msisdn)
        socket.setdefaulttimeout(None)
    except Exception,e:
        error = ('operation:getSubscriberType, desc:failed to retrieve '
                 'subscriber type for %s,error:%s' % (str(msisdn), str(e)))
        print error
        return 'prepaid'
    else:
        return type


def getSubscriberLanguage(resources):
    '''checks the language for the given subscriber'''
    from urllib2 import urlopen,Request
    msisdn = resources['parameters']['msisdn']
    try:
        url = 'http://127.0.0.1:9062/language?operation=get&msisdn=%s' % (msisdn)
        language = urlopen(Request(url),timeout=3).read()
        print '%s-language:%s' % (msisdn, language)
    except Exception,e:
        error= 'process:getSubscriberLanguage failed for:%s, error %s' % (msisdn, str(e))
        print error
        return 'txt-2'
    else:
        return language 

def get_performance(resources, start_time):
    from datetime import datetime, timedelta
    parameters = resources['parameters']
    s_type, sub_type = 'prepaid', 1
    try:
        msisdn = parameters['msisdn']
        sessionid = parameters['sessionId']
        if 'type' in parameters:
            s_type = parameters['type']
        if s_type == 'postpaid':
            sub_type = 2
        end_time = datetime.now()
        total_d = end_time - start_time
        if hasattr(timedelta, 'total_seconds'):
            #Pthon2.7
            mytime = total_d.total_seconds()
        else:
            #Python2.4
            mytime = (total_d.microseconds + (total_d.seconds + total_d.days * 24 * 3600) * 10**6) / float(10**6)
        print 'CDR-%s|%s|%s|%s'%(msisdn,sessionid,str(mytime),str(sub_type))
    except Exception, e:
        print 'Error getting performance data - %s' % (str(e))
        pass

if __name__ == '__main__':
    resources = {}# setup()
    parameters = {
                    'msisdn':'261337150441',
                    'request':'1',
                    'sessionId':'12345',
                    'language':'txt-1'
            }
    resources['parameters'] = parameters
    print getSubscriberLanguage(resources)
    #print getSubscriberType(resources)
