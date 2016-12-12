#!/usr/bin/env python2.7
from direct_cmb_mg.src.metrics.sendmetric import  send_metric
from direct_cmb_mg.src.metrics.config import TECHNO_TREE_TEMPLATE, \
    TECHNO_TREE_TIME_TEMPLATE
        
from datetime import datetime, timedelta
from utilities.logging.core import log
def get_connection():
    """
    1. Establishes a connection with the IPACs module
    2. returns the established connection
    """
    import cx_Oracle
    from ussd.configs.core import ipacs as databases
    from ussd.services.common.secure.secure import decrypt
    try:
        connection = cx_Oracle.Connection(
                decrypt(databases['core']['username']), 
                decrypt(databases['core']['password']), 
                databases['core']['string'], threaded=True)
    except cx_Oracle.DatabaseError as err:
        error = 'operation:get_connection failed :  error %s' % (str(err), )
        log({}, error)
    return connection

def get_subscriber_type(resources):
    '''retrieves the subscriber type from TechnoTree Ability'''
    time_before = datetime.now()
    connection = get_connection()
    time_after = datetime.now()
    elapsed_time = time_after - time_before
    print 'IPACS connection: Time Taken :  %s' % (str(elapsed_time))
    cursor = connection.cursor()
    msisdn = (resources['parameters']['msisdn'])[-9:]
    sql = "select CUS_CUSTOMER_CATEGORY From incms.cms_m_customer \
        where  cus_tel_no =:msisdn"
    params = {'msisdn': msisdn}
    resources['type'] = 'timer'
    resources['start'] = datetime.now()
    resources['nameSpace'] = TECHNO_TREE_TIME_TEMPLATE
    try:
        cursor.execute(sql, params)
        result = cursor.fetchall()
        cursor.connection.commit()
        send_metric(resources)
    except Exception, err:
        error = ("operation:get_subscriber_type,") + (
                "desc:failed to add service on tabs for %s,error:%s") % (
                    msisdn, str(err),)
        log( resources, error)
        resources['type'] =  'beat'
        action = 'failure'
        name_space = TECHNO_TREE_TEMPLATE.substitute(package = action)
        resources['nameSpace'] = name_space
        send_metric(resources)
    else:
        resources['type'] =  'beat'
        action = 'success'
        name_space = TECHNO_TREE_TEMPLATE.substitute( package = action )
        resources['nameSpace'] = name_space
        send_metric(resources)
        if len(result) > 0:
            subscriber_type  = result[0][0]
            info = "Subscriber Type : %s" % str(subscriber_type)
            log ( resources, info, 'info' )
            if str(subscriber_type) == 'PREPAID':
                subscriber_type = 'prepaid'
            else:
                subscriber_type = 'postpaid'
            return subscriber_type
        else:
            info = "Subscriber is neither prepaid nor postpaid"
            log ( resources, info, 'info' )
            return 'None'
    finally:
        info = 'closing DB connection'
        log ( resources, info, 'info')
        cursor.close()
        connection.close()


def get_subscriber_language(resources):
    '''checks the language for the given subscriber'''
    from urllib2 import urlopen
    from direct_cmb_mg.src.config import TIMEOUT
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    try:
        url = 'http://127.0.0.1:9062/language?msisdn=%s&operation=get' % (
            str(msisdn))
        language = urlopen(url, timeout = TIMEOUT['language']) 
        language = language.read()
        print "Language : %s" % str(language)
    except Exception, err:
        error = ("operation: get_subscriber_language failed ") + (
            "for msisdn :%s, error :%s") % ( str(msisdn), str(err))
        print error
        return 'txt-3'
    else:
        return language 

def get_performance(resources, start_time):
    """
    used to gauge the time a request takes to be processed
    """
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
            mytime = (total_d.microseconds + (total_d.seconds + 
                total_d.days * 24 * 3600) * 10**6) / float(10**6)
        print 'CDR-%s|%s|%s|%s' % (msisdn, sessionid, str(mytime), 
                str(sub_type) )
    except Exception, err:
        print 'operation:get_performance failed : error - %s' % (str(err))
        pass

if __name__ == '__main__':
    resources = {}
    resources['parameters'] = {}
    resources['parameters']['msisdn'] = '261333333333'
    resp = get_subscriber_type(resources)
    print resp
