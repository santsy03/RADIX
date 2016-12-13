#!/usr/bin/env python
from ussd.metrics.sendmetric import  sendMetric
from ussd.metrics.config import dbTimeTemplate,dbTemplate


def getCurrentCount(resources):
    '''retrieves the current number of call backs that have been sent by a subscriber'''
    from datetime import datetime
    parameters = resources['parameters']
    msisdn = "261%s"%(str(parameters['msisdn'])[-9:])
    print str(msisdn)+ "::: msisdn"
    try:
        cursor = ((resources['connections']).acquire()).cursor()
        print 'Connecting to DB: retrieving  current number of call backs used for msisdn %s'%(str(msisdn))
        now = datetime.now()
        resources['type'] =  'timer'
        resources['start'] = now
        resources['nameSpace'] = dbTimeTemplate
        today = '%s%s%s' %(str(now.day).zfill(2),str(now.month).zfill(2),str(now.year),)
        print "today :: %s"%(str(today))
        sql = "select id,requests from service_call_me_back where msisdn = :msisdn and expiry_date > to_date('%s','ddmmyyyy')" %today
        params = {'msisdn':msisdn}
        cursor.execute(sql,params)
        result = cursor.fetchone()
        count = cursor.rowcount
        print 'Close DB Connection'
        cursor.close()
        sendMetric(resources)
    except Exception,e:
        error = 'operation:getCurrentRequestCount,desc: could not retrieve the count of missed call alert requests for %s,error:%s' %(msisdn,str(e),)
        print error
        try:
            print 'Close DB Connection'
            cursor.close()
            resources['type'] =  'beat'
            action = 'failure'
            nameSpace = dbTemplate.substitute(package=action)
            resources['nameSpace'] = nameSpace
            sendMetric(resources)

        except Exception:
            pass
        raise e
        
    else:
        resources['type'] =  'beat'
        action = 'success'
        nameSpace = dbTemplate.substitute(package=action)
        resources['nameSpace'] = nameSpace
        sendMetric(resources) 
        if count == 0:
            return False
        elif count == 1:
            return result

def sendMessage(msisdn,recipient,message):
    '''sends the call me back message'''
    from config import countryCode
    from urllib import urlopen,urlencode
    try:
        from ussd.configs.core import kannel
    except ImportError, err:
        from configs.core import kannel
    try:
        from ussd.services.common.secure.secure import decrypt
    except ImportError, err:
        from services.common.secure.secure import decrypt
    recipient = '+%s%s' %(countryCode, str(recipient)[-9:])
    msisdn = '+'+msisdn
    user = decrypt(kannel['username'])
    password = decrypt(kannel['password'])
    args = urlencode({'smsc':'USSD','username':decrypt(kannel['username']),'password':decrypt(kannel['password']), 'from': msisdn,'to':str(recipient),'text':str(message)})
    try:
        url = 'http://127.0.0.1:14020/cgi-bin/sendsms?%s'%(args)
        print 'Sending \'%s\' From:%s, To:%s' %(message, str(msisdn), str(recipient))
        resp = urlopen(url).read()
    except Exception,e:
        error = 'operation:callMeBack.sendMessage,desc:%s-%s,error:%s' %(str(msisdn),str(recipient),str(e))
        print error
        raise e
    else:
        return resp


def isAirtel(resources):
    from ussd.postpaid.core import getSubscriberType
    from config import countryCode
    parameters = resources['parameters']
    recipient = parameters['recipient']
    parameters['msisdn'] = parameters['recipient']
    print str(countryCode),str(recipient)
    msisdn = str(parameters['msisdn'])[-9:]
    try:
        print "RECIPIENT without country code - %s" % str(msisdn)
        if str(msisdn).startswith('33'):
            return True
        else:
            return False
    except Exception, err:
	print 'operation:isAirtel. failed for %s. Error: %s' % (recipient, str(err))
	return False
	raise err

def validateRecipient(recipient):
    '''validate the recipient msisdn'''
    if not recipient.isdigit():
	return False
    if recipient[-9:][0] != '3':
        return False
    if len(recipient) < 9:
	return False
    return True

