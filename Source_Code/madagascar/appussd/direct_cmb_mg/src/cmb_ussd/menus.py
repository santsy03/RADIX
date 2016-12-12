#!/usr/bin/env python2.7
# coding: utf-8
from string import Template
from twisted.internet import defer
from datetime import datetime, timedelta
from direct_cmb_mg.src.config import  MESSAGES
from utilities.logging.core import log

class menu0():
    def processAction(self,resources):
        resources['currentMenu'] = 'home'
        return resources

class menu1():
    def __init__(self):
        pass

    def processAction(self,resources):
        return resources

    def start(self,resources):
        from direct_cmb_mg.src.common.core import invoke_cmb
        print "RESOURCES IN MENUS : %s" % str(resources)
        b_number = resources['parameters']['ussdRequestString']
        msisdn = resources['parameters']['msisdn']
        resources['parameters']['b_number'] = b_number
        language = resources['parameters']['language']
	try:
	    submit = invoke_cmb(resources)   # send CMB request
	except Exception,e:
	    error = ("Error: Desc:failed to send cmb request for") + (
		    " msisdn:%s, b_number:%s,error:%s") % (
			    str(msisdn), str(b_number), str(e) )
	    log( resources, error)
	    resources['cmb_status'] = '1'  #failure
	    self.menuTxt = MESSAGES[language]['failure_txt']
	else:
	    resources['cmb_status'] = '0'  #successful
	    self.menuTxt = submit
        print self.menuTxt
        resources['ussdResponseString'] = self.menuTxt
        resources['action']= 'end'
        return resources



menus = {'home':menu1,
        'start' : menu0
	}
if __name__ == '__main__':
    resources = {}
    resources['msisdn'] = '735267974'
    resources['parameters'] = {'msisdn':'254735267974','b_number':'67890098765'}
    test =menu1 ()
    print test.start(resources)
