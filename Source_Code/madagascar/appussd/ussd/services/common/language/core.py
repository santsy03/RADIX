#!/usr/bin/env python
import cx_Oracle
import traceback
from datetime import datetime
from DBUtils.PooledDB import PooledDB

from ussd.configs.core import databases
from ussd.services.common.secure.secure import decrypt
from ussd.metrics.sendmetric import  sendMetric
from ussd.metrics.config import dbTimeTemplate
from ussd.metrics.config import dbTemplate

def db_setup():
    db = databases['core']
    pooled = PooledDB(cx_Oracle, maxcached = 5, maxconnections=100,\
            user = decrypt(db['username']), password = decrypt(db['password'])\
            ,dsn = db['string'], threaded = True)
    pooled.timeout = 300
    return pooled.connection()


def getLanguage(resources):
    '''retrieves the current language setting for the given subscriber'''
    now = datetime.now()
    resources['start'] = now
    resources['type'] =  'timer'
    resources['nameSpace'] = dbTimeTemplate
    conn = db_setup()
    cursor = conn.cursor()
    try:
        msisdn = resources['msisdn']
        sql = ('select language from new_service_language where msisdn = :msisdn')
        cursor.execute(sql,{'msisdn':msisdn})
        result = cursor.fetchone()
        count = cursor.rowcount
        cursor.close()
        conn.close()
        sendMetric(resources)
    except Exception,e:
        error = 'operation:getLanguage,desc: could not retrieve language settings,error=%s' %str(e)
        print traceback.format_exc()

        try:
            cursor.close()
            conn.close()
            resources['type'] =  'beat'
            action = 'failure'
            nameSpace = dbTemplate.substitute(package=action)
            resources['nameSpace'] = nameSpace
            sendMetric(resources)
            return 'txt-2'
        except:
            return 'txt-2'
            
    else:
        resources['type'] =  'beat'
        action = 'success'
        nameSpace = dbTemplate.substitute(package=action)
        resources['nameSpace'] = nameSpace
        try:
            sendMetric(resources)
        except Exception,e:
            print str(e) + ":: Error"
        if count == 0:
            return 'txt-2'
        else:
            return result[0]

def setLanguage(resources):
    '''retrieves the current language setting for the given subscriber'''
    from config import responses
    now = datetime.now()
    resources['start'] = now
    resources['type'] =  'timer'
    resources['nameSpace'] = dbTimeTemplate
    #cursor = ((resources['connections']).acquire()).cursor()
    conn = db_setup()
    cursor = conn.cursor()
    try:
        msisdn = resources['msisdn']
        msg = resources['msg']
        print 'Connecting to DB : setting language for msisdn :' +str(msisdn)
        sql = ("select language from new_service_language where msisdn = :msisdn")
        param = {'msisdn':msisdn}
        cursor.execute(sql, param).fetchall()
        if cursor.rowcount > 0:
            sql0 = ("update new_service_language set language = :language where msisdn = :msisdn")

        else:
            sql0 = ("insert into new_service_language (id, msisdn, language, modified_at)\
                    values (new_service_lan.nextval, :msisdn, :language, sysdate)")
        params = {}
        params['msisdn'] = msisdn
        params['language'] = msg
        cursor.execute(sql0, params)
        cursor.connection.commit()
        cursor.close()
        conn.close()
        sendMetric(resources)
    except Exception,e:
        error = 'operation:getLanguage,desc: could not retrieve language settings,error=%s' %str(e)
        print error
        try:
            print 'Close DB Connection'
            cursor.close()
            conn.close()
            resources['type'] =  'beat'
            action = 'failure'
            nameSpace = dbTemplate.substitute(package=action)
            resources['nameSpace'] = nameSpace
            sendMetric(resources)
        except Exception,e:
            pass
    else:
        resources['type'] =  'beat'
        action = 'success'
        nameSpace = dbTemplate.substitute(package=action)
        resources['nameSpace'] = nameSpace
        sendMetric(resources)
        return responses[msg]

def processRequest(resources):
    operation = resources['operation']
    if operation == 'set':
        return setLanguage(resources)
    elif operation == 'get':
        return getLanguage(resources)



if __name__ == '__main__':
    resources = {}
    conn = db_setup()
    resources = {'msisdn':'261330465390','msg':'txt-3', 'connections':conn, 'operation':'get'}
    resources['parameters'] = {}
    #resources['parameters']['msisdn'] = '261338999232'
    #parameters['msisdn'] = '261336173681'
    #resources['parameters'] = parameters
    print getLanguage(resources)
    print processRequest(resources)
