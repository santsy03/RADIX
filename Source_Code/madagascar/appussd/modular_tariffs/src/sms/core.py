__author__ = 'Andrew Kamau'

def validateText(text):
    '''Checks whether the message received conforms to the expected format'''
    import re
    from config import keywords as kw
    if text.isalpha() or text.isdigit():
        '''filter out non-alnum strings'''
        return [False]
    if not text.startswith(kw[0]): 
        '''filter out those that do not begin with key-word'''
        if not text.startswith(kw[1]):
            return [False]
    try:
        text_parts = text.partition(kw[0])
        if not text_parts[2]:
            text_parts = text.partition(kw[1])
        period = text_parts[1]
        plan = (text_parts[2]).strip()[0]
        magicNumber = (text_parts[2]).strip()[-8:]
    except Exception, err:
        print 'operation:validateText. Error: %s ' % str(err)
        raise err
    else:
        return [True, plan, period, magicNumber]

def processSmsRequest(resources):
    import modular_tariffs.src.configs as config
    from utilities.logging.core import log
    from config import USSD_RESPONSES
    from config import default_language
    language = default_language
    invalid_command = USSD_RESPONSES['invalid_command'][language]
    invalidCommand = invalid_command
    postpaidMessage = USSD_RESPONSES['postpaid'][language]
    from config import periodMapping as p_m
    from config import planMapping as m_p
    from sms import sendSMS as sendMessage
    from magicNumber.src.core import processRequest
    from magicNumber.src.flares.config import msisdns
    from metrics.config import magic_no_sms as sms_count
    from metrics.config import magic_no_sms_resp_time as sms_time
    from metrics.metricHandler import heartBeat as hb
    from datetime import datetime as dt
    st = dt.now()
    try:
        hb().beat(sms_count)
        print '[DEBUG] Metric sent: %s' % (str(sms_count))
    except:
        pass
    msisdn = str(resources['msisdn'])
    parameters = {}
    parameters['msisdn'] = msisdn
    resources['parameters'] = parameters
    type = getSubType(msisdn)
    if type != 'prepaid':
	response = postpaidMessage
	log(resources, sendMessage(resources, response))
	return response
    else:
        try:
            command = (resources['txt'].strip()).lower()
            if command == 'statut':
	            parameters['action'] = 'status'
	            resources['parameters'] = parameters
	            resp = processRequest(resources)
            elif command == 'stop':
	            parameters['action'] = 'unsubscribe'
	            resources['parameters'] = parameters
	            resp = processRequest(resources)
            else:
                validated = validateText(command)
                summ = 'MSISDN: %s -- Message: %s -- Validated: %s ' % (msisdn, command, str(validated[0]))
                log(resources, summ)
                if not validated[0]:
                    '''failed validation'''
                    summ = '%s -- %s' % (msisdn, invalidCommand)
                    log(resources, summ)
                    sendMessage(resources, invalidCommand)
                else:
                    plan = m_p[str(validated[1])]
                    period = p_m[str(validated[2])]
                    magicNo = validated[3]
                    parameters['period'] = period.strip()
                    parameters['plan'] = plan.strip()
                    parameters['magicNumber'] = magicNo.strip()
                    action = 'subscribe'
                    parameters['action'] = action
                    resources['parameters'] = parameters
                    resp = processRequest(resources)
                    try:
                        hb().period(sms_time, st)
                        print '[DEBUG] Metric sent: %s' % (str(sms_time))
                    except:
                        pass
        except:
            error = invalidCommand
            print '%s -- %s' % (msisdn, invalidCommand)
            response = error
            parameters = {'msisdn':msisdn}
            resources['parameters'] = parameters
            sendMessage(resources,str(error))
        else:
            response = command

def notifySubscriber(msisdn,msg):
    '''sends the sms feedback'''
    from urllib2 import urlopen,Request
    from urllib import urlencode
    url = 'http://10.10.32.97:14020/cgi-bin/sendsms?username=radix&pass=radix&'
    #url = 'http://10.10.32.65:13013/cgi-bin/sendsms?username=plabs&pass=plabs654&'
    #urlstring = urlencode({'smsc':'radixt','to':msisdn,'from':'767','text':msg})
    urlstring = urlencode({'smsc':'ussdmgn','to':msisdn,'from':'613','text':msg})
    nstring = urlstring.replace('%2A767%23','*767#')
    request = Request(url+nstring)
    print urlstring
    try:
        resp = (urlopen(request)).read().strip()
    except Exception,e:
        error = 'notifying subscriber failed %s:%s,msg:%s' %(msisdn,str(e),str(msg),)
        print error
        raise e
    else:
        print 'resp:%s,msisdn:%s' %(str(resp),str(msisdn))


def getSubType(msisdn):
    '''
    checks whether sub is prepaid or postpaid
    '''
    from magicNumber.src.ucip.airHandler import getBalanceAndDate
    try:
	resp = getBalanceAndDate(msisdn)
    except Exception,e:
	error = 'operation:getSubType failed for %s. Error: %s'%(msisdn,str(e))
	print error
	raise e
    else:
	if str(resp['responseCode']) == '0':
	    type = 'prepaid'
	else:
	    type = resp['responseCode']
	return type



if __name__ == '__main__':
    resources = {}
    resources['msisdn'] = '22798209806'
    #resources['txt'] = 'jour,unilateral,22796964700'
    resources['txt'] = 'JOUR 1 96123456'
    texts = ['Jour 1 96123456','Jour1 96123456','JOUR 1 96123456','jour 1 96123456','semaine196123456','SEMAINE2 96123456','Semaine 2 96123456']
    #resources['txt'] =  'invalid string'
    #for text in texts:
        #print validateText(text.lower())
    print processSmsRequest(resources)
