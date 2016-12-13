from datetime import datetime
from ussd.metrics.sendmetric import sendMetric
from ussd.metrics.config import airTemplate,airTimeTemplate
from ussd.services.prepaid.tarrif.config import response,names

def getServiceClass(resources, get_sc=False):
    '''retrieves a subscriber's service class'''
    from ussd.services.prepaid.tarrif.config import response,names
    from ussd.prepaid.airHandler import AIRHandler
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    language = parameters['language']
    resources['type'] = 'timer'
    resources['start'] = datetime.now()
    resources['nameSpace'] = airTimeTemplate
    try:
        time_now = datetime.now()
        air = AIRHandler()
        resp = air.getBalanceAndDate(str(msisdn))
        time_later = datetime.now()
        sendMetric(resources)
        elapsed_time = time_later - time_now
        print 'operation:getBalanceAndDate :: time taken : %s'%(str(elapsed_time))
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
        print 'operation:getBalanceAndDate : response code %s for msisdn %s'%(str(resp['responseCode']),str(msisdn))
        if str(resp['responseCode']).strip() == '0':
            serviceClass = resp['serviceClassCurrent']
            if get_sc:
                print '{} - service class: {}'.format(msisdn, serviceClass)
                return int(serviceClass)
            print str(serviceClass) + ":: service class"
            try:
                name = names[str(serviceClass)][language]
            except Exception,e:
                print 'unknown service class : %s'%(str(e))
                return "Votre plan tarifaire n'existe pas"
            else:
                return response[language]['successfullyCheckedTarrif'].substitute(name=name)
        else:
            return response[language]['errorAir'] 
            
        
   
def setServiceClass(resources):
    '''changes a subscriber's tarrif plan'''
    from ussd.prepaid.airHandler import AIRHandler
    from config import names, disallowed_sc
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    language = parameters['language']
    serviceClass = parameters['serviceClass']
    service_name = 'setServiceClass'
    tarrif_name = names[serviceClass][language]
    if canSetServiceClass(resources):
        if getServiceClass(resources, True) in disallowed_sc:
            return response[language]['sos']
        resources['type'] = 'timer'
        resources['start'] = datetime.now()
        resources['nameSpace'] = airTimeTemplate
        try:
            air = AIRHandler()
            time_now = datetime.now()
            result = air.setServiceClass(msisdn,int(serviceClass),service_name,tarrif_name)
            time_later = datetime.now()
            sendMetric(resources)
            elapsed_time = time_later - time_now
            print 'operation:setServiceClass :: time taken : %s'%(str(elapsed_time))
        except Exception,e:
            error = 'operation:setServiceClass failed for msisdn %s , error %s'%(str(msisdn),str(error))
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
            print 'operation:setServiceClass : response code %s for msisdn %s'%(str(result['responseCode']),str(msisdn))
            if str(result['responseCode']).strip() == '0':
                resp = response[language]['successfullySetServiceClass']
            elif str(result['responseCode']).strip() == '124':
                resp = response[language]['insufficientFunds']
            elif str(result['responseCode']).strip() == '117':
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
        time_now = datetime.now()
        response = air.getFaFList(msisdn)
        time_later = datetime.now()
        sendMetric(resources)
        elapsed_time = time_later - time_now
        print 'operation:getFaFList :: time taken : %s'%(str(elapsed_time))
    except Exception,e:
        error = "operation:canSetServiceClass failed for msisdn %s : error %s"%(str(msisdn),str(e))
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
        print 'operation:canSetServiceClass : response code %s for msisdn %s'%(str(response['responseCode']),str(msisdn))
        if str(response['responseCode']).strip() == '0':
            if response.has_key('fafInformationList'):
                for x in response['fafInformationList']:
                    list_fafs.append(x['fafNumber'])
                print len(list_fafs)
                if len(list_fafs) > 3:
                    resp = False
                else:
                    resp = True
            else:
                resp = True
        else:
            resp = False
        return resp


if __name__ == "__main__":
    from ussd.services.prepaid.core import setup
    resources = {}  
    resources = setup(resources) 
    resources['parameters'] = {'msisdn':'261337272618','serviceClass':'7','language':'txt-1'}
    print setServiceClass(resources)
          

    
           
             
