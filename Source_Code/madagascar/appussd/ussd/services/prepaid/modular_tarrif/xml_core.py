#!/usr/bin/python2.4
import time, Cookie, os, shelve,sys
from datetime import datetime, timedelta
from xmlrpclib import ServerProxy, Transport, Error, ProtocolError
from ussd.metrics.config import dataPlanBalanceCheckTemplate,dataPlanBalanceCheckTimeTemplate
from ussd.metrics.sendmetric import  sendMetric
#from ussd.services.prepaid.modular_tarrif.xml_core import getModularTariffStatus
from datetime import datetime
import socket
from xmlrpclib import ServerProxy,Error


class SpecialTransport(Transport):
	def __init__(self, cookie = None):
		self.cookie = cookie 

        def send_content(self, connection, request_body):
                body = request_body.replace('\n','')
                body = body.replace("<?xml version='1.0'?>",'<?xml version="1.0" encoding="UTF-8"?>')
                connection.putheader("Content-Type", "text/xml",)
                connection.putheader("User-Agent", "ussdmenu",)
                connection.putheader("Authorization", "Basic testussdmenu",)
                #connection.putheader("Cookie", self.cookie)
                connection.putheader("Content-Length", str(len(body)))
                connection.endheaders()
                if request_body:
                        connection.send(body)

class CookieTransport(Transport):
	def request(self, host, handler, request_body, verbose=0):
		h = self.make_connection(host)
		if verbose:
			h.set_debuglevel(1)
		self.send_request(h, handler, request_body)
		self.send_host(h, host)
		self.send_user_agent(h)
		self.send_content(h, request_body)
		errcode, errmsg, headers = h.getresponse()
		errcode = 200
		cookies = self._get_cookies(headers)
                cok = None
                for cookie in cookies:
                        ck = str(cookie)
                        cok = ck.split(':')
                        cvalue = cok[1].strip()
                        if cvalue.startswith('YJSESSIONID'):
                                h.putheader("Cookie", cvalue)

		if errcode != 200:
			raise ProtocolError(
			host + handler,
			errcode, errmsg,
			headers
		)

		self.verbose = verbose

		try:
			sock = h._conn.sock
		except AttributeError:
			sock = None

		response = self._parse_response(h.getfile(), sock)
		if len(response) == 1:
			response = response[0]

		return response, cok

	def send_content(self, connection, request_body):
        	body = request_body.replace('\n','')
        	body = body.replace("<?xml version='1.0'?>",'<?xml version="1.0" encoding="UTF-8"?>')
        	connection.putheader("Content-Type", "text/xml")
                connection.putheader("User-Agent", "ussdmenu",)
                connection.putheader("Authorization", "Basic testussdmenu",)
        	#connection.putheader("Cookie", "JSESSIONID=08730887D71219F39CDA8F4EF935270D; Path=/blackberry")
        	connection.putheader("Content-Length", str(len(body)))
        	connection.endheaders()
        	if request_body:
            		connection.send(body)
	
	def _get_cookies(self, headers):
		import Cookie
		c = []
		for v in headers.getheaders('Set-Cookie'):
			c.append(Cookie.SimpleCookie(v))
		return c

def checkSession(msisdn,gws):
    print 'in check Session'
    cookie = Cookie.SimpleCookie()
    string_cookie = os.environ.get('HTTP_COOKIE')
    #Use time elapsed to delete old cookies
    message = None
    if not string_cookie:
        print 'in string_coo'
        sid = msisdn
        cookie['sid'] = sid
        message = None
    else:
        cookie.load(string_cookie)
        sid = cookie['sid'].value
    cookie['sid']['expires'] = 12 * 30 * 24 * 60 * 60   
    # The shelve module will persist the session data
    # and expose it as a dictionary
    session_dir = '/appussd/ussd/services/prepaid/modular_tarrif/session'
    session = shelve.open(session_dir + '/sess_' + sid, writeback=True)
    sessionid = session.get('sessionid')
    if sessionid != gws:
        os.system('rm %s/sess_%s'%(session_dir,sid))
    else:
        # Retrieve last visit time from the session
        lastvisit = session.get('lastvisit')
        if lastvisit:
            dates = time.gmtime(float(lastvisit))
            ddate = time.strftime('%Y-%m-%d %H:%M:%S',dates)
            now = datetime.now()
            #pd = todate-dates
            #pst = pd.seconds/60
            #pd = datetime.now() + timedelta(minutes=-4)
        jid = session.get('JSESSIONID')
        #print str(jid)+"jid"
        if jid:
            message = jid
    return message
    
