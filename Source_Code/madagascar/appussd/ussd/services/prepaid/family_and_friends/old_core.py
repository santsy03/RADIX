from ussd.prepaid.airHandler import AIRHandler
from ussd.services.prepaid.core import sendSMS
from ussd.services.prepaid.family_and_friends.config import fafId,response
from datetime import datetime
from ussd.metrics.sendmetric import sendMetric
from ussd.metrics.config import airTemplate,airTimeTemplate
def setFaf(resources):
    '''adds a FnF to a subscriber's list'''
    parameters = resources['parameters']
    parameters['real_msisdn'] = parameters['msisdn']
    fafNumber = str(parameters['faf'])[-9:]
    language = parameters['language']
    action = parameters['fafAction']
    if validateFaf(resources):
        parameters['msisdn'] = parameters['real_msisdn']
        if str(action) == 'ADD':
            result = getFafList(resources)
            if result['parameters']['fafListFull']:
                resources['parameters']['status'] = '4'
                message = response[language]['fafAlreadyFull']
                parameters['message'] = message
                sendSMS(resources)
                return response[language]['confirmationText']
            elif result == 'error':
                resources['parameters']['status'] = '0'
                message = response[language]['errorAir']
                parameters['message'] = message.substitute(fafNumber=fafNumber)
                sendSMS(resources)
                return response[language]['errorAir']
            else:
                if tagAsChargable(resources):
                    print 'successfully tagged as chargable'
                    if billSubscriber(resources):
                        print 'successfully Billed Subscriber'#updateBillingTable(resources)
                    else:
                        resources['parameters']['status'] = '2'
                        message = response[language]['insufficientFunds']
                        parameters['message'] = message
                        sendSMS(resources)
                        return response[language]['confirmationText']
                resources = updateFafList(resources)
                if resources['parameters']['status'] == '5':
                    message = response[language]['successfullyAdded']
                    parameters['message'] = message.substitute(fafNumber=fafNumber)
                elif resources['parameters']['status'] == '3':
                    message = response[language]['fafAlreadyExists']
                    parameters['message'] = message.substitute(fafNumber=fafNumber)
                elif resources['parameters']['status'] == '2':
                    message = response[language]['insufficientFunds']
                    parameters['message'] = message
                else:
                    resources['parameters']['status'] = '0'
                    message = response[language]['errorAir']
                    parameters['message'] = message 
                sendSMS(resources)
                #updateAddingStatus(resources)
                return response[language]['confirmationText']
        elif action == 'DELETE':
            result = getFafList(resources)
            if result == 'error':
                resources['parameters']['status'] = '0'
                message = response[language]['errorAir']
                parameters['message'] = message.substitute(fafNumber=fafNumber)
                sendSMS(resources)
                return response[language]['errorAir']
            elif result['parameters']['fafListFull']:
                if not checkIfChargable(resources): 
                    if tagAsChargable(resources):
                        print 'successfully tagged as chargable'
            resp = updateFafList(resources)
            if resources['parameters']['status'] == '5':
                message = response[language]['successfullyDeleted']
                parameters['message'] = message.substitute(fafNumber=fafNumber)
            elif resources['parameters']['status'] == '1':
                message = response[language]['numberDoesNotExist']
                parameters['message'] = message.substitute(fafNumber=fafNumber)
            else:
                resources['parameters']['status'] = '0'
                message = response[language]['errorAir']
                parameters['message'] = message 
            sendSMS(resources)
            #updateDeletingStatus(resources)
            return response[language]['confirmationText']
        updateFnFStatus(resources)
    else:
        message = response[language]['invalidFaf']
        parameters['message'] = message.substitute(fafNumber=fafNumber)
        return parameters['message'] 
   
