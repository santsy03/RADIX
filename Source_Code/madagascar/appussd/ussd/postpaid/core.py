from ussd.metrics.sendmetric import  sendMetric
from ussd.metrics.config import technoTreeTimeTemplate,technoTreeTemplate
from datetime import datetime

def getConnection(name):
    import cx_Oracle
    from ussd.configs.core import ipacs as databases
    from ussd.services.common.secure.secure import decrypt
    if name == 'IPACS':
        try:
            connection = cx_Oracle.Connection(decrypt(databases['core']['username']),decrypt(databases['core']['password']),databases['core']['string'],threaded=True)
        except Exception,e:
            error = 'operation:getConnection failed :  error %s'%(str(e),)
            print error
        return connection

def getSubscriberDetails(resources):
    '''retrieves Subscriber Details'''
    import cx_Oracle
    from datetime import datetime

    time_before = datetime.now()
    connection = getConnection('IPACS')
    time_after = datetime.now()
    elapsed_time = time_after - time_before
    print 'IPACS connection: Time Taken :  %s'%(str(elapsed_time))
    parameters = resources['parameters']
    msisdn = str(parameters['msisdn'])[-9:]
    par1 = ''
    par2 = ''
    par3 = ''
    par4 = ''
    par5 = ''
    par6 = ''
    par7 = ''
    par8 = ''
    resources['type'] = 'timer'
    resources['start'] = datetime.now()
    resources['nameSpace'] = technoTreeTimeTemplate
    try:
        cursor = connection.cursor()
        cursor.setinputsizes(cx_Oracle.STRING,cx_Oracle.STRING,cx_Oracle.STRING,cx_Oracle.STRING,cx_Oracle.STRING,cx_Oracle.STRING,cx_Oracle.STRING,cx_Oracle.STRING,cx_Oracle.STRING)
        result = cursor.callproc('INCMS.IVR_BALANCE_QUERY_V3',[msisdn,par1,par2,par3,par4,par5,par6,par7,par8])
        cursor.close()
        connection.close()
        sendMetric(resources)
    except Exception,e:
        error = 'operation:getSubscriberDetails,desc:could not retrieve the subscribers plan for %s, error:%s' %(int(msisdn),str(e),)
        print error
        try:
            cursor.close()
            resources['type'] =  'beat'
            action = 'failure'
            nameSpace = technoTreeTemplate.substitute(package=action)
            resources['nameSpace'] = nameSpace
            sendMetric(resources)
        except Exception:
            pass
        raise e

    else:
        resources['type'] =  'beat'
        action = 'success'
        nameSpace = technoTreeTemplate.substitute(package=action)
        resources['nameSpace'] = nameSpace
        sendMetric(resources)
        subs_details = []
        if len(result) > 0:
            for i in result:
                if i == None:
                    i = 0
                subs_details.append(i)
            print str(subs_details) + ":: subs details"
            resources['parameters']['current_balance'] = subs_details[1]
            resources['parameters']['current_month_usage'] = subs_details[2]
            resources['parameters']['total_sms_available'] = subs_details[3]
            resources['parameters']['credit_limit'] = subs_details[4]
            resources['parameters']['free_minutes'] = subs_details[5]
            resources['parameters']['gprs_discount_available'] = subs_details[6]
            resources['parameters']['free_units_off_available'] = subs_details[7]
            resources['parameters']['with_gprs_discount'] = subs_details[8]
        else:
            print 'no result from technotree'
        return resources
       

