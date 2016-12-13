def getTarrif(msisdn):
    ''' retrieves the tarrif for the given subscriber'''
    from prepaid.airHandler import AIRHandler
    air = AIRHandler()
    try:
        details = air.getBalanceAndDate(msisdn)
        if details['responseCode'] == 0:
            return str(details['serviceClassCurrent'])
        else:
            error = 'operation:getTarrif,desc:error retrieving tarrif details for %s,desc:%s' %(msisdn,str(details),)
            print error
    except Exception,e:
        error = 'operation:getTarrif,desc: error retrieving tarrif details for %s,desc:%s' %(msisdn,str(e),)
        print error
        raise (e)



def check_sub_type(msisdn):
    ''' 
    retrieves the serviceClassCurrent for the given subscriber
    sc 4 -- postpaid else prepaid
    '''
    from ussd.prepaid.airHandler import AIRHandler
    air = AIRHandler()
    try:
        details = air.getBalanceAndDate(msisdn)
        if details['responseCode'] == 0:
            sc = int(details['serviceClassCurrent'])
            if sc == 4:
                return 'postpaid'
            else:
                return 'prepaid'
        else:
            error = 'operation:check_sub_type,for %s,resp code:%s' % (msisdn, str(details['responseCode']))
            print error
            return 'postpaid'
    except Exception,e:
        error = 'operation:getTarrif,desc: error retrieving tarrif details for %s,desc:%s' %(msisdn,str(e),)
        print error
        return 'postpaid'

def getBalance(resources):
    '''retrieves the balance for the given subscriber'''
    from prepaid.airHandler import AIRHandler
    from decimal import Decimal
    air = AIRHandler()
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    cents = Decimal('0.01')
    try:
	details = air.getBalanceAndDate(msisdn)
        if details['responseCode'] == 0:
            return str((Decimal(details['accountValue1'])/Decimal('100')).quantize(cents))
        else:
            error = 'operation:getBalance,desc:error checking balance for %s,desc:%s' %('msisdn',str(details),)
            print error
    except Exception,e:
        error = 'operation:getBalance,desc: error retrieving balance for %s,desc:%s' %(str(msisdn),str(e),)
        print error
        raise (e)

def getRegistrationStatus(resources):
    '''retrieves the registration status for the given subscriber'''
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    cursor = (resources['zap'].acquire()).cursor()
    print 'Connecting to DB: Getting subscription status for msisdn'+str(msisdn)
    sql = 'SELECT substr(AUTHORIZED_MOBILE_NUMBER,-12,12) MSISDN,ACCOUNT_STATUS STATUS FROM ADMDBZAP.MOBILE_ACCOUNT_INFO  where AUTHORIZED_MOBILE_NUMBER = :msisdn'
    try:
        cursor.execute(sql,{'msisdn':msisdn})
        result = cursor.fetchall()
        count = cursor.rowcount
        print 'Close DB Connection'
        cursor.close()
    except Exception,e:
        error = 'operation:getRegistrationStatus,desc: could not retrieve registration status for %s,error:%s' %(str(msisdn),str(e),)
        print error
        try:
            print 'Close DB Connection'
            cursor.close()
        except Exception,b:
            pass
        raise e
    else:
        if count == 0:
            return False
        else:
            return True

def setup():
    from cx_Oracle import SessionPool
    resources = {}
    resources['zap'] = SessionPool('mamousr','mam0123','10.10.32.185:1525/mvtpstby',10,50,5,threaded=True)
    return resources

if __name__ == '__main__': 
    print check_sub_type('261330891190')
    #print getTarrif('254735449662')
    #resources = setup()
    #resources['parameters'] = {}
    #(resources['parameters'])['msisdn'] = '254735449662'
    #print getBalance(resources)
    #print getRegistrationStatus(resources)
