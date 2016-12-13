import httplib, urllib, urllib2

params = urllib.urlencode({
    'msisdn' :'261330465390',
    'packageId' : '0',
    'action': 'stop',
    'auto_renewal': '0',
    'channel': 'gui'
    })
headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept': 'text/plain'}
conn = httplib.HTTPConnection("127.0.0.1:8787")
conn.request("POST", "/process", params, headers)

url = "http://127.0.0.1:8787/process"
print url
print  params

resp = conn.getresponse()

#resp = urllib2.urlopen(urllib2.Request(url, params))
#print response.status, response.reason
data = resp.read()
print data
#conn.close()