def getLastInvoiceAmount(resources):
    '''retrieves the last invoice amount'''
    import cx_Oracle
    time_before = datetime.now()
    connection = getConnection('IPACS')
    time_after = datetime.now()
    elapsed_time = time_after - time_before
    print 'IPACS connection: Time Taken :  %s'%(str(elapsed_time))
    parameters = resources['parameters']
    msisdn = str(parameters['msisdn'])[-9:]
    par1 = ''
    par2 = ''
    resources['type'] = 'timer'
    resources['start'] = datetime.now()
    resources['nameSpace'] = technoTreeTimeTemplate
    try:
        cursor = connection.cursor()
        cursor.setinputsizes(cx_Oracle.STRING,cx_Oracle.STRING,cx_Oracle.STRING)
        result = cursor.callproc('INCMS.IVR_BALANCE_QUERY_V4',[msisdn,par1,par2])
        cursor.close()
        connection.close()
        sendMetric(resources)
    except Exception,e:
        error = 'operation:getSubscriberDetails,desc:could not retrieve the subscribers plan for %s, error:%s' %(str(msisdn),str(e),)
        print error
        try:
            print 'Close DB Connection'
            cursor.close()
            resources['type'] =  'beat'
            action = 'failure'
            nameSpace = technoTreeTemplate.substitute(package=action)
            resources['nameSpace'] = nameSpace
            sendMetric(resources)
        except Exception:
            pass
        raise e
    else:
        resources['type'] =  'beat'
        action = 'success'
        nameSpace = technoTreeTemplate.substitute(package=action)
        resources['nameSpace'] = nameSpace
        sendMetric(resources)
        subs_details = []
        if len(result) > 0:
            for i in result:
                if i == None:
                    i = 0
                subs_details.append(i)
            print str(subs_details) + ":: subs details"
            resources['parameters']['opening_bal'] =  subs_details[1]
            resources['parameters']['last_invoice_amount'] = subs_details[2]
        else:
            print 'no result from technotree'
        return resources



def getSubscriberType(resources):
    '''retrieves the subscriber type from TechnoTree Ability'''
    import cx_Oracle
    time_before = datetime.now()
    connection = getConnection('IPACS')
    time_after = datetime.now()
    elapsed_time = time_after - time_before
    print 'IPACS connection: Time Taken :  %s'%(str(elapsed_time))
    cursor = connection.cursor()
    msisdn = (resources['parameters']['msisdn'])[-9:]
    sql = "select CUS_CUSTOMER_CATEGORY From incms.cms_m_customer where  cus_tel_no =:msisdn"
    params = {'msisdn': msisdn}
    resources['type'] = 'timer'
    resources['start'] = datetime.now()
    resources['nameSpace'] = technoTreeTimeTemplate
    try:
        cursor.execute(sql,params)
        result = cursor.fetchall()
        cursor.connection.commit()
        cursor.close()
        connection.close()
        sendMetric(resources)
    except Exception,e:
        error = 'operation:provisionService,desc:failed to add service on tabs for %s,error:%s' %(msisdn,str(e),)
        print error
        try:
            print 'Close DB Connection'
            cursor.close()
            resources['type'] =  'beat'
            action = 'failure'
            nameSpace = technoTreeTemplate.substitute(package=action)
            resources['nameSpace'] = nameSpace
            sendMetric(resources)
        except Exception:
            pass
        raise e
    else:
        resources['type'] =  'beat'
        action = 'success'
        nameSpace = technoTreeTemplate.substitute(package=action)
        resources['nameSpace'] = nameSpace
        sendMetric(resources)
        if len(result) > 0:
            return result[0][0]
        else:
            print 'no result from technotree ability'

def getOutstandingBalance(resources):
    from decimal import Decimal
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    usage = getCurrentUsage(resources)
    outstanding = getCurrentInvoice(resources)
    try:
        balance = usage + outstanding
    except Exception,e:
        error = 'operation:getOutstandingBalance,desc: failed to retrieve outstanding balance for %s, error:%s' %(msisdn,str(e),)
        print error
    else:
        return str(balance)

if __name__ == '__main__':
    #from test import setup
    resources = {}
    parameters = {}
    parameters['msisdn'] = '261330200003'
    #print "msisdn :: %s" % str(parameters['msisdn'])
    #parameters['msisdn'] ='261337117117'
    resources['parameters'] = parameters
    #print 'plan: %s' %(str(getSubscriberPlan(resources)))
    #print  getLastInvoiceAmount(resources)
    #print  getSubscriberDetails(resources)
    print getSubscriberType(resources)
