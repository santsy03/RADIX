from datetime import datetime
from ussd.metrics.sendmetric import sendMetric
from ussd.metrics.config import airTemplate,airTimeTemplate
from ussd.services.prepaid.tarrif.config import response,names
def getServiceClass(resources):
    '''retrieves a subscriber's service class'''
    from ussd.services.prepaid.tarrif.config import response,names
    from ussd.prepaid.airHandler import AIRHandler
    print 'in getService Class'
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    language = parameters['language']
    print msisdn
    resources['type'] = 'timer'
    resources['start'] = datetime.now()
    resources['nameSpace'] = airTimeTemplate
    try:
        air = AIRHandler()
        resp = air.getBalanceAndDate(str(msisdn))
        sendMetric(resources)
    except Exception,e:
        error = 'operation:getServiceClass failed for msisdn %s: error %s'%(str(msisdn),str(e))
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
            serviceClass = resp['serviceClassCurrent']
            print 'service class ::: ' + str(serviceClass)
            name = names[str(serviceClass)]
            print 'name ::: ' + str(name)
            return response[language]['successfullyCheckedTarrif'].substitute(name=name)
        else:
            return response[language]['errorAir'] 
            
        
   
def setServiceClass(resources):
    '''changes a subscriber's tarrif plan'''
    from ussd.prepaid.airHandler import AIRHandler
    from config import names
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    language = parameters['language']
    serviceClass = parameters['serviceClass']
    service_name = 'setServiceClass'
    tarrif_name = names[serviceClass]
    if canSetServiceClass(resources):
        resources['type'] = 'timer'
        resources['start'] = datetime.now()
        resources['nameSpace'] = airTimeTemplate
        try:
            air = AIRHandler()
            result = air.setServiceClass(msisdn,int(serviceClass),service_name,tarrif_name)
            sendMetric(resources)
        except Exception,e:
            error = 'oparation:setServiceClass failed for msisdn %s , error %s'%(str(msisdn),str(error))
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
            if str(result['responseCode']).strip() == '0':
                resp = response[language]['successfullySetServiceClass']
            elif str(result['responseCode']).strip() == '124':
                resp = response[language]['insufficientFunds']
            elif str(result['responseCode']).strip() == '105':
                resp = response[language]['notAllowed']
            else:
                resp = response[language]['errorAir']
    else:
        resp = response[language]['notAllowed']
    return resp
        

def canSetServiceClass(resources):
    '''checks if a subscriber is allowed to set their service class'''
    from ussd.prepaid.airHandler import AIRHandler
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    language = parameters['language']
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
                    list_fafs.append(x['fafNumber'])
                print str(list_fafs) + ":::fafs"
                if len(list_fafs) >= 3:
                    resp = False
                else:
                    resp = True
            else:
                resp = True
        else:
            resp = False
        return resp


if __name__ == "__main__":
    resources = {}   
    resources['parameters'] = {'msisdn':'261337272618','serviceClass':'7','language':'txt-1'}
    print setServiceClass(resources)
          

    
           
             