def billSubscriber(resources):
    from ussd.services.prepaid.family_and_friends.config import cost
    parameters = resources['parameters']
    msisdn = parameters['msisdn'] 
    resources['type'] = 'timer'
    resources['start'] = datetime.now()
    resources['nameSpace'] = airTimeTemplate
    try:
        air = AIRHandler()
        response = air.updateBalanceAndDate(msisdn,-int(cost))
        sendMetric(resources)
    except Exception,e:
        error = "operation:billSubscriber failed for msisdn %s : error %s"%(str(msisdn),str(e))
        print error
        action = 'failure'
        resources['type'] = 'beat'
        resources['nameSpace'] = airTemplate.substitute(package=action)
        sendMetric(resources)
    else:
        action = 'success'
        resources['type'] = 'beat'
        resources['nameSpace'] = airTemplate.substitute(package=action)
        sendMetric(resources)
        if str(response['responseCode']).strip() == '0':
            a = True
            if a:#updateBillingTable(resources):  
                print 'successfully billed'
                return True
            else:
                return False
        else:
            print 'ReponseCode :: %s'%(str(response['responseCode']))
            return False

def checkIfChargable(resources):
    '''checks if subscriber is chargable i.e. when adding fafs'''
    msisdn = resources['parameters']['msisdn']
    sql = 'select chargable from service_fnf_chargable where msisdn=:msisdn'
    params = {'msisdn':msisdn}
    result = []
    print str(resources) + "resources"
    try:
        cursor = (resources['connections'].acquire()).cursor()
        cursor = cursor.execute(sql,params)
        result = cursor.fetchall()
        cursor.connection.commit()
        cursor.close()
    except Exception,e:
        error = 'operation:updateFnFStatus-UPDATE failed for msisdn :%s :Error :%s'%(str(msisdn),str(e))
        print error
    else:
        if len(result) > 0:
            if str(result[0][0]) == '1':
                return True
            else:
                return False
        else:
            return False

def tagAsChargable(resources):
    '''tags subscriber as chargable'''
    msisdn = resources['parameters']['msisdn']
    created_at = datetime.now()
    try:
        sql = 'insert into service_fnf_chargable(id,msisdn,chargable,created_at) values (service_fnf_chargable_sqc.nextval,:msisdn,1,:created_at)'
        params = {'msisdn':msisdn,'created_at':created_at}
        cursor = (resources['connections'].acquire()).cursor()
        cursor.execute(sql,params)
        print 'cursor' + str(cursor)
        cursor.connection.commit()
        cursor.close()
    except Exception,e:
        error = 'operation:tagAsChargable failed for msisdn :%s  :Error :%s'%(str(msisdn),str(e))
        print error
    else:
        print 'successfully inserted fnf record'
        return True
       
def validateFaf(resources):
    '''validates if faf is a prepaid'''
    from ussd.postpaid.core import getSubscriberType
    parameters = resources['parameters']
    parameters['msisdn'] = parameters['faf']
    if validateRecipient(parameters['faf']):
        type = getSubscriberType(resources)
        print str(type) + "type"
        if type == 'P':
            return True
        if type == 'N':
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


def updateDeletionStatus(resources):
    '''inserts and updates the record with the subscriber details'''
    from datetime import datetime
    print 'Params :::' + str(resources['parameters'])
    parameters = resources['parameters']
    msisdn = str(parameters['msisdn'])
    fafNumber = str(parameters['faf'])
    action= str(parameters['fafAction'])
    status = str(parameters['status'])
    
    sql = 'update service_fnf set status =:status,active = 1 where msisdn=:msisdn and faf =:fafNumber and modified_at=:modified_at'
    params = {'msisdn':msisdn,'status':status,'fafNumber':fafNumber,'modified_at':modified_at}
    try:
        cursor = (resources['connections'].acquire()).cursor()
        cursor = cursor.execute(sql,params)
        cursor.connection.commit()
        cursor.close()
    except Exception,e:
        error = 'operation:updateFnFStatus-UPDATE failed for msisdn :%s : fafNumber :%s :Error :%s'%(str(msisdn),str(fafNumber),str(e))
        print error
    else:
        print 'successfully updated record'
    
