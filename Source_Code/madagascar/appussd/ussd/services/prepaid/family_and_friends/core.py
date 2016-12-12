from ussd.prepaid.airHandler import AIRHandler
from ussd.services.prepaid.core import sendSMS
from ussd.services.prepaid.family_and_friends.config import fafId,response
from datetime import datetime
from ussd.metrics.sendmetric import sendMetric
from ussd.metrics.config import airTemplate,airTimeTemplate,dbTemplate,dbTimeTemplate

def setFaf(resources):
    '''adds a FnF to a subscriber's list'''
    parameters = resources['parameters']
    parameters['real_msisdn'] = parameters['msisdn']
    fafNumber = str(parameters['faf'])[-9:]
    language = parameters['language']
    action = parameters['fafAction']
    msisdn = parameters['msisdn']
    try:
        if validateFaf(resources):
            parameters['msisdn'] = parameters['real_msisdn']
            if str(action) == 'ADD':
                resources = addFaf(resources)
            elif str(action) == 'DELETE':
                resources = deleteFaf(resources)
            return resources
        else:
            message = response[language]['invalidFaf']
            parameters['message'] = message.substitute(fafNumber=fafNumber)
            return parameters['message']
    except Exception,e:
        print 'Error ::for msisdn %s - error- %s'%(str(msisdn),str(e))

def addFaf(resources):
    '''adds a faf in the subscriber faf list'''
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    parameters['real_msisdn'] = parameters['msisdn']
    fafNumber = str(parameters['faf'])[-9:]
    language = parameters['language']
    action = parameters['fafAction']
    parameters['msisdn'] = parameters['real_msisdn']
    try:
        result = getFafList(resources)
        print "Result :: %s" % str(result)
        if result == 'error':
            resources['parameters']['status'] = '0'
            message = response[language]['errorAir']
            parameters['message'] = message
            sendSMS(resources)
            return response[language]['errorAir']
        elif result['parameters']['fafListFull'] == True:
            resources['parameters']['status'] = '4'
            message = response[language]['fafAlreadyFull']
            parameters['message'] = message
            sendSMS(resources)
            insertAdditionStatus(resources)
            return response[language]['confirmationText']
        elif result['parameters']['fafListFull'] == False:
            resources = updateFafList(resources)
            print "Status :: %s" % str(resources['parameters']['status'])
            if resources['parameters']['status'] == '5':
                message = response[language]['successfullyAdded']
                parameters['message'] = message.substitute(fafNumber=fafNumber)
                sendResult(resources)
            elif resources['parameters']['status'] == '4':
                message = response[language]['fafAlreadyFull']
                parameters['message'] = message
            elif resources['parameters']['status'] == '2':
                message = response[language]['insufficientFunds']
                parameters['message'] = message
            else:
                resources['parameters']['status'] = '0'
                message = response[language]['errorAir']
                parameters['message'] = message 
            sendSMS(resources)
            insertAdditionStatus(resources)
            return response[language]['confirmationText']
    except Exception,e:
        print 'Error in add Faf for msisdn -%s error -%s'%(str(msisdn),str(e))


def deleteFaf(resources):
    '''delete faf from subscriber faflist'''
    parameters = resources['parameters']
    parameters['real_msisdn'] = parameters['msisdn']
    fafNumber = str(parameters['faf'])[-9:]
    language = parameters['language']
    action = parameters['fafAction']
    parameters['msisdn'] = parameters['real_msisdn']
    resp = processDeleteRequest(resources)
    if resources['parameters']['status'] == '5':
       message = response[language]['successfullyDeleted']
       parameters['message'] = message.substitute(fafNumber=fafNumber)
       sendResult(resources)
    elif resources['parameters']['status'] == '1':
       message = response[language]['numberDoesNotExist']
       parameters['message'] = message.substitute(fafNumber=fafNumber)
    elif resources['parameters']['status'] == '2':
       message = response[language]['insufficientFunds']
       parameters['message'] = message
    else:
       resources['parameters']['status'] = '0'
       message = response[language]['errorAir']
       parameters['message'] = message 
    sendSMS(resources)
    insertDeletionStatus(resources)
    return response[language]['confirmationText']
   

       
def validateFaf(resources):
    '''validates if faf is a prepaid'''
    from ussd.postpaid.core import getSubscriberType
    parameters = resources['parameters']
    parameters['msisdn'] = parameters['faf']
    if validateRecipient(parameters['faf']):
        type = getSubscriberType(resources)
        if type == 'PREPAID':
            return True
        if type == 'POSTPAID':
            return True
        else:
            return False
    else:
        return False