def sendCMBRequest(resources):
    '''sends call me back request from the originating msisdn to the specified msisdn'''
    from string import Template
    from datetime import datetime, timedelta
    from config import responses, messageSender
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    recipient = (parameters['recipient'].strip()).replace(' ','')
    parameters['recipient'] = recipient
    resources['parameters'] = parameters
    language = parameters['language']
    if not validateRecipient(recipient):
	respMessage = responses['wrongNumber'][language]
	sendMessage(messageSender, msisdn, respMessage)
	return respMessage
    if not isAirtel(resources):
	respMessage = responses['offnet'][language]
	sendMessage(messageSender, msisdn, respMessage)
	return respMessage
    parameters['msisdn'] = msisdn
    language = parameters['language']
    currentTime = datetime.now()
    expiry_date = currentTime + timedelta(days = int(1))
    count = getCurrentCount(resources)
    print str(count) + ":: count"
    if not count or int(count[1]) < 10:
        if not count:
            print 'in not count'
            sql = 'insert into service_call_me_back(id,msisdn,requests,expiry_date) values(service_cmb_sqc.nextval, :msisdn, :requests , :expiry_date)'
            params =  {'msisdn':msisdn, 'requests':1 ,'expiry_date':expiry_date}
            requests = '1' 
        elif int(count[1]) < 10:
            print 'in count < 10'
            sql = 'update service_call_me_back set requests = :requests where id = :id'
            params = {'requests':int(count[1])+1,'id':count[0]}
            requests = str((count[1])+1)
        msg = responses['b_party_message'][language] % msisdn
        sendMessage(msisdn, recipient, msg)
        response = Template((responses['True'])[language])
        resources['type'] =  'timer'
        resources['start'] = currentTime
        resources['nameSpace'] = dbTimeTemplate
        try:
            '''Connecting to DB: Updating the number of CMB requests done'''
            cursor = (resources['connections'].acquire()).cursor()
            cursor.execute(sql,params)
            cursor.connection.commit()
            cursor.close()
            print sendMetric(resources)
        except Exception,e:
            error = 'operation:callMeBack.sendCMBRequest,desc:failed to update database %s-%s,error:%s' %(str(msisdn),str(recipient),str(e),)
            print error
            try:
                print 'Close DB Connection'
                cursor.close()
                resources['type'] =  'beat'
                action = 'failure'
                nameSpace = dbTemplate.substitute(package=action)
                resources['nameSpace'] = nameSpace
                print sendMetric(resources)
            except Exception:
                pass
            raise e
        else:
            resources['type'] =  'beat'
            action = 'success'
            nameSpace = dbTemplate.substitute(package=action)
            resources['nameSpace'] = nameSpace
            print sendMetric(resources)

	    requestsdiff = str(10 - int(requests))
	    #if requestsdiff == '1':
		#partyA_message = Template(responses['one'][language]).substitute(requestsdiff=requestsdiff,recipient=recipient)
	    if requestsdiff == '0':
		partyA_message = Template(responses['zero'][language]).substitute(recipient=recipient)
            else:
		response = Template(responses['success'][language])
                partyA_message = response.substitute(requestsdiff=requestsdiff,recipient=recipient)
                partyA_message = check_time_between(resources, partyA_message)
	    sendMessage(messageSender, msisdn, partyA_message)
	    return partyA_message
    else:
        response = (responses['False'])[language]
        return response
def check_time_between(resources, a_party_message):
    """
    checks the time the request is sent and uses this result
    to determine the message to be sent to subscriber
    """
    from datetime import datetime, timedelta
    from config import responses,time_1, time_2
        

    language = resources['parameters']['language']
    recipient = resources['parameters']['recipient']
    time = datetime.now()
    time_now = str(time).split(' ')[0]
    print "TIME NOW : %s" % str(time_now)
    if time_1 <= time_now <= time_2:
        message = responses['message_1'][language] % str(recipient)
        return message
    else:
        return a_party_message


def setup():
    from cx_Oracle import SessionPool
    try:
        from configs.core import databases
        from services.common.secure.secure import decrypt
    except ImportError, err:
        from ussd.configs.core import databases
        from ussd.services.common.secure.secure import decrypt
    db = databases['core']
    user = decrypt(db['username'])
    password = decrypt(db['password'])
    resources = {}
    resources['connections'] = SessionPool(user, password, db['string'],10,50,5,threaded=True) 
    return resources

if __name__ == '__main__':
    resources = setup()
    parameters = {}
    parameters['msisdn'] = '261337272618'
    parameters['recipient'] = '261337272618'
    parameters['language'] = 'txt-2'
    resources['parameters'] = parameters
    #print getCurrentCount(resources)
    print sendCMBRequest(resources)
    #print airCheck(parameters['recipient'])
    #print isAirtel(resources)
    #print validateRecipient(parameters['recipient'].strip())
    #print sendMessage(parameters['msisdn'],parameters['recipient'],'hey there')