def updateFnFStatus(resources):
    '''inserts and updates the record with the subscriber details'''
    from datetime import datetime
    print 'Params :::' + str(resources['parameters'])
    parameters = resources['parameters']
    msisdn = str(parameters['msisdn'])
    fafNumber = str(parameters['faf'])
    action= str(parameters['fafAction'])
    status = '6'
    created_at = datetime.now()
    sql = 'insert into service_fnf(id,msisdn,faf_number,action,status,created_at) values (service_fnf_sqc.nextval,:msisdn,:fafNumber,:action,:status,:created_at)'
    params = {'msisdn':msisdn,'fafNumber':fafNumber,'action':action,'status':status,'created_at':created_at}
    try:
        cursor = (resources['connections'].acquire()).cursor()
        cursor = cursor.execute(sql,params)
        cursor.connection.commit()
        cursor.close()
    except Exception,e:
        error = 'operation:updateFnFStatus-INSERT failed for msisdn :%s : fafNumber :%s :Error :%s'%(str(msisdn),str(fafNumber),str(e))
        print error

    else:
        print 'successfully inserted fnf record'
        modified_at = datetime.now()
        sql = 'update service_fnf set status =:status where msisdn=:msisdn and faf =:fafNumber and modified_at=:modified_at'
        params = {'msisdn':msisdn,'status':status,'fafNumber':fafNumber,'modified_at':modified_at}
        try:
            cursor = (resources['connections'].acquire()).cursor()
            cursor = cursor.execute(sql,params)
            cursor.connection.commit()
            cursor.close()
        except Exception,e:
            error = 'operation:updateFnFStatus-UPDATE failed for msisdn :%s : fafNumber :%s :Error :%s'%(str(msisdn),str(fafNumber),str(e))
            print error
        else:
            print 'successfully updated record'

def updateFafList(resources):
    '''adds or deletes faf number to a subscriber'''
    parameters = resources['parameters']
    msisdn = str(parameters['msisdn'])
    fafNumber = '0%s'%(str(parameters['faf'])[-9:])
    action= str(parameters['fafAction'])
    service_name = 'ussd2mgFnFApplication' 
    resources['type'] = 'timer'
    resources['start'] = datetime.now()
    resources['nameSpace'] = airTimeTemplate
    print 'msisdn%s:::fafNumber:%s::: action%s::'%(str(msisdn),str(fafNumber),str(action))
    try:
        air = AIRHandler()
        resp = air.updateFaFList(msisdn,action,fafNumber,fafId,service_name)
        sendMetric(resources)
    except Exception,e:
        error = "operation:AddFaF failed for msisdn %s : error %s"%(str(msisdn),str(e))
        print error
        action = 'failure'
        resources['type'] = 'beat'
        resources['nameSpace'] = airTemplate.substitute(package=action)
        sendMetric(resources)
    else:
        action = 'success'
        resources['type'] = 'beat'
        resources['nameSpace'] = airTemplate.substitute(package=action)
        sendMetric(resources)
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
                print str(each) + "::: each"
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
        print str(parameters['message'])+ ":::: message"
        sendSMS(resources)
        return response[language]['confirmationText']

def getFafList(resources):
    '''gets the subscriber's Faf List'''
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    list_fafs = []
    resources['type'] = 'timer'
    resources['start'] = datetime.now()
    resources['nameSpace'] = airTimeTemplate
    try:
        air = AIRHandler()
        response = air.getFaFList(msisdn)
        sendMetric(resources)
    except Exception,e:
        error = "operation:getFafList failed for msisdn %s : error %s"%(str(msisdn),str(e))
        print error
        action = 'failure'
        resources['type'] = 'beat'
        resources['nameSpace'] = airTemplate.substitute(package=action)
        sendMetric(resources)
    else:
        action = 'success'
        resources['type'] = 'beat'
        resources['nameSpace'] = airTemplate.substitute(package=action)
        sendMetric(resources)
        if str(response['responseCode']).strip() == '0':
            if response.has_key('fafInformationList'):
                print 'fafInformationList' + str(response['fafInformationList'])
                for x in response['fafInformationList']:
                    list_fafs.append((x['fafNumber'],x['fafIndicator']))
                print 'fafList  :::'+str(list_fafs)
                if len(list_fafs) == 3:
                    resources['parameters']['fafListFull'] = True
                else:
                    resources['parameters']['fafListFull'] = False
                resources['parameters']['fafList'] = list_fafs
            else:
                resources['parameters']['fafList'] = '0'
                resources['parameters']['fafListFull'] = False
            return resources
        else:
            print 'error from AIR for msisdn:%s in getFafList '%(str(msisdn))
            return 'error'

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
    resources['parameters'] = {'msisdn':'261330770007','language':'txt-1','faf':'0333737373','fafAction':'ADD'}
    #print validateFaf(resources)
    print setFaf(resources)

