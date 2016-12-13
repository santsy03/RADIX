#!/usr/bin/env python
#coding: utf-8

from configs.config import databases

eng = 'txt-1'
fr = 'txt-2'
ma = 'txt-3'
default_language = fr

AIR = {}
SQL = {}
BILL = {}
PORTS = {}
QUEUES = {}
THREADS = {}
METRICS = {}
MESSAGES = {}
TIMEOUTS = {}
WHITELIST = {}
DATABASES = {}
EXCEPTIONS = {}
APPLICATIONS = {}
STATUS_CODES = {}
USSD_MESSAGES = {}
ALLOWED_PACKAGES = {}

HOME = '/appussd/me2u/src'
#HOME = '/home/andrew/hg/mg_me2u/me2u/src'

SQL['log_transaction'] = 'insert into me2u (ID, MSISDN, RECIPIENT, BAL_BEFORE, BAL_AFTER, REC_BAL_BEFORE, REC_BAL_AFTER, REC_EXPIRY, STATUS, AMOUNT, CREATED_AT) values (ME2U_SEQ.NEXTVAL, :msisdn, :recipient, :bal_before, :bal_after, :rec_bal_before, :rec_bal_after, :rec_expiry, :status, :amount, :created_at)'
SQL['fetch_packages'] = 'select volume from provisioning_packages'

BILL['toggle'] = 'off'  #'on'
BILL['price'] = '1'

PORTS['ussd'] = '6328'
PORTS['flares'] = '6329'
#PORTS['flares'] = '5090'  # TEST

APPLICATIONS['prepaid'] = 'http://127.0.0.1:%s/' % PORTS['ussd']
APPLICATIONS['postpaid'] = ''

AIR['dedicated_account'] = 1011
#AIR['dedicated_account'] = 8
AIR['dedicated_account_action'] = ''
AIR['dedicated_account_factor'] = 100   # 1:100
AIR['externalData1'] = 'me2u'
AIR['externalData2'] = ''
AIR['action'] = 'adjustmentAmountRelative'

EXCEPTIONS['billing_error'] = 'Failed to bill on AIR.'
EXCEPTIONS['missingParameter'] = 'Parameter Missing: %s'
EXCEPTIONS['invalid_action'] = 'Invalid Action Invoked: %s'

QUEUES['core'] = 'me2u'
QUEUES[''] = ''

THREADS['core'] = 10
THREADS['ussd'] = 200
THREADS['flares'] = 200

TIMEOUTS['flares'] = '10'  #seconds 
TIMEOUTS['ussd'] = '10'    #seconds

STATUS_CODES['insufficient_data_balance'] = '1'
STATUS_CODES['amount_max'] = '2'
STATUS_CODES['amount_min'] = '3'
STATUS_CODES['no_bundle'] = '4'
STATUS_CODES['success'] = '5'
STATUS_CODES['insufficient_funds'] = '7'
STATUS_CODES['error'] = '0'
STATUS_CODES['volume_not_allowed'] = '8'

# minimum amount sub can share on me2u (in MBs)
MINIMUM_MB_ALLOWED = '5'

MESSAGES['0'] = 'There was an error processing your request'
MESSAGES['1'] = ''
MESSAGES['2'] = 'Desole, vous ne pouvez pas envoyer plus de 50% de votre forfait. Merci pour votre fidelite'
MESSAGES['3'] = 'Desole, vous ne pouvez pas envoyer moins de %sMo a un client. Merci pour votre fidelite' % MINIMUM_MB_ALLOWED
MESSAGES['4'] = 'Desole, vous devez d\'abord souscrire a un forfait internet'
#MESSAGES['5'] = 'Felicitation, vous venez d\'envoyer %s Mo au %s avec succes'
MESSAGES['5'] = 'Vous avez envoye %s Mo au %s. Merci d\'avoir utilise Internet CpourToi.'
MESSAGES['6'] = ''
MESSAGES['7'] = 'Vous avez suffisamment de fonds pour mener à bien cette transaction'
MESSAGES['8'] = 'Amount not allowed'

MESSAGES['recipient'] = {}
#MESSAGES['recipient']['success'] = 'Felicitation, vous venez de recevoir %s Mo du numero %s. Bonne utilisation'
MESSAGES['recipient']['success'] = 'Vous avez recu %s Mo du %s. Votre solde Internet est de %s Mo valable jusqu\'au %s'

USSD_MESSAGES['postpaid'] = 'Desole, seuls les clients prepaid peuvent utiliser ce service. Merci pour votre fidelite'
USSD_MESSAGES['not_whitelisted'] = 'Unknown Application'
USSD_MESSAGES['error'] = 'System is currently unavailable. please try again later.'
USSD_MESSAGES['defered_response'] = 'Veuillez patienter svp, votre demande est en cours de traitement.'

ALLOWED_PACKAGES['toggle'] = 'off'   #on

WHITELIST['msisdns'] = ['261336173681','261337827887','261337321372','261334613190']
WHITELIST['toggle'] = 'on'   #'off'

db = databases['core']
DATABASES['username'] = db['username']
DATABASES['password'] = db['password']
DATABASES['string'] = db['string'] 

METRICS['flares_hits'] = 'application.me2u.flares.hit'
METRICS['flares_failure'] = 'application.me2u.flares.failure'
METRICS['core_resp_time'] = 'application.me2u.service.response_time'
METRICS['air_getbalance'] = 'application.me2u.air.time'
METRICS['db_insert'] = 'application.me2u.db.insert.time'
METRICS['db_select'] = 'application.me2u.db.select.time'
METRICS['sms'] = 'application.me2u.sendSMS.time'
METRICS['failed_validation'] = 'application.me2u.validation_fail'
METRICS['passed_validation'] = 'application.me2u.validation_pass'
METRICS[''] = ''

error_ussd = ''