def validateRecipient(recipient):
    '''validate the recipient msisdn'''
    if not recipient.isdigit():
        return False
    if recipient[-9:][0] != '3':
        return False
    if len(recipient) < 9:
        return False
    return True


def insertDeletionStatus(resources):
    '''inserts a deletethe record with the subscriber details'''
    from datetime import datetime
    parameters = resources['parameters']
    msisdn = '261%s'%(str(parameters['msisdn'])[-9:])
    fafNumber = '261%s'%(str(parameters['faf'])[-9:])
    action= str(parameters['fafAction'])
    status = str(parameters['status'])
    created_at = datetime.now()
    modified_at = datetime.now()
    details = []
    resources['type'] =  'timer'
    resources['start'] = datetime.now()
    resources['nameSpace'] = dbTimeTemplate
    print msisdn , fafNumber ,status ,created_at , modified_at ,action ,status
    try:
        sql = 'insert into service_fnf(id,msisdn,faf_number,action,status,created_at,modified_at,active) values (service_fnf_sqc.nextval,:msisdn,:fafNumber,:action,:status,:created_at,:modified_at,0)'
        params = {'msisdn':msisdn,'fafNumber':fafNumber,'action':action,'status':status,'created_at':created_at,'modified_at':modified_at}
        connection = resources['connections'].connection()
        cursor = connection.cursor()
        cursor.execute(sql,params)
        cursor.connection.commit()
        cursor.close()
        connection.close()
        endtime = datetime.now()
        elapsed_time = endtime - resources['start']
        print 'operation:insertDeletionStatus :: time taken  ::: %s'%(str(elapsed_time))
        sendMetric(resources)
    except Exception,e:
        error = 'operation:insertDeletionStatus -failed for msisdn :%s : fafNumber :%s :Error :%s'%(str(msisdn),str(fafNumber),str(e))
        print error
        resources['type'] =  'beat'
        action = 'failure'
        nameSpace = dbTemplate.substitute(package=action)
        resources['nameSpace'] = nameSpace
        sendMetric(resources)
    else:
        resources['type'] =  'beat'
        action = 'success'
        nameSpace = dbTemplate.substitute(package=action)
        resources['nameSpace'] = nameSpace
        sendMetric(resources)
        print 'successfully inserted delete fnf record'

    
def insertAdditionStatus(resources):
    '''inserts a record with the subscriber details'''
    from datetime import datetime
    parameters = resources['parameters']
    msisdn = '261%s'%(str(parameters['msisdn'])[-9:])
    fafNumber = '261%s'%(str(parameters['faf'])[-9:])
    action= str(parameters['fafAction'])
    status = parameters['status']
    created_at = datetime.now()
    modified_at = datetime.now()
    sql = 'insert into service_fnf(id,msisdn,faf_number,action,status,created_at,modified_at,active) values (service_fnf_sqc.nextval,:msisdn,:fafNumber,:action,:status,:created_at,:modified_at,1)'
    params = {'msisdn':msisdn,'fafNumber':fafNumber,'action':action,'status':status,'created_at':created_at,'modified_at':modified_at}
    resources['type'] =  'timer'
    resources['start'] = datetime.now()
    resources['nameSpace'] = dbTimeTemplate
    try:
        connection = resources['connections'].connection()
        cursor = connection.cursor()
        cursor.execute(sql,params)
        cursor.connection.commit()
        cursor.close()
        connection.close()
        endtime = datetime.now()
        elapsed_time = endtime - resources['start']
        print 'operation:insertAdditionStatus :: time taken -%s'%(str(elapsed_time))
        sendMetric(resources)
    except Exception,e:
        error = 'operation:insertAdditionStatus-INSERT failed for msisdn :%s : fafNumber :%s :Error :%s'%(str(msisdn),str(fafNumber),str(e))
        print error
        resources['type'] =  'beat'
        action = 'failure'
        nameSpace = dbTemplate.substitute(package=action)
        resources['nameSpace'] = nameSpace
        sendMetric(resources)

    else:
        resources['type'] =  'beat'
        action = 'success'
        nameSpace = dbTemplate.substitute(package=action)
        resources['nameSpace'] = nameSpace
        sendMetric(resources)
        print 'successfully inserted addition fnf record'


