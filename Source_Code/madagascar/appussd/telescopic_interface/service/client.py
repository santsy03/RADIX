from urllib import urlencode
from urllib2 import urlopen

url = "http://127.0.0.1:4045/process?"

def call_service():
    msisdn = '261330465390'
    package = '59'
    can_renew = '0'
    data = urlencode({'msisdn':msisdn, 'package_id':package,
        'can_renew':can_renew})
    try:
        full_url = url + str(data)
        resp = urlopen(full_url)

    except Exception, e:
        raise e

    else:
        print resp.read()

if __name__ == '__main__':
    print call_service()
