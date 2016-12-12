import traceback
import xml.etree.ElementTree as ET

from xml.dom.minidom import parseString
from urllib import urlencode
from urllib2 import urlopen, URLError


def process_blackberry(resources):
    parameters = resources['parameters']
    sessionId = parameters['sessionId']
    ussd_body = parameters['ussd_body']
    msisdn = parameters['msisdn']
    service_key = 150
    key = str(service_key)
    try:
        url = 'http://172.25.129.32:8017/blackberry/ussdservice?'
        data = urlencode({'msisdn':msisdn, 'Ussd_Body':ussd_body, 'Service_Key':key})
        full_url = url + str(data)
        print full_url
        response = urlopen(full_url, data ="").read()
        #response = urlopen(full_url, data = data).read()
        print response

    except Exception, e:
        print traceback.format_exc()

    else:
        xmlData = ET.fromstring(response)  
        resp = xmlData[0][0][0][0][5][1][0].text
        return resp




if __name__ == '__main__':
    resources = {}
    params = {}
    #params['msisdn'] = '261338001184'
    #params['msisdn'] = '261330465390'
    params['msisdn'] = '261331005578'
    params['sessionId'] = '9998111511'
    params['ussd_body'] = '7'
    resources['parameters'] = params
    print process_blackberry(resources)
        
        
