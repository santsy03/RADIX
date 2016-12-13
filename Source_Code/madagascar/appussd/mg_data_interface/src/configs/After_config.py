#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
config for the madagascar data interface

'''

from string import Template

HOST_NAME = __import__('socket').gethostname()

CWD = "/appussd/mg_data_interface/src/consumer"                           
LOG_NAME = "data_responselog-{}".format(HOST_NAME)
PID_FILE = '/appussd/mg_data_interface/src/consumer/data_prov_daemon-{}.pid'.format(HOST_NAME)
 
MEG_CWD = "/appussd/mg_data_interface/src/megfiftn_consumer"                       
MEG_LOG_NAME = "meg_responselog-{}".format(HOST_NAME)
MEG_PID_FILE = '/appussd/mg_data_interface/src/megfiftn_consumer/meg15_daemon-{}.pid'.format(HOST_NAME)


DEBUG = True
MIN_AMOUNT = 5
DA_FACTOR = 100
DA_ACTION = 'dedicatedAccountValueNew'
DA_ID = 8
WORKERS = 30
DEBUG = False

MAX_PURCHASES_PER_BLOCK = 2
BUY_KEYWORD = 'mix'
STOP_KEYWORD = 'stop'

SERVICE_ID = 2

NOW_SMS_EVENT_ID = 1
THIRD_DAY_SMS_EVENT_ID = 4
DAY_OF_RENEWAL_EVENT_ID = 5

RENEW_EVENT_ID = 2

MSISDN_LENGTH = 8

ALLOWED_PREFIXES = ['76','77','66','74','75','65','64']

 
BARRED_AFTERNOON_QUOTA = 91
BARRED_MORNING_QUOTA = 92
TIME_BARRED = 93
 

SPECIAL_NUMBERS = ['261330465390']
#SPECIAL_NUMBERS = ['22667102208','22667088086','22666201744','22666009090','22677717415','22677717390','22667125657','22677717378','22677717399','22677717392','22674345604','22666201745','22667088085','22675059211','22674437923','22667125657','22674344369','22674345604','22667125658']

PROVISION_URL =  "http://127.0.0.1:9002/submitProvision?"
BALANCE_URL =  "http://127.0.0.1:9002/submitProvision?"
FREQUENCY  =  3

ACK = {}


ACK['txt-1'] = "Eto ampanatontosana ny fangatahanao. Mahandrasa kely azafady. Misaotra tompoko."
ACK['txt-2'] = "We have recieved your request, please wait as we process it"
ACK['postpaid'] = "Cher client vous n'etes pas autorise a acceder a ce service"
ACK['wrong_mix'] = "Raha mila fanampim-panazavana dia antsoy ny sampana mpikarakara ny mpanjifa. Misaotra tompoko"
ACK['wrong_class'] = "Tompoko, tsy tontosa ny fangatahanao. Ny tolotra RTA mix dia natokana ho an ny mpanjifa RTA Mobile.Misaotra tompoko"
ACK['wrong_rec'] = "Le nombre que vous avez envoyez n'est pas valide"
ACK['wrong_amount'] = "Le montant que vous envoyer n'est pas valide"
ACK['wrong'] = "demande meconnu"


MESSAGES = {}
MESSAGES['subscriber'] ={}
MESSAGES['subscriber']['same'] = "chere client vous ne pouvez pas ajoutez votre numero comme numero magique"
MESSAGES['subscriber']['is_barred'] = "Desole vous ne pouvez pas souscrire ce numero a numero magique"

#metrics
HITS = 'application.mg_data.hits.ussd'
INSERT_METRIC = 'application.mg_data.hits.ussd'
INSERT_CDR_METRIC = 'application.mg_data.hits.meg.cdrinsert'
UPDATE_CDR_METRIC = 'application.mg_data.hits.meg.trackerupdate'

SUCCESS_HIT = "application.internet.success.%s"
FAIL_HIT = "application.internet.fail.%s"

AUTH_KEY = 'modularP4ss'
ACCOUNT_ID = 'modular'
ROUTING_KEY = 'mg_data'
MEG_KEY = 'meg_fiftn'

MEG_QUEUES = {}
MEG_QUEUES['test'] = 'test_megfiftn_queue'
MEG_QUEUES['prod'] = 'megfiftn_queue'

QUEUES = {}
QUEUES['test'] = 'test_mg_data_interface_queue'
QUEUES['prod'] = 'mg_data_interface_queue'



#=============Start of double data promotion bundles==================
bonusMsgs = {}
bonusMsgs['131'] = {}
bonusMsgs['131']['txt-1'] = "You have successfully subscribed to MyMeg250.You have 250MB valid 7days and Bonus 250MB valid 7 days.Press *999*141# to check remaining balance"
bonusMsgs['131']['txt-2'] = "Tafiditra ny MyMeg250: 250Mo ampiasaina internet manankery 7andro sy bonus 250Mo manankery 7andro. Tsindrio ny *999*141# raha hijery ny Mo na Ko azo ampiasaina."
bonusMsgs['131']['txt-3'] = "L'offre MyMeg250 a ete effectue avec succes: 250Mo d internet valable 7jours et 250Mo de bonus internet valable 7jours. Consultation forfait, tapez *999*141#."

bonusMsgs['132'] = {}
bonusMsgs['132']['txt-1'] = "You have successfully subscribed to MyMeg500.You have 500MB valid 7days and Bonus 500MB valid 7 days.Press *999*141# to check remaining balance."
bonusMsgs['132']['txt-2'] = "Tafiditra ny MyMeg500: 500Mo ampiasaina internet manankery 7andro sy bonus 500Mo manankery 7andro. Tsindrio ny *999*141# raha hijery ny Mo na Ko azo ampiasaina."
bonusMsgs['132']['txt-3'] = "L'offre MyMeg500 a ete effectue avec succes: 500Mo d internet valable 7jours et 500Mo de bonus internet valable 7jours. Consultation forfait, tapez *999*141#."

bonusMsgs['133'] = {}
bonusMsgs['133']['txt-1'] = "You have successfully subscribed to MyGig1.You have 1GB valid 30days and Bonus 1GB valid 7 days.Press *999*141# to check remaining balance."
bonusMsgs['133']['txt-2'] = "Tafiditra ny MyGig1: 1Go ampiasaina internet manankery 30andro sy bonus 1Go manankery 7andro. Tsindrio ny *999*141# raha hijery ny Mo na Ko azo ampiasaina."
bonusMsgs['133']['txt-3'] = "L'offre MyGig1 a ete effectue avec succes: 1Go d internet valable 30jours et 1Go de bonus internet valable 7jours. Consultation forfait, tapez *999*141#."

#===========End of double data promotion bundles=====================
#===========Replacing temporary messgaes ===================
newMsgs = {}
#newMsgs['32'] = {}
#newMsgs['32']['txt-1'] = "You have succesfully subscribed to MyMeg20 Night: 20Mb valid for 1 night. Dial *999*103# to check remaining balance. Thank you."
#newMsgs['32']['txt-2'] = "Tafiditra ny MyMeg20Night: 20Mo ampiasaina internet manankery 1alina. Tsindrion ny *999*103# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."
#newMsgs['32']['txt-3'] = "L'offre MyMeg20 Night a ete effectue avec succes: 20Mo valable 1 nuit. Tapez *999*103# pour consulter le forfait restant. Merci."

newMsgs['32'] = {}
newMsgs['32'][1] = "Tafiditra ny MyMeg20Night: 20Mo ampiasaina internet @ 9ora alina-12ora alina. Tsindrion ny *999*103# ahafantaranao ny Kiloctet sy Megaoctet azo ampiasaina."
newMsgs['32'][2] = "Tafiditra ny MyMeg20Night: 20Mo ampiasaina internet @ 12ora alina-5ora maraina. Tsindrion ny *999*103# ahafantaranao ny Kiloctet sy Megaoctet azo ampiasaina."

'''
newMsgs['32'] = {}
newMsgs['32'][1] = {}
newMsgs['32'][1]['txt-1'] = "Tafiditra ny MyMeg20Night: 20Mo ampiasaina internet @ 9ora alina-12ora alina. Tsindrion ny *999*103# ahafantaranao ny Kiloctet sy Megaoctet azo ampiasaina."
newMsgs['32'][1]['txt-2'] = "Tafiditra ny MyMeg20Night: 20Mo ampiasaina internet @ 9ora alina-12ora alina. Tsindrion ny *999*103# ahafantaranao ny Kiloctet sy Megaoctet azo ampiasaina."
newMsgs['32'][1]['txt-3'] = "Tafiditra ny MyMeg20Night: 20Mo ampiasaina internet @ 9ora alina-12ora alina. Tsindrion ny *999*103# ahafantaranao ny Kiloctet sy Megaoctet azo ampiasaina."
newMsgs['32'][2] = {}
newMsgs['32'][2]['txt-1'] = "Tafiditra ny MyMeg20Night: 20Mo ampiasaina internet @ 12ora alina-5ora maraina. Tsindrion ny *999*103# ahafantaranao ny Kiloctet sy Megaoctet azo ampiasaina."
newMsgs['32'][2]['txt-2'] = "Tafiditra ny MyMeg20Night: 20Mo ampiasaina internet @ 12ora alina-5ora maraina. Tsindrion ny *999*103# ahafantaranao ny Kiloctet sy Megaoctet azo ampiasaina."
newMsgs['32'][2]['txt-3'] = "Tafiditra ny MyMeg20Night: 20Mo ampiasaina internet @ 12ora alina-5ora maraina. Tsindrion ny *999*103# ahafantaranao ny Kiloctet sy Megaoctet azo ampiasaina."
'''
newMsgs['33'] = {}
newMsgs['33']['txt-1'] = "You have succesfully subscribed to MyMeg50 Night: 50Mb valid for 1 night. Dial *999*103# to check remaining balance. Thank you."
newMsgs['33']['txt-2'] = "Tafiditra ny MyMeg50Night: 50Mo ampiasaina internet manankery 1alina. Tsindrion ny *999*103# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."
newMsgs['33']['txt-3'] = "L'offre MyMeg50 Night a ete effectue avec succes: 50Mo valable 1 nuit. Tapez *999*103# pour consulter le forfait restant. Merci."

newMsgs['35'] = {}
newMsgs['35']['txt-1'] = "You have succesfully subscribed to MyMeg100 Night: 100Mb valid for 3 nights. Dial *999*103# to check remaining balance. Thank you."
newMsgs['35']['txt-2'] = "Tafiditra ny MyMeg100Night: 100Mo ampiasaina internet manankery 3alina. Tsindrion ny *999*103# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."
newMsgs['35']['txt-3'] = "L'offre MyMeg100 Night a ete effectue avec succes: 100Mo valable 3 nuits. Tapez *999*103# pour consulter le forfait restant. Merci."

newMsgs['4'] = {}
newMsgs['4']['txt-1'] = "You are successfully subscribed to MyMeg50: 50Mb valid 1 day and 25Mb of BONUS to be used from 11pm to 05:59am. Press *999*114# to check remaining balance."
newMsgs['4']['txt-2'] = "Tafiditra ny MyMeg50: ahazoana 50Mo ampiasaina internet h@ 12ora alina sy BONUS 25Mo ampiasaina @ 11ora alina - 06ora maraina. Megaoctet  tavela: *999*114#."
newMsgs['4']['txt-3'] = "La souscription a MyMeg50 a ete effectuee avec succes: c est 50Mo utilisable 1 jour et un BONUS de 25Mo, valable de 23h a 05h59. Solde restant: *999*114#."

newMsgs['6'] = {}
newMsgs['6']['txt-1'] = "You are successfully subscribed to MyMeg100: 100Mb valid 7 days and 100Mb of BONUS to be used from 11pm to 05:59am. Press *999*114# to check remaining balance."
newMsgs['6']['txt-2'] = "Tafiditra ny MyMeg100: ahazoana 100Mo ampiasaina internet mandritra ny 7 andro sy BONUS 100Mo ampiasaina @ 11ora alina-06ora maraina. Megaoctet tavela:*999*114#."
newMsgs['6']['txt-3'] = "La souscription a MyMeg100 a ete effectuee avec succes: c est 100Mo valable en 7 jours et un BONUS de 100Mo, valable de 23h a 05h59. Solde restant: *999*114#"

newMsgs['8'] = {}
newMsgs['8']['txt-1'] = "You are successfully subscribed to MyMeg250: 250Mb valid 7 days and 200Mb of BONUS to be used from 11pm to 05:59am. Press *999*114# to check remaining balance."
newMsgs['8']['txt-2'] = "Tafiditra ny MyMeg250: ahazoana 250Mo ampiasaina internet mandritra ny 7 andro sy BONUS 200Mo ampiasaina @ 11ora alina-06ora maraina. Megaoctet tavela:*999*114#."
newMsgs['8']['txt-3'] = "La souscription a MyMeg250 a ete effectuee avec succes: c est 250Mo valable en 7 jours et un BONUS de 200Mo, valable de 23h a 05h59. Solde restant: *999*114#."

newMsgs['9'] = {}
newMsgs['9']['txt-1'] = "You are successfully subscribed to MyMeg500: 500Mb valid 7 days and 300Mb of BONUS to be used from 11pm to 05:59am. Press *999*114# to check remaining balance."
newMsgs['9']['txt-2'] = "Tafiditra ny MyMeg500: ahazoana 500Mo ampiasaina internet mandritra ny 7 andro sy BONUS 300Mo ampiasaina @ 11ora alina-06ora maraina. Megaoctet tavela:*999*114#."
newMsgs['9']['txt-3'] = "La souscription a MyMe500 a ete effectuee avec succes: c est 500Mo valable en 7 jours et un BONUS de 300Mo, valable de 23h a 05h59. Solde restant: *999*114#."

newMsgs['11'] = {}
newMsgs['11']['txt-1'] = "You are successfully subscribed to MyGig1: 1Gb valid 30 days and 2Gb of BONUS to be used from 11pm to 05:59am. Press *999*114# to check remaining balance."
newMsgs['11']['txt-2'] = "Tafiditra ny MyGig1: ahazoanao 1Go ampiasaina mandritra ny 30 andro sy BONUS 2Go ampiasaina @ 11ora alina-06 ora maraina. Megaoctet  tavela:*999*114#."
newMsgs['11']['txt-3'] = "La souscription a MyGig1 a ete effectuee avec succes: c est 1Go valable en 30 jours un BONUS de 2Go, valable de 23h a 05h59. Solde restant: *999*114#."

newMsgs['12'] = {}
newMsgs['12']['txt-1'] = "You have succesfully subscribed to MyGig2: 2Gb valid for 30 days. Dial *999*114# to check remaining balance. Thank you."
newMsgs['12']['txt-2'] = "Tafiditra ny MyGig2: 2Go ampiasaina internet manankery 30andro. Tsindrion ny *999*114# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."
newMsgs['12']['txt-3'] = "L'offre MyGig2 a ete effectue avec succes: 2Go valable 30 jours. Tapez *999*114# pour consulter le forfait restant. Merci."

newMsgs['14'] = {}
newMsgs['14']['txt-1'] = "You are successfully subscribed to MyGig5: 5Gb valid 30 days and 5Gb of BONUS to be used from 11pm to 05:59am. Press *999*114# to check remaining balance."
newMsgs['14']['txt-2'] = "Tafiditra ny MyGig5: ahazoanao 5Go ampiasaina mandritra ny 30 andro sy BONUS 5Go ampiasaina @ 11ora alina-06 ora maraina. Megaoctet  tavela:*999*114#."
newMsgs['14']['txt-3'] = "La souscription a MyGig5 a ete effectuee avec succes: c est 5Go valable en 30 jours et un BONUS de 5Go, valable de 23h a 05h59. Solde restant: *999*114#."

newMsgs['15'] = {}
newMsgs['15']['txt-1'] = "You are successfully subscribed to MyGig10: 10Gb valid 30 days and 10Gb of BONUS to be used from 11pm to 05:59am. Press *999*114# to check remaining balance."
newMsgs['15']['txt-2'] = "Tafiditra ny MyGig10: ahazoanao 10Go ampiasaina mandritra ny 30 andro sy BONUS 10Go ampiasaina @ 11ora alina-06 ora maraina. Megaoctet  tavela:*999*114#."
newMsgs['15']['txt-3'] = "La souscription a MyGig10 a ete effectuee avec succes: 10Go valable en 30 jours et un BONUS de 10Go, valable de 23h a 05h59. Solde restant: *999*114#."


newMsgs['16'] = {}
newMsgs['16']['txt-1'] = "You have succesfully subscribed to MyGig30: 30Gb valid for 30 days. Dial *999*114# to check remaining balance. Thank you."
newMsgs['16']['txt-2'] = "Tafiditra ny MyGig30: 30Go ampiasaina internet manankery 30andro. Tsindrion ny *999*114# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."
newMsgs['16']['txt-3'] = "L'offre MyGig30 a ete effectue avec succes: 30Go valable 30 jours. Tapez *999*114# pour consulter le forfait restant. Merci."


#newMsgs['19'] = {}
#newMsgs['19']['txt-1'] = "You have succesfully subscribed to Facebook offer: 75Mb valid for 1 day. Dial *999*36# to check remaining balance. Thank you."
#newMsgs['19']['txt-2'] = "Tafiditra ny tolotra Facebook: 75Mo hanaovana Facebook manankery 1 andro . Tsindrion ny *999*36# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."
#newMsgs['19']['txt-3'] = "L'offre Facebook a ete effectue avec succes: 75Mo valable 1 jour. Tapez *999*36# pour consulter le forfait restant. Merci."
newMsgs['19'] = {}
newMsgs['19']['txt-1'] = "Tafiditra ny tolotra Facebook manankery 1 andro. Tsindrion ny *999*36# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."
newMsgs['19']['txt-2'] = "Tafiditra ny tolotra Facebook manankery 1 andro. Tsindrion ny *999*36# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."
newMsgs['19']['txt-3'] = "Tafiditra ny tolotra Facebook manankery 1 andro. Tsindrion ny *999*36# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."

#newMsgs['20'] = {}
#newMsgs['20']['txt-1'] = "You have succesfully subscribed to Twitter offer: 75Mb valid for 1 day. Dial *999*37# to check remaining balance. Thank you."
#newMsgs['20']['txt-2'] = "Tafiditra ny tolotra Twitter: 75Mo hanaovana Twitter manankery 1 andro . Tsindrion ny *999*37# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."
#newMsgs['20']['txt-3'] = "L'offre Twitter a ete effectue avec succes: 75Mo valable 1 jour. Tapez *999*37# pour consulter le forfait restant. Merci."
newMsgs['20'] = {}
newMsgs['20']['txt-1'] = "Tafiditra ny tolotra Twitter manankery 1 andro. Tsindrion ny *999*37# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."
newMsgs['20']['txt-2'] = "Tafiditra ny tolotra Twitter manankery 1 andro. Tsindrion ny *999*37# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."
newMsgs['20']['txt-3'] = "Tafiditra ny tolotra Twitter manankery 1 andro. Tsindrion ny *999*37# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."

#newMsgs['21'] = {}
#newMsgs['21']['txt-1'] = "You have succesfully subscribed to Whatsapp offer: 75Mb valid for 1 day. Dial *999*38# to check remaining balance. Thank you."
#newMsgs['21']['txt-2'] = "Tafiditra ny tolotra Whatsapp: 75Mo hanaovana Whatsapp manankery 1 andro . Tsindrion ny *999*38# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."
#newMsgs['21']['txt-3'] = "L'offre Whatsapp a ete effectue avec succes: 75Mo valable 1 jour. Tapez *999*38# pour consulter le forfait restant. Merci."
newMsgs['21'] = {}
newMsgs['21']['txt-1'] = "Tafiditra ny Tolotra Whatsapp manankery 1 andro. Tsindrion ny *999*38# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."
newMsgs['21']['txt-2'] = "Tafiditra ny Tolotra Whatsapp manankery 1 andro. Tsindrion ny *999*38# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."
newMsgs['21']['txt-3'] = "Tafiditra ny Tolotra Whatsapp manankery 1 andro. Tsindrion ny *999*38# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."

newMsgs['119'] = {}
newMsgs['119']['txt-1'] = "Your subscription to Internet Mlay was performed with success, valid till 11:59PM. Thank you."
newMsgs['119']['txt-2'] = "Tontosa ny fangatahanao hampiasa ny tolotra Internet Mlay, manakery hatramin ny 11:59 alina. Misaotra tompoko."
newMsgs['119']['txt-3'] = "Votre souscription a l'offre Internet Mlay a ete effectuee avec succes, valable jusqu a 23h59. Merci."


#===========End of replacing temporary messgaes ===================

#====Names of above package ids==============
'''
tempMsgs = {}
tempMsgs[MyMeg 15][1]
tempMsgs[MyMeg 50][4]  
tempMsgs[MyMeg 100][6] 
tempMsgs[MyMeg 250][8]
tempMsgs[MyMeg 500][9]
tempMsgs[MyGig 1][11]
tempMsgs[MyGig 2][12]
tempMsgs[MyGig 5][14]
tempMsgs[MyGig 10][15]
tempMsgs[MyGig 30][16]
tempMsgs[Facebook][19]
tempMsgs[Twitter][20]
tempMsgs[Whatsapp][21]
tempMsgs[MyMeg 50(GIFT)][22]
tempMsgs[MyMeg 100(GIFT)][23]
tempMsgs[MyMeg 250(GIFT)][24]
tempMsgs[MyMeg 500(GIFT)][25]
tempMsgs[MyGig 1(GIFT)][26]
tempMsgs[MyGig 2GIFT)][27]
tempMsgs[MyGig 5(GIFT)][28]
tempMsgs[MyGig 10(GIFT)][30]
tempMsgs[MyGig 30(GIFT)][30]
tempMsgs[MyMeg 15 (GIFT)][121]
tempMsgs[Facebook (GIFT)][122]
tempMsgs[Twitter (GIFT)][123]
tempMsgs[Whatsapp (GIFT)][124]
tempMsgs[MyMeg 50(NIGHT)][33]
tempMsgs[MyMeg 100(NIGHT)][35]
tempMsgs[Regional][119]