def manageSession(msisdn, jsid,gws):
    cookie = Cookie.SimpleCookie()
    string_cookie = os.environ.get('HTTP_COOKIE')
    #Use time elapsed to delete old cookies
    if not string_cookie:
        sid = msisdn
        cookie['sid'] = sid
        message = 'New'
    else:
        cookie.load(string_cookie)
        sid = cookie['sid'].value
    cookie['sid']['expires'] = 12 * 30 * 24 * 60 * 60
   
    # The shelve module will persist the session data
    # and expose it as a dictionary
    session_dir = '/appussd/ussd/services/prepaid/modular_tarrif/session'
    session = shelve.open(session_dir + '/sess_' + sid, writeback=True)

    # Retrieve last visit time from the session
    lastvisit = session.get('lastvisit')
    if lastvisit:
        message = 'Old'        
        #   time.asctime(time.gmtime(float(lastvisit)))
    jid = session.get('JSESSIONID')
    if not jid and jsid != '':
        session['JSESSIONID'] = jsid
    session['sessionid'] = gws
    # Save the current time in the session
    session['lastvisit'] = repr(time.time())
    return message, jid

def getModularTariffStatus(resources):
    print 'in get modular tariff'
    url = 'http://172.25.128.100:80/status-provisioning/Subscription_request/process.do'
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    sessionId = parameters['sessionId']
    key = parameters['key']
    code = parameters['code']
    params = {}
    params['SEQUENCE'] = '0'
    params['END_OF_SESSION'] = 'FALSE'
    params['LANGUAGE'] = 'FRA'
    params['SESSION_ID'] = sessionId
    params['SERVICE_KEY'] = key
    params['MOBILE_NUMBER'] = msisdn
    params['USSD_BODY'] = code
    try:
	jsess = checkSession(msisdn,sessionId)
	if jsess:
            print 'in jsess'
	    selection = parameters['selection']
	    params['USSD_BODY'] = selection
            resources['type'] = 'timer'
            resources['start'] = datetime.now()
            resources['nameSpace'] = dataPlanBalanceCheckTemplate.substitute(key=key) 
	    server = ServerProxy(url, transport=SpecialTransport(cookie=jsess), verbose=True)
            socket.setdefaulttimeout(5)
	    response = server.USSD_MESSAGE(params)
            sendMetric(resources)
	else:
            print 'in the else'
            resources['type'] = 'timer'
            resources['start'] = datetime.now()
            resources['nameSpace'] = dataPlanBalanceCheckTimeTemplate.substitute(key=key) 
            server = ServerProxy(url, transport=SpecialTransport(cookie=jsess), verbose=True)
            socket.setdefaulttimeout(5)
            response = server.USSD_MESSAGE(params)
            sendMetric(resources)
            print 'response:::'+ str(response)
            manageSession(msisdn,sessionId,sessionId)
    except ProtocolError, err:
        print err
        resources['type'] = 'beat'
        request = 'balance_check'
        action = 'failure'
        resources['nameSpace'] = dataPlanBalanceCheckTemplate.substitute(package=action,request=request,key=key)
        sendMetric(resources) 
    else:
        resources['type'] = 'beat'
        request = 'balance_check'
        action = 'success'
        resources['nameSpace'] = dataPlanBalanceCheckTemplate.substitute(package=action,request=request,key=key)
        sendMetric(resources) 
        return response

if __name__ == '__main__':
    ssid = 134356
    rstr = sys.argv[2]
    if sys.argv[1] != '':
        ssid = sys.argv[1]
    print 'session %s | input %s'%(ssid,rstr)
    resources = {'parameters':{'msisdn':'261337272168','sessionId':ssid,'selection':rstr}}
    print getModularTariffStatus(resources)
