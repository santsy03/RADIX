from urllib import urlencode,urlopen

def sendMessage(resources,message):
    '''sends the call me back message'''
    import urllib
    from urllib import urlopen,urlencode
    from configs.core import kannel
    from services.common.secure.secure import decrypt
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    recipient = parameters['recipient']
    recipient = '254%s'%(str(recipient[-9:]))
    message = message
    params = urllib.urlencode({'username': decrypt(kannel['user']), 'password': decrypt(kannel['password']), 'from': msisdn, 'to': recipient, 'text': message})
    print params
    try:
        #url = 'http://127.0.0.1:14020/cgi-bin/sendsms?%s'%(params)
        url = 'http://10.10.32.65:13013/cgi-bin/sendsms?%s'%(params)
	print url
        resp = urllib.urlopen(url)
        response = resp.read()
    except Exception,e:
        error = 'operation:callMeBack.sendMessage,desc:%s-%s,error:%s' %(str(msisdn),str(recipient),str(e))
        print error
        raise e
    else:
        return response

if __name__ == '__main__':
    resources = {}
    parameters = {}
    parameters['sender'] = '254735449662'
    parameters['msisdn'] = 'Radix'
    parameters['recipient'] = '254735449662'
    message = 'test message'
    resources['parameters'] = parameters
    print sendMessage(resources,message)
