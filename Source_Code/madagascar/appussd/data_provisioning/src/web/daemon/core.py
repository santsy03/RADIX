#!/usr/bin/env python
#from data_provisioning.src.common.core import log
from utilities.logging.core import log
import traceback

def updateRequestStatus(resources):
    '''updates the status for the given transactionId'''
    from data_provisioning.src.common.db.core import getConnection
    from datetime import datetime
    try:
        parameters = resources['parameters']
        transactionId = parameters['transactionId']
        response = parameters['response']
        balance_response = parameters['balance_response']
        status = parameters['status']
        conn = getConnection(resources)
        cursor = conn.cursor()
        now = datetime.now()
        sql = 'update requests set status = :status,response = :response, balance = :balance, completed_at = systimestamp where id =:transactionId'
        params = {'response':response,'transactionId':transactionId,'status':int(status),"balance": balance_response}
        cursor.execute(sql,params)
        cursor.connection.commit()
    except Exception,e:
        error = 'operation:updateRequestStatus,desc: failed to update request status %s,error:%s' %(str(transactionId),str(e),) 
        log(resources,error,'error')
        log(resources, traceback.format_exc(),'error')
        cursor.close()
        conn.close()
    else:
        info = "updated request: %s successfully" % (str(transactionId))
        log(resources, info, 'info')
        try:
            cursor.close()
            conn.close()
        except Exception, err:
            log(resources, traceback.format_exc(), 'error')



def getCallBack(resources):
    from data_provisioning.src.common.db.core import getConnection
    try:
        parameters = resources['parameters']
        transactionId = parameters['transactionId']
        conn = getConnection(resources)
        cursor = conn.cursor()
        sql = 'select callback,msisdn from requests where id =:transactionId'
        params = {'transactionId':int(transactionId)}
        cursor.execute(sql,params)
        result = cursor.fetchone()
        count = cursor.rowcount
    except Exception,e:
        error = 'operation:getCallBack,desc:retrieving callbacks failed for %s,error:%s' %(str(transactionId),str(e),)
        log(resources,error)
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass
    else:
        cursor.close()
        conn.close()
        if count == 1:
            if str(result[0]).strip() == '-':
                info = '%s - does not have a callback' %(str(transactionId))
                log(resources, info, 'info')
                return False
            else:
                info = '%s- %s -%s' %(str(transactionId), str(result), str(parameters))
                log(resources, info, 'info')
                return result
        else:
            return False

def invokeCallBack(resources):
    from urllib import urlencode
    from urllib2 import urlopen,Request

    parameters = resources['parameters']
    callBack = parameters['callBack']
    transactionId = str(parameters['transactionId'])
    name = parameters['name']
    status = str(parameters['status'])
    volume = parameters['volume']
    expiry = parameters['expiry']
    msisdn = parameters['msisdn']
    data = urlencode({'transactionId':transactionId,'msisdn':msisdn,'statusCode':status,'packageName':name,'balance':volume,'expiry':expiry})
    try:
        request = Request(callBack,data)
        resp = (urlopen(request,timeout=3)).read()
        info = '%s - %s - %s' %(str(transactionId), str(callBack), str(resp))
        log(resources,info, 'info')
    except Exception,e:
        error = 'operation:invokeCallBack,desc: failed to invoke callBack for %s - %s,error:%s' %( str(transactionId), str(callBack),str(e),)
        log(resources,error, 'error')


def processRequest(resources):
    try:
        transactionId = resources['parameters']['transactionId']
        updateRequestStatus(resources)
        results = getCallBack(resources) 
        callBack = False
        if results:
            callBack = results[0]
            msisdn = results[1]
        if callBack:
            resources['parameters']['msisdn'] = msisdn
            resources['parameters']['callBack'] = callBack
            invokeCallBack(resources)
    except Exception,e:
        error = 'operation:processRequest,desc: failed to process provisioning response %s ,error:%s' %(str(transactionId), str(e))
        log(resources ,error, 'error')
        log(resources, traceback.format_exc(),'error')


def setup(resources):
    from cx_Oracle import SessionPool
    from data_provisioning.src.common.secure.core import decrypt
    from data_provisioning.src.configs.core import databases
    from config import home

    cwd = home

    resources = {}
    resources['connections'] = SessionPool(decrypt((databases['core'])['username']),decrypt((databases['core'])['password']),(databases['core'])['string'],10,50,5,threaded=True)
    return resources


