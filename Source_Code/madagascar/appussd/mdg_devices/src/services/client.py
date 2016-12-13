#!/usr/bin/python2.7
# coding: utf-8
import urllib
import sys
ipport = '127.0.0.1:7867'
#msisdn = '261337073708'
msisdn = '261330891190'
transid = '98864'
ssid = 134356
rstr = sys.argv[2]
if sys.argv[1] != '':
    ssid = sys.argv[1]

params = urllib.urlencode({'msisdn': msisdn,'input':rstr,'TYPE':1})
f = urllib.urlopen("http://%s/process?%s" %(ipport,params))
print f.read()
