#!/usr/bin/env python2.7

def getCurrentCount(resources):
    '''retrieves the current number of call backs that have been sent by a subscriber'''
    from datetime import datetime
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    try:
        cursor = ((resources['connections']).acquire()).cursor()
        now = datetime.now()
        today = '%s%s%s' %(str(now.day).zfill(2),str(now.month).zfill(2),str(now.year),)
        sql = "select id,requests from service_call_me_back where msisdn = :msisdn and expiry_date > to_date('%s','ddmmyyyy')" %today
        params = {'msisdn':msisdn}
        cursor.execute(sql,params)
        result = cursor.fetchone()
        count = cursor.rowcount
        cursor.close()
    except Exception,e:
        error = 'operation:getCurrentRequestCount,desc: could not retrieve the count of missed call alert requests for %s,error:%s' %(msisdn,str(e),)
        print error
        try:
            cursor.close()
        except Exception:
            pass
        raise e
    else:
        if count == 0:
            return False
        elif count == 1:
            return result

def sendMessage(resources):
    '''sends the call me back message'''
    import urllib
    from urllib import urlopen,urlencode
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    recipient = parameters['recipient']
    recipient = '261%s'%(str(recipient[-9:]))
    message = resources['message'] 
    args = urlencode({'to':'261%s'%(str(recipient[-9:])),'from':msisdn,'text':str(message)})
    params = urllib.urlencode({'username': 'radix', 'password': 'radix', 'from': msisdn, 'to': recipient, 'text': message})
    try:
        url = 'http://127.0.0.1:14020/cgi-bin/sendsms?%s'%(params)
        resp = urllib.urlopen(url)
        response = resp.read()
    except Exception,e:
        error = 'operation:callMeBack.sendMessage,desc:%s-%s,error:%s' %(str(msisdn),str(recipient),str(e))
        print error
        raise e
    else:
        print str(response) + 'Response'
        return response

def validateRecipient(recipient):
    ''' checks if the reciepient number is an airtel number.... added by vitalis '''
    if len(recipient) == 12:
        #if recipient[3:-7] == '6':
        return 'valid'
    else:
        return 'invalid'
    
def sendCMBRequest(resources):
    '''sends call me back request from the originating msisdn to the specified msisdn'''
    from string import Template
    #resources['connections'] = setup()
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    recipient = parameters['recipient']
    recipient = '261%s'%(str(recipient[-9:]))
    language = parameters['language']
    count = getCurrentCount(resources)
    from config import responses,message
    try:
        validity = validateRecipient(recipient)
    except Exception,e:
        error = 'error, failed to check validity of recipient %s, for CMB Request sent by msisdn %s, error %s' %(recipient,msisdn,str(e))
        print error
        raise e
    else:
        if validity == 'valid':
            if not count or int(count[1]) < 10:
                if not count:
                    sql = 'insert into service_call_me_back(id,msisdn,requests,expiry_date) values(service_cmb_sqc.nextval,:msisdn,:requests,sysdate+1)'
                    requests = '1'
                    params =  {'msisdn':msisdn,'requests':requests}
                elif int(count[1]) < 10:
                    sql = 'update service_call_me_back set requests = :requests where id = :id'
                    params = {'requests':int(count[1])+1,'id':count[0]}
                    requests = str(int(count[1])+1)
                sms = Template(message[language])
                message = sms.substitute(msisdn = msisdn)
                resources['message'] = message
                sendMessage(resources)
                response = Template((responses['True'])[language])
                try:
                    cursor = (resources['connections'].acquire()).cursor()
                    cursor.execute(sql,params)
                    cursor.connection.commit()
                    cursor.close()
                    
                except Exception,e:
                    error = 'operation:callMeBack.sendCMBRequest,desc:failed to update database %s-%s,error:%s' %(str(msisdn),str(recipient),str(e),)
                    print error
                    try:
                        cursor.close()
                    except Exception:
                        pass
                    raise e
                else:
                    return response.substitute(requests=requests,recipient=recipient)
            else:
                response = (responses['False'])[language]
                return response
        else:
            return responses['invalid'][language] 
            
            


def setup():
    from cx_Oracle import SessionPool
    from ussd.configs.core import databases
    from datetime import datetime
    from ussd.services.common.secure.secure import decrypt
    from ussd.metrics.config import databaseTimeTemplate
    from ussd.metrics.sendmetric import  sendMetric
    username = decrypt((databases['core'])['username'])
    password = decrypt((databases['core'])['password'])
    string = databases['core']['string']
    resources = {}
    resources['type'] =  'timer'
    resources['nameSpace'] = databaseTimeTemplate
    now = datetime.now()
    resources['start'] = now
    resources['connections'] = SessionPool(username,password,string,10,50,5,threaded=True) 
    print sendMetric(resources)
    return resources['connections']

if __name__ == '__main__':
    resources = {} 
    parameters = {}
    parameters['msisdn'] = '23563979791'
    parameters['recipient'] = '23563979791'
    parameters['language'] = 'txt-2'
    resources['parameters'] = parameters
    print sendCMBRequest(resources)
