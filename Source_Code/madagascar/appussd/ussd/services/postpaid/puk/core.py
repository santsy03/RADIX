import cx_Oracle
import socket
import traceback
from urllib import urlencode
from urllib2 import urlopen, URLError

from config import TIMEOUT, url
from ussd.configs.core import ipacs as databases
from ussd.services.common.secure.secure import decrypt

def ipacs_connect():
    try:
        connection = cx_Oracle.Connection(decrypt(databases['core']['username']),
        decrypt(databases['core']['password']),databases['core']['string'],threaded=True)

    except Exception, e:
        print traceback.format_exc()

    else:
        return connection



def process_get_puk_details(resources):
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    try:
        cursor = (ipacs_connect()).cursor()
        sql = ("select sim_puk_1, sim_puk_2 from cin_m_sim where sim_sim_no =\
              (select TEL_SIM_NO from cin_m_msisdn_mast where tel_msisdn_no = :nu)")
        param = {}
        param['nu'] = msisdn
        res = cursor.execute(sql, param).fetchall()[0][0]
       
    except Exception, e:
         print traceback.format_exc()

    else:
        return res

def process_puk(resources):
    parameters = resources['parameters']
    recipient = parameters['recipient']
    msisdn = parameters['msisdn']
    sessionId = parameters['sessionId']
    fdn = parameters['called_msisdn']
    language = parameters['language']
    socket.setdefaulttimeout(TIMEOUT)
    try:
        data = urlencode({'msisdn':recipient, 'countryId':'10008',
               'called_msisdn':fdn, 'msIsdn':'NULL'})
        resp = (urlopen(url, data)).read()
    
    except socket.timeout:
        print "%s|%sConnetion to PUK exceeded:%s"\
              %(str(msisdn), str(sessionId), str(TIMEOUT))
        return message

    except URLError, e:
        print "%s|%s|PUK url error:%s"\
              %(str(msisdn), str(sessionId), str(e))
        return message

    except Exception, e:
        print traceback.format_exc()
 
    else:
        return resp


if __name__ == '__main__':
    resources = {}
    parameters = {}
    parameters['msisdn'] = '261336173681'
    parameters['recipient'] = '333737373'
    parameters['called_msisdn'] = '332323233'
    parameters['sessionId'] = '876544'
    resources['parameters'] = parameters
    print process_puk(resources)
        