'''
#====End of Names================================================================

MESSAGES['success'] = Template("Tontosa ny fangatahanao. Tsindrio ny *999*55# raha hijery ireo isa efa azonao @ Promo Mifety 55. Misaotra tompoko")

MESSAGES['success_15'] = "Tafiditra ny MyMeg15 ahazoanao 15Mo ampiasaina internet. Fijerena Mo tavela: tsindrio ny *999*114#. Misaotra tompoko"

MESSAGES['success_15_morn'] = "Tafiditra ny Mymeg15: 15Mo ampiasaina internet hatr@12 ora. Tsindrio ny *999*114# ahafantaranao ny Kilooctet sy ny megaoctet sisa azo ampiasaina."
#MESSAGES['success_15_morn']= {}
#MESSAGES['success_15_morn']['txt-1'] = "You have succesfully subscribed to MyMeg10: 10Mb valid till 12pm. Dial *999*114# to check remaining balance. Thank you."
#MESSAGES['success_15_morn']['txt-2'] = "Tafiditra ny MyMeg10 ahazoanao 10Mo hanaovana internet hatramin ny 12ora atoandro. Fijerena Mo tavela: tsindrio ny *999*114#. Misaotra tompoko."
#MESSAGES['success_15_morn']['txt-3'] = "L'offre MyMeg10 a ete effectue avec succes: 10Mo valable jusqu a 12h. Tapez *999*114# pour consulter le forfait restant. Merci."

#MESSAGES['success_15_morn']= {}
#MESSAGES['success_15_morn']['txt-1'] = "Tafiditra ny Mymeg15: 15Mo ampiasaina internet hatr@12 ora. Tsindrio ny *999*114# ahafantaranao ny Kilooctet sy ny megaoctet sisa azo ampiasaina."
#MESSAGES['success_15_morn']['txt-2'] = "Tafiditra ny Mymeg15: 15Mo ampiasaina internet hatr@12 ora. Tsindrio ny *999*114# ahafantaranao ny Kilooctet sy ny megaoctet sisa azo ampiasaina."
#MESSAGES['success_15_morn']['txt-3'] = "Tafiditra ny Mymeg15: 15Mo ampiasaina internet hatr@12 ora. Tsindrio ny *999*114# ahafantaranao ny Kilooctet sy ny megaoctet sisa azo ampiasaina."

MESSAGES['success_15_afte'] = "Tafiditra ny MyMeg15 ahazoanao 15Mo ampiasaina internet hatr@ 5 ora. Tsindrion ny *999*114# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."

#MESSAGES['success_15_afte'] = {}
#MESSAGES['success_15_afte']['txt-1'] = "You have succesfully subscribed to MyMeg10: 10Mb valid till 5pm. Dial *999*114# to check remaining balance. Thank you."
#MESSAGES['success_15_afte']['txt-2'] = "Tafiditra ny MyMeg10 ahazoanao 10Mo hanaovana internet hatramin ny 5 ora hariva. Fijerena Mo tavela: tsindrio ny *999*114#. Misaotra tompoko."
#MESSAGES['success_15_afte']['txt-3'] = "L'offre MyMeg10 a ete effectue avec succes: 10Mo valable jusqu a 17h. Tapez *999*114# pour consulter le forfait restant. Merci."
#MESSAGES['success_15_afte']['txt-2'] = "Tafiditra ny MyMeg15: 15Mo ampiasaina internet hatr@ 5 ora. Miampy 10 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."
#MESSAGES['success_15_afte']['txt-1'] = "Tafiditra ny MyMeg15: 15Mo ampiasaina internet hatr@ 5 ora. Miampy 10 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."
#MESSAGES['success_15_afte']['txt-3'] = "Tafiditra ny MyMeg15: 15Mo ampiasaina internet hatramin ny 5 ora. Tsindrion ny *999*114# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."

MESSAGES['success_15_french'] = "Votre demande a ete executee. Vous avez 15Mo d'internet. Tapez *999*114# pour connaitre les Mo restants.Merci"

MESSAGES['time_barred'] = "Ny fidirana amin io tolotra io dia misokatra hatramin ny 5 ora hariva ihany. Manasa anao hampiasa Mymeg 50 *114*4#. Misaotra tompoko."

MESSAGES['time_barred_french'] = "Cher client,votre demande n a pas ete executee. Vous pouvez souscrire a MyMeg15 de 8h-12h et de 13h-17h. Merci"

MESSAGES["time_barred_bparty"] = "Chere client, on ne peut pas pourchaser MyMeg15 pour votre ami parceque il est disponible seulement de 8h-12h et de 13h-17h Merci"

MESSAGES["morning_barred"] = "Tompoko, tsy tontosa ny fangatahanao. Manomboka amin ny 1ora-5ora no hahafahanao miditra indray amin ny MyMeg15 . Misaotra tompoko"
MESSAGES["morning_barred_french"] = "Cher client,v otre demande n a pas ete executee. Vous pouvez souscrire a nouveau de 13h jusqu a 17h. Merci"

MESSAGES["afternoon_barred"] = "Tompoko, tsy tontosa ny fangatahanao. Efa feno ny hahafahanao mampiasa io tolotra io androany. Misaotra tompoko "
MESSAGES["afternoon_barred_french"] = "Cher client,votre demande n a pas ete executee. Vous avez atteint le nombre de souscription autorise pour ce jour. Merci"

MESSAGES['success_night'] = Template("Tontosa ny fangatahanao. Ianao dia manana $data hanaovana internet. Tsindrio ny *999*103# ahafantaranao ny ambiny afaka ampiasainao. Misaotra tompoko")

MESSAGES['social'] = Template("Tontosa ny fangatahanao: 75Mo ho an ny $data manankery 1 andro. Tsindrio ny *999*$code# ahafantaranao ny ambina Kilooctet sy Megaoctet azo ampiasaina.")
MESSAGES['kozy'] = "Kozy Kozy: Manana 900 sec, 45 SMS sy 50 Mo ianao,manankery hatr@ 11:59 ora alina. Misaotra tompoko."
MESSAGES['regional'] = "Tontosa ny fangatahanao hampiasa ny tolotra Internet Mlay, manakery hatramin ny 11:59 alina. Misaotra tompoko"


MESSAGES['balance'] = Template('Ils vous reste $data qui expirera le $expiry.')
MESSAGES['no_balance'] = "vous n'avez pas une forfait en cours"

MESSAGES['ack'] = 'Request received, Check the confirmation messages and then restart the device before you start browsing'
MESSAGES['error'] = '''Tsy tontosa ny fangatahanao. Avereno afaka fotoana fohy azafady. Misaotra tompoko'''

MESSAGES['conflicting_bundle'] = 'Dear customer you are currently subscribed to another bundle. To purchase this bundle please exhaust your current bundle. Dial *544# to check your current bundle balance. Airtel.'

MESSAGES['subscriber'] = {}
MESSAGES['subscriber']['success'] = Template("Felicitations. Vous venez d'offrir avec succes $data valide pour $days jours au $b_msisdn.Naviguez vite et moins cher.Cliquez ici www.opera.com")

#MESSAGES['insufficient_funds'] = 'Dear customer you do not have sufficient funds to purchase this bundle. Please reload and try again. Airtel.'
MESSAGES['insufficient_funds'] = "Vous n'avez pas assez de credit pour vous abonner. Merci de recharger votre compte"
#MESSAGES['insufficient_funds'] = "Desole! Vpus n'avez pas de credit pour souscrire a ce forfait. Veuillez recharger plus reessayer SVP!"
MESSAGES['recipient'] = {}
MESSAGES['recipient']['success'] = Template("Felicitations.le $benefactor vient de vous offrir $data valable jusqu'au $expiry.Naviquez vite et moins cher.Cliquez ici www.opera.com")
MESSAGES['is_barred'] = 'Tsy tontosa ny fangatahanao. Avereno afaka fotoana fohy azafady. Misaotra tompoko'
MESSAGES['renewal_removed'] = 'Votre renouvellement a ete desactive avec succes'
MESSAGES['no_renew'] = "Desole  vous n'avez pas de renouvellement active"
MESSAGES['tip'] = 'Press *131# to check your current balance before your start browsing. If balance still same, revise the process. Airtel'

MESSAGES['unlimited_succ'] = {}
MESSAGES['unlimited_succ']['txt-1']  = "Your subscription to the Unlimited Internet Offer was performed with success. Thank you"
MESSAGES['unlimited_succ']['txt-3'] = "Votre souscription a I offer Internet illimite a ete effectuee avec succes. Merci"
MESSAGES['unlimited_succ']['txt-2'] = "Tontosa ny fangatahanao hampiasa ny tolotra internet illimite. Misaotra tompoko"

MESSAGES['unlimited_unsucc'] = {}
MESSAGES['unlimited_unsucc']['txt-1'] = "Your subscription to the Unlimited Internet offer was rejected. Please refill your account and try later. Thank you"
MESSAGES['unlimited_unsucc']['txt-3'] = "Votre souscription a I offer internet Illimite a ete rejetee. Veuillez rajouter du credit a votre compte et reessayer plus tard. Merci"
MESSAGES['unlimited_unsucc']['txt-2'] = "Votre souscription a I offer internet Illimite a ete rejetee. Veuillez rajouter du credit a votre compte et reessayer plus tard. Merci"
#MESSAGES['unlimited_unsucc']['txt-3'] = "Votre souscription a I offer internet Illimite a ete rejetee. Veuillez rajouter du credit a votre compte et reessayer plus tard. Merci"

MESSAGES['success_mymeg_10'] = "Tafiditra ny MyMeg10: 10Mo ampiasaina internet hatramin ny 12 ora. Tsindrion ny *999*114# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."
MESSAGES['success_mymeg_10_morn'] = "Tafiditra ny MyMeg10 ahazoanao 10Mo ampiasaina internet hatr@ 12 ora. Tsindrio ny *999*114# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."
MESSAGES['success_mymeg_10_afte'] = "Tafiditra ny MyMeg10 ahazoanao 10Mo ampiasaina internet hatr@ 5 ora. Tsindrion ny *999*114# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."

MESSAGES['success_fb_weekly'] = "Tafiditra ny tolotra Facebook manankery 7 andro. Tsindrion ny *999*44# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."
MESSAGES['success_tw_weekly'] = "Tafiditra ny tolotra Twitter manankery 7 andro. Tsindrion ny *999*45# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."
MESSAGES['success_wa_weekly'] = "Tafiditra ny Tolotra Whatsapp manankery 7 andro. Tsindrion ny *999*46# ahafantaranao ny Kiloctet sy Megaoctet sisa azo ampiasaina."

BUNDLES = {}
BUNDLES["4"] = "4"
BUNDLES["0"] = "0"
BUNDLES["6"] = "6"
BUNDLES["8"] = "8"
BUNDLES["9"] = "9"
BUNDLES["11"] = "11"
BUNDLES["12"] = "12"
BUNDLES["14"] = "14"
BUNDLES["15"] = "15"
BUNDLES["16"] = "16"
BUNDLES["32"] = "32"
BUNDLES["33"] = "33"
BUNDLES["35"] = "35"
BUNDLES["36"] = "19"
BUNDLES["37"] = "20"
BUNDLES["38"] = "21"
BUNDLES["40"] = "1"
BUNDLES["20"] = "58"
BUNDLES["41"] = "179"  #MyMeg10 Activation
BUNDLES["44"] = "180"  #Facebook Weekly Activation
BUNDLES["45"] = "181"  #Twitter Weekly Activation
BUNDLES["46"] = "182"  #Whatsapp Weekly Activation

#bonus bundles
BUNDLES["131"] = "131"
BUNDLES["132"] = "132"
BUNDLES["133"] = "133"

'''
BUNDLES["10"] = "17"
BUNDLES["11"] = "18"
BUNDLES["12"] = "19"
BUNDLES["13"] = "20"
BUNDLES["14"] = "21"
'''

B_BUNDLES = {}
B_BUNDLES["4"] = "22"
B_BUNDLES["0"] = "0"
B_BUNDLES["6"] = "23"
B_BUNDLES["8"] = "24"
B_BUNDLES["9"] = "25"
B_BUNDLES["11"] = "26"
B_BUNDLES["12"] = "27"
B_BUNDLES["14"] = "28"
B_BUNDLES["15"] = "29"
B_BUNDLES["16"] = "30"
B_BUNDLES["17"] = "36"
B_BUNDLES["20"] = "58"   #Data Unlimited GIFT Activation
B_BUNDLES["36"] = "19"   #Facebook GIFT Activation
B_BUNDLES["37"] = "20"   #Twitter GIFT Activation
B_BUNDLES["38"] = "21"   #Whatsapp GIFT Activation
B_BUNDLES["40"] = "1"    #MyMeg15 GIFT Activation
B_BUNDLES["41"] = "179"  #MyMeg10 GIFT Activation
B_BUNDLES["44"] = "180"  #Facebook Weekly GIFT Activation
B_BUNDLES["45"] = "181"  #Twitter Weekly GIFT Activation
B_BUNDLES["46"] = "182"  #Whatsapp Weekly GIFT Activation


VALIDITY = {}
VALIDITY["4"] = "1"
VALIDITY["6"] = "3"
VALIDITY["8"] = "7"
VALIDITY["9"] = "7"
VALIDITY["11"] = "30"
VALIDITY["12"] = "30"
VALIDITY["14"] = "30"
VALIDITY["15"] = "30"
VALIDITY["16"] = "30"
VALIDITY["17"] = "1"
VALIDITY["19"] = "1"
VALIDITY["20"] = "1"
VALIDITY["21"] = "1"
VALIDITY["22"] = "1"
VALIDITY["23"] = "3"
VALIDITY["24"] = "7"
VALIDITY["25"] = "7"
VALIDITY["26"] = "30"
VALIDITY["27"] = "30"
VALIDITY["28"] = "30"
VALIDITY["29"] = "30"
VALIDITY["30"] = "30"
VALIDITY["31"] = "2"
VALIDITY["32"] = "2"
VALIDITY["33"] = "5"
VALIDITY["34"] = "7"
VALIDITY["35"] = "7"
VALIDITY["36"] = "1"
VALIDITY["1"] = "1"
VALIDITY["58"] = "30"
VALIDITY["119"] = "30"
VALIDITY["179"] = "1"  #MyMeg10
VALIDITY["180"] = "7"  #Facebook Weekly
VALIDITY["181"] = "7"  #Twitter Weekly
VALIDITY["182"] = "7"  #Whatsapp Weekly

#bonus bundles
VALIDITY["131"] = "7"
VALIDITY["132"] = "7"
VALIDITY["133"] = "30"


KOZY_PACKAGE_ID = "17"
UNLIMITED_ID = "58"
REGIONAL_ID = "119"

#bonus bundles
BONUSMEG250 = "131"
BONUSMEG500 = "132"
BONUSGIG1 = "133"

BONUSBUNDLES = ['131','132','133']
NEWMSGBUNDLES = ['4','6','8','9','11','12','14','15','16','19','20','21','32','33','35','119']

DATA_USAGE = ['4', '6', '8', '9']

NIGHT_BUNDLES = ['31','32','33','34','35']
SOCIAL = ['19','20','21']

SOCIAL_PKGS = {}
SOCIAL_PKGS['19'] = '36'
SOCIAL_PKGS['20'] = '37'
SOCIAL_PKGS['21'] = '38'

MY_MEG_10 = '179'
SOCIAL_FB_WEEKLY = '180'
SOCIAL_TW_WEEKLY = '181'
SOCIAL_WA_WEEKLY = '182'

BILL_PLAN = {}
BILL_PLAN[8]  = {'bonus_offer_id': 1249, 'cost': 6000, 'refill_id': 'DP00', 'offer_id': 1018}  # MyMeg 250
BILL_PLAN[9]  = {'bonus_offer_id': 1248, 'cost': 10000, 'refill_id': 'DP01', 'offer_id': 1019} # MyMeg 500
BILL_PLAN[11] = {'bonus_offer_id': 1250, 'cost': 30000, 'refill_id': 'DP02', 'offer_id': 1021} # MyGig 1