def updateFafList(resources):
    '''adds or deletes faf number to a subscriber'''
    from datetime import datetime
    parameters = resources['parameters']
    msisdn = str(parameters['msisdn'])
    fafNumber = '0%s'%(str(parameters['faf'])[-9:])
    action= str(parameters['fafAction'])
    service_name = 'ussd2mgFnFApplication' 
    resources['type'] = 'timer'
    resources['start'] = datetime.now()
    resources['nameSpace'] = dbTimeTemplate
    print 'msisdn- %s : fafNumber- %s : action- %s'%(str(msisdn),str(fafNumber),str(action))
    try:
        air = AIRHandler()
        time_now = datetime.now()
        resp = air.updateFaFList(msisdn,action,fafNumber,fafId,service_name)
        endtime = datetime.now()
        elapsed_time = endtime - time_now
        print 'operation:updateFaflist ::: time taken %s'%(str(elapsed_time))
        sendMetric(resources)
    except Exception,e:
        error = "operation:update FaFList failed for msisdn %s : error %s"%(str(msisdn),str(e))
        print error
        action = 'failure'
        resources['type'] = 'beat'
        resources['nameSpace'] = dbTemplate.substitute(package=action)
        sendMetric(resources)
    else:
        action = 'success'
        resources['type'] = 'beat'
        resources['nameSpace'] = dbTemplate.substitute(package=action)
        sendMetric(resources)
        print 'operation:updateFaFList : response code %s for msisdn %s'%(str(resp['responseCode']),str(msisdn))
        if str(resp['responseCode']).strip() == '0':
            resources['parameters']['status'] = '5'
        elif str(resp['responseCode']).strip() == '130':
            resources['parameters']['status'] = '3'
        elif str(resp['responseCode']).strip() == '124':
            resources['parameters']['status'] = '2'
        elif str(resp['responseCode']).strip() == '129':
            resources['parameters']['status'] = '1'
        else:
            resources['parameters']['status'] = '0'
        return resources


def processDeleteRequest(resources):
    '''processes Delete request'''
    parameters = resources['parameters']
    msisdn = str(parameters['msisdn'])
    fafNumber = '0%s'%(str(parameters['faf'])[-9:])
    action= str(parameters['fafAction'])
    service_name = 'ussd2mgFnFApplication' 
    resources['type'] = 'timer'
    resources['start'] = datetime.now()
    resources['nameSpace'] = dbTimeTemplate
    print 'msisdn- %s : fafNumber- %s : action- %s'%(str(msisdn),str(fafNumber),str(action))
    try:
        air = AIRHandler()
        time_now = datetime.now()
        resp = air.updateFaFListWithoutCharge(msisdn,action,fafNumber,fafId,service_name)
        time_later = datetime.now()
        sendMetric(resources)
        elapsed_time = time_later - time_now
        print 'operation:processDeleteRequest ::: time taken %s'%(str(elapsed_time))
    except Exception,e:
        error = "operation:processDeleteRequest failed for msisdn %s : error %s"%(str(msisdn),str(e))
        print error
        action = 'failure'
        resources['type'] = 'beat'
        resources['nameSpace'] = dbTemplate.substitute(package=action)
        sendMetric(resources)
    else:
        action = 'success'
        resources['type'] = 'beat'
        resources['nameSpace'] = dbTemplate.substitute(package=action)
        sendMetric(resources)
        print 'operation:processDeleteRequest : response code %s for msisdn %s'%(str(resp['responseCode']),str(msisdn))
        if str(resp['responseCode']).strip() == '0':
            resources['parameters']['status'] = '5'
        elif str(resp['responseCode']).strip() == '130':
            resources['parameters']['status'] = '3'
        elif str(resp['responseCode']).strip() == '124':
            resources['parameters']['status'] = '2'
        elif str(resp['responseCode']).strip() == '129':
            resources['parameters']['status'] = '1'
        else:
            resources['parameters']['status'] = '0'
        return resources

def processGetFafList(resources):
    '''processes get Faf List request'''
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    fafAction = parameters['fafAction']
    language = parameters['language']
    result = getFafList(resources)
    list = []
    if result == 'error':
        message = response[language]['airError']
        parameters['message'] = message.substitute(fafNumber=fafNumber)
        sendSMS(resources)
        return resources[language]['airError']
    else:
        if result['parameters']['fafList'] == '0':
            list = '0'
        else:
            for each in resources['parameters']['fafList']:
                fafIndicator = int(each[1])
                fafNumber = each[0]
                if fafIndicator == fafId:
                    list.append(fafNumber)
                else:
                    list = '0'
            list =','.join(list)
        list = str(list)
        message = response[language]['fafList']
        parameters['message'] = message.substitute(list=list)
        sendSMS(resources)
        return response[language]['confirmationText']

