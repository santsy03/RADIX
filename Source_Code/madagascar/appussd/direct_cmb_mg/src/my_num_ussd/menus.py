#!/usr/bin/env python2.7
# coding: utf-8
from string import Template
from twisted.internet import defer
from datetime import datetime, timedelta
from direct_cmb_mg.src.config import MESSAGES

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
        '''My Number Request'''
        msisdn = resources['parameters']['msisdn']
        msisdn = "+261%s" % str(msisdn[-9:])
        language = resources['parameters']['language']
        resources['ussdResponseString'] = \
            MESSAGES[language]['my_number_message'] % str(msisdn)
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
