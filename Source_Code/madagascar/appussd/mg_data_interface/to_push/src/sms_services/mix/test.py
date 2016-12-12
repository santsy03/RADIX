import httplib, urllib, urllib2

params = urllib.urlencode({
    'msisdn' :'261330465390',
    'packageId' : '1',
    'txt': 'mix',
    'auto_renewal': 'False',
    })

#conn = httplib.HTTPConnection("127.0.0.1:5000")
#conn.request("POST", "/process",
#             params)

url = "http://127.0.0.1:4050/process"
print url
print  params

#response = conn.getresponse()

resp = urllib2.urlopen(urllib2.Request(url, params))
#print response.status, response.reason
data = resp.read()
print data
#conn.close()