def getFafList(resources):
    '''gets the subscriber's Faf List'''
    from datetime import datetime
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    if parameters['fafAction'] == 'ADD' or  parameters['fafAction'] == 'DELETE':
        fafNumber = parameters['faf']
    list_fafs = []
    resources['type'] = 'timer'
    resources['start'] = datetime.now()
    resources['nameSpace'] = airTimeTemplate
    try:
        air = AIRHandler()
        time_now = datetime.now()
        response = air.getFaFList(msisdn)
        time_later = datetime.now()
        elapsed_time = time_later - time_now
        print 'operation:getFafList ::: time taken %s'%(str(elapsed_time))
        sendMetric(resources)
        action = 'success'
        resources['type'] = 'beat'
        resources['nameSpace'] = airTemplate.substitute(package=action)
        sendMetric(resources)
        print 'operation:getFaFList : response code %s for msisdn %s'%(str(response['responseCode']),str(msisdn))
        if str(response['responseCode']).strip() == '0':
            if response.has_key('fafInformationList'):
                for x in response['fafInformationList']:
                    faf_number = str(x['fafNumber'])[-9:]
                    fafIndicator = int (x['fafIndicator'])
                    if fafIndicator == int(fafId):
                        list_fafs.append((faf_number,fafIndicator))
                if len(list_fafs) >= 3:
                    resources['parameters']['fafListFull'] = True
                    resources['parameters']['fafList'] = list_fafs
                    return resources
                else:
                    resources['parameters']['fafListFull'] = False
                    resources['parameters']['fafList'] = list_fafs
                    return resources
            else:
                resources['parameters']['fafList'] = '0'
                resources['parameters']['fafListFull'] = False
                return resources
        else:
            print 'error from AIR for msisdn:%s in getFafList '%(str(msisdn))
            return 'error'
    except Exception,e:
        error = "operation:getFafList failed for msisdn %s : error %s"%(str(msisdn),str(e))
        print error
        action = 'failure'
        resources['type'] = 'beat'
        resources['nameSpace'] = airTemplate.substitute(package=action)
        sendMetric(resources)

def sendResult(resources):
    '''sends the resulst of add/delete to IPACS'''
    import cx_Oracle
    from datetime import datetime
    from ussd.postpaid.core import getConnection
    from ussd.metrics.config import technoTreeTimeTemplate,technoTreeTemplate

    time_before = datetime.now()
    connection = getConnection('IPACS')
    time_after = datetime.now()
    elapsed_time = time_after - time_before
    print 'IPACS connection: Time Taken :  %s'%(str(elapsed_time))
    print resources
    try:
        parameters = resources['parameters']
        print "Parameters %s" % str(parameters)
        msisdn = str(parameters['msisdn'])[-9:]
        fnf_msisdn = str(parameters['faf'])[-9:]
        action = str(parameters['fafAction']).upper()
        user_id = 'USSD'
        resources['type'] = 'timer'
        resources['start'] = datetime.now()
        resources['nameSpace'] = technoTreeTimeTemplate
        cursor = connection.cursor()
        cursor.setinputsizes(cx_Oracle.STRING,cx_Oracle.STRING,cx_Oracle.STRING,cx_Oracle.STRING)
        result = cursor.callproc('INCMS.IPACS_FNF_API',[msisdn,fnf_msisdn,action,user_id])
        print "Result :: %s"  % str(result)
        cursor.close()
        connection.close()
        sendMetric(resources)
    except Exception,e:
        error = 'operation:sendResult failed for msisdn: %s, error:%s' %(int(msisdn),str(e),)
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



def setup(resources):
    from cx_Oracle import SessionPool
    from ussd.configs.core import databases
    from ussd.services.common.secure.secure import decrypt
    try:
        resources['connections'] = SessionPool(decrypt(databases['core']['username']),decrypt(databases['core']['password']),databases['core']['string'],10,50,5,threaded=True)
    except:
        pass
    return resources
 

if __name__ == "__main__":
    resources = {}
    resources = setup(resources)
    #resources['parameters'] = {'msisdn':'261337150441','language':'txt-3','faf':'0331100465','fafAction':'ADD'}
    resources['parameters'] = {'msisdn':'261337272618','language':'txt-3','faf':'0331100465','fafAction':'ADD'}
    #print validateFaf(resources)
    #print processGetFafList(resources) 
    print sendResult(resources)
    #print setFaf(resources) 
    #print updateFafList(resources)

