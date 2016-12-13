#!/usr/bin/env python
#coding: utf-8


CURRENT = 'prod'
DEBUG = True
CHANNEL = 'direct_cmb'

HOME = {}
HOME[CURRENT] = '/appussd/direct_cmb'
HOME['dev'] = '/appussd/test/direct_cmb'



ENV = {}
ENV['prod'] = {}
ENV['prod']['cmb_flares'] = 8767
ENV['prod']['cmb_ussd'] = 5551
ENV['prod']['my_num_flares'] = 6787 
#ENV['prod']['my_num_flares'] = 7070
ENV['prod']['my_num_ussd'] = 4441 

ENV['dev'] = {}
ENV['dev']['cmb_flares'] = ''
ENV['dev']['cmb_ussd'] = ''
ENV['dev']['my_num_flares'] = ''
ENV['dev']['my_num_ussd'] = '' 

PORTS = {}
PORTS['cmb_flares'] = ENV[CURRENT]['cmb_flares']
PORTS['cmb_ussd'] = ENV[CURRENT]['cmb_ussd']
PORTS['my_num_flares'] = ENV[CURRENT]['my_num_flares']
PORTS['my_num_ussd'] = ENV[CURRENT]['my_num_ussd']

THREADS = {}
THREADS['flares'] = 200
THREADS['ussd'] = 200

LOGS = {}
LOGS['flares'] = '%s/flares/logs' % HOME[CURRENT]
LOGS['ussd'] = '%s/ussd/logs' % HOME[CURRENT]

TIMEOUT = {}
TIMEOUT['ussd'] = 10  # timeout when calling ussd service
TIMEOUT['cmb'] = 5   # timeout when calling CMB service
TIMEOUT['language'] = 5   # timeout when calling language service


MESSAGES = {}
MESSAGES['txt-1'] = {}
MESSAGES['txt-2'] = {}
MESSAGES['txt-3'] = {}
MESSAGES['txt-1']['my_number_message'] = 'Dear customer, your number is %s'
MESSAGES['txt-2']['my_number_message'] = "Tompoko, ny nomeraonao dia %s"
MESSAGES['txt-3']['my_number_message'] = "Votre numero d'appel est %s"

MESSAGES['txt-1']['disallowed_txt'] = 'You are not allowed to use this service'
MESSAGES['txt-2']['disallowed_txt'] = '(mg)You are not allowed to use this service'
MESSAGES['txt-3']['disallowed_txt'] = '(fr)You are not allowed to use this service'

MESSAGES['txt-1']['failure_txt'] = 'Votre demande n\'a pas pu être traitee. S\'il vous plait reessayer plus tard.'
MESSAGES['txt-1']['failure_txt'] = '(mg)Votre demande n\'a pas pu être traitee. S\'il vous plait reessayer plus tard.'
MESSAGES['txt-1']['failure_txt'] = '(fr)Votre demande n\'a pas pu être traitee. S\'il vous plait reessayer plus tard.'

MESSAGES['txt-1']['invalid_number'] = '(Eng)Le numero que vous avez saisi est incorrect. S\'il vous plait ressayez avec un numero correct.'
MESSAGES['txt-2']['invalid_number'] = '(mg)Le numero que vous avez saisi est incorrect. S\'il vous plait ressayez avec un numero correct.'
MESSAGES['txt-3']['invalid_number'] = 'Le numero que vous avez saisi est incorrect. S\'il vous plait ressayez avec un numero correct.'

MESSAGES['txt-1']['successful_message'] = 'Your request has been sent to %s'
MESSAGES['txt-2']['successful_message'] = 'Your request has been sent to %s'
MESSAGES['txt-3']['successful_message'] = 'Your request has been sent to %s'


MSISDNS = ['261336173681','261330722156']

CMB = {}
CMB['port'] = '8001'
CMB['url'] = 'http://127.0.0.1:9097/process?%s'
CMB['action'] = 'cmb'
