'''
config for the madagascar data interface

'''

from string import Template

CWD = "/appussd/mg_data_interface/src/consumer"
LOG_NAME = "data_responselog"
PID_FILE = '/appussd/mg_data_interface/src/consumer/data_prov_daemon.pid'

MEG_CWD = "/appussd/mg_data_interface/src/megfiftn_consumer"
MEG_LOG_NAME = "meg_responselog"
MEG_PID_FILE = '/appussd/mg_data_interface/src/megfiftn_consumer/meg15_daemon.pid'


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


#=====New message notifications====================================

tempMsgs = {}
tempMsgs[4] = "Tafiditra ny MyMeg50: 50Mo ampiasaina internet manankery 1andro. Miampy 15 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa azonao."
tempMsgs[6] = "Tafiditra ny MyMeg100: 100Mo ampiasaina internet manankery 3andro. Miampy 25 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa azonao."
tempMsgs[8] = "Tafiditra ny MyMeg250:250Mo ampiasaina internet manankery 7andro. Miampy 25 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa azonao."
tempMsgs[9] = "Tafiditra ny MyMeg500: 500Mo ampiasaina internet manankery 7andro. Miampy 30 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa azonao."
tempMsgs[11] = "Tafiditra ny MyGig1: 1Go ampiasaina internet manankery 30 andro. Miampy 40 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa azonao."
tempMsgs[12] = "Tafiditra ny MyGig2: 2Go ampiasaina internet manankery 30andro. Miampy 50 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa azonao."
tempMsgs[14] = "Tafiditra ny MyGig5: 5Go ampiasaina internet manankery 30andro. Miampy 50 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa azonao."
tempMsgs[15] = "Tafiditra ny MyGig10: 10Go ampiasaina internet manankery 30andro. Miampy 60 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa azonao"
tempMsgs[16] = "Tafiditra ny MyGig30: 30Go ampiasaina internet manankery 30andro. Miampy 60 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa azonao."
tempMsgs[19] = "Tontosa ny fangatahanao: 75Mo ho an ny Facebook manankery 1andro. Miampy 10 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa azonao."
tempMsgs[20] = "Tontosa ny fangatahanao: 75Mo ho an ny Twitter manankery 1andro. Miampy 10 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa azonao."
tempMsgs[21] = "Tontosa ny fangatahanao: 75Mo ho an ny Whatsapp manankery 1andro.Miampy 10 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa azonao."
#tempMsgs[22] = Template("Tontosa ny fandefasanao MyMeg50 Kado any @ $b_msisdn. Miampy 15 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
#tempMsgs[23] = Template("Tontosa ny fandefasanao MyMeg100 Kado any @ $b_msisdn. Miampy 25 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
#tempMsgs[24] = Template("Tontosa ny fandefasanao MyMeg250 Kado any @ $b_msisdn. Miampy 25 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
#tempMsgs[25] = Template("Tontosa ny fandefasanao MyMeg500 Kado any @ $b_msisdn. Miampy 30 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
#tempMsgs[26] = Template("Tontosa ny fandefasanao MyGig1 Kado any @ $b_msisdn. Miampy 40 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
#tempMsgs[27] = Template("Tontosa ny fandefasanao MyGig2 Kado any @ $b_msisdn. Miampy 50 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
#tempMsgs[28] = Template("Tontosa ny fandefasanao MyGig5 Kado any @ $b_msisdn. Miampy 50 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa efa azonao. ")
#tempMsgs[29] = Template("Tontosa ny fandefasanao MyGig10 Kado any @ $b_msisdn. Miampy 60 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
#tempMsgs[30] = Template("Tontosa ny fandefasanao MyGig30 Kado any @ $b_msisdn. Miampy 60 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
#tempMsgs[121] = Template("Tontosa ny fandefasanao MyMeg15 Kado any @ $b_msisdn. Miampy 10 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
#tempMsgs[122] = Template("Tontosa ny fandefasanao Facebook Kado any @ $b_msisdn. Miampy 10 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
#tempMsgs[123] = Template("Tontosa ny fandefasanao Twitter Kado any @ $b_msisdn. Miampy 10 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
#tempMsgs[124] = Template("Tontosa ny fandefasanao Whatsapp Kado any @ $b_msisdn. Miampy 10 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
tempMsgs[32] = "Tafiditra ny MyMeg20Night: 20Mo ampiasaina internet manankery 2alina. Miampy 10 ny isanao @ promo fahaleovantena. Tsindrio *999*55# raha hijery ireo isa azonao."
tempMsgs[33] = "Tafiditra ny MyMeg50Night: 50Mo ampiasaina internet manankery 1alina. Miampy 15 ny isanao @ promo fahaleovantena. Tsindrio *999*55# raha hijery ireo isa azonao."
tempMsgs[35] = "Tafiditra ny MyMeg100Night:100Mo ampisaina internet manankery 3 alina. Miampy 20 ny isanao @ promo fahaleovantena. Tsindrio *999*55# raha hijery ireo isa azonao."
tempMsgs[119] = "Tafiditra ny Internet M'Lay manankery hatr@ 12 ora alina. Miampy 10 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."


#======End of new message notification=======================================================
#====Names of above package ids==============
'''
tempMsgs = {}
tempMsgs[MyMeg 15][1]
tempMsgs[MyMeg 50][4] = "Tafiditra ny MyMeg50: 50Mo ampiasaina internet manankery 1 andro. Miampy 15 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."
tempMsgs[MyMeg 100][6] = "Tafiditra ny MyMeg100: 100Mo ampiasaina internet manankery 3 andro. Miampy 25 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."
tempMsgs[MyMeg 250][8] = "Tafiditra ny MyMeg250: 250Mo ampiasaina internet manankery 7 andro. Miampy 25 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."
tempMsgs[MyMeg 500][9] = "Tafiditra ny MyMeg500: 500Mo ampiasaina internet manankery 7 andro. Miampy 30 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."
tempMsgs[MyGig 1][11] = "Tafiditra ny MyGig1: 1Go ampiasaina internet manankery 30andro. Miampy 40 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."
tempMsgs[MyGig 2][12] = "Tafiditra ny MyGig2: 2Go ampiasaina internet manankery 30andro. Miampy 50 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."
tempMsgs[MyGig 5][14] = "Tafiditra ny MyGig5: 5Go ampiasaina internet manankery 30andro. Miampy 50 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."
tempMsgs[MyGig 10][15] = "Tafiditra ny MyGig10: 10Go ampiasaina internet manankery 30andro. Miampy 60 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."
tempMsgs[MyGig 30][16] = "Tafiditra ny MyGig30: 30Go ampiasaina internet manankery 30andro. Miampy 60 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."
tempMsgs[Facebook][19] = "Tontosa ny fangatahanao: 75Mo ho an ny Facebook manankery 1andro. Miampy 10 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."
tempMsgs[Twitter][20] = "Tontosa ny fangatahanao: 75Mo ho an ny Twitter manankery 1andro. Miampy 10 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."
tempMsgs[Whatsapp][21] = "Tontosa ny fangatahanao: 75Mo ho an ny Whatsapp manankery 1andro.Miampy 10 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao"
tempMsgs[MyMeg 50(GIFT)][22] = Template("Tontosa ny fandefasanao MyMeg50 Kado any @ $b_msisdn. Miampy 15 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
tempMsgs[MyMeg 100(GIFT)][23] = Template("Tontosa ny fandefasanao MyMeg100 Kado any @ $b_msisdn. Miampy 25 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
tempMsgs[MyMeg 250(GIFT)][24] = Template("Tontosa ny fandefasanao MyMeg250 Kado any @ $b_msisdn. Miampy 25 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
tempMsgs[MyMeg 500(GIFT)][25] = Template("Tontosa ny fandefasanao MyMeg500 Kado any @ $b_msisdn. Miampy 30 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
tempMsgs[MyGig 1(GIFT)][26] = Template("Tontosa ny fandefasanao MyGig1 Kado any @ $b_msisdn. Miampy 40 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
tempMsgs[MyGig 2GIFT)][27] = Template("Tontosa ny fandefasanao MyGig2 Kado any @ $b_msisdn. Miampy 50 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
tempMsgs[MyGig 5(GIFT)][28] = Template("Tontosa ny fandefasanao MyGig5 Kado any @ $b_msisdn. Miampy 50 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
tempMsgs[MyGig 10(GIFT)][30] = Template("Tontosa ny fandefasanao MyGig10 Kado any @ $b_msisdn. Miampy 60 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
tempMsgs[MyGig 30(GIFT)][30] = Template("Tontosa ny fandefasanao MyGig30 Kado any @ $b_msisdn. Miampy 60 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
tempMsgs[MyMeg 15 (GIFT)][121] = Template("")
tempMsgs[Facebook (GIFT)][122] = Template("Tontosa ny fandefasanao Facebook Kado any @ $b_msisdn. Miampy 10 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
tempMsgs[Twitter (GIFT)][123] = Template("Tontosa ny fandefasanao Twitter Kado any @ $b_msisdn. Miampy 10 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
tempMsgs[Whatsapp (GIFT)][124] = Template("Tontosa ny fandefasanao Whatsapp Kado any @ $b_msisdn. Miampy 10 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
tempMsgs[MyMeg 50(NIGHT)][33] = Template("Tafiditra ny MyMeg50Night: 50Mo ampiasaina internet manankery 1alina. Miampy 15 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
tempMsgs[MyMeg 100(NIGHT)][35] = Template("Tafiditra ny MyMeg100Night: 100Mo internet manankery 3 alina. Miampy 20 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
tempMsgs[Regional][119] = "Tafiditra ny Internet M'Lay manankery hatr@ 12 ora alina. Miampy 10 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."

'''

#====End of Names================================================================

#MESSAGES['success'] = Template("Tontosa ny fangatahanao. Tsindrio ny *999*114# ahafataranao ny Kilooctet sy Megaoctet sisa azo ampiasaina. Misaotra Tompoko")
MESSAGES['success'] = Template("Tontosa ny fangatahanao. Tsindrio ny *999*55# raha hijery ireo isa efa azonao @ Promo Mifety 55. Misaotra tompoko")

MESSAGES['success_15'] = "Tafiditra ny MyMeg15 ahazoanao 15Mo ampiasaina internet. Fijerena Mo tavela: tsindrio ny *999*114#. Misaotra tompoko"

#MESSAGES['success_15_morn'] = "Tafiditra ny MyMeg15 ahazoanao 15Mo ampiasaina internet hatramin ny 12 ora atoandro. Fijerena Mo tavela: tsindrio ny *999*114#. Misaotra tompoko"
MESSAGES['success_15_morn'] = "Tafiditra ny MyMeg15: 15Mo ampiasaina internet hatr@ 12 ora. Miampy 10 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."

#MESSAGES['success_15_afte'] = "Tafiditra ny MyMeg15 ahazoanao 15Mo ampiasaina internet hatramin ny 5 ora hariva. Fijerena Mo tavela: tsindrio ny *999*114#. Misaotra tompoko"
MESSAGES['success_15_afte'] = "Tafiditra ny MyMeg15: 15Mo ampiasaina internet hatr@ 5 ora. Miampy 10 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."


MESSAGES['success_15_french'] = "Votre demande a ete executee. Vous avez 15Mo d'internet. Tapez *999*114# pour connaitre les Mo restants.Merci"

MESSAGES['time_barred'] = "Ny fidirana amin io tolotra io dia misokatra hatramin ny 5 ora hariva ihany. Manasa anao hampiasa Mymeg 50 *114*4#. Misaotra tompoko."

MESSAGES['time_barred_french'] = "Cher client,votre demande n a pas ete executee. Vous pouvez souscrire a MyMeg15 de 8h-12h et de 13h-17h. Merci"

MESSAGES["time_barred_bparty"] = "Chere client, on ne peut pas pourchaser MyMeg15 pour votre ami parceque il est disponible seulement de 8h-12h et de 13h-17h Merci"

MESSAGES["morning_barred"] = "Tompoko, tsy tontosa ny fangatahanao. Manomboka amin ny 1ora-5ora no hahafahanao miditra indray amin ny MyMeg15 . Misaotra tompoko"
MESSAGES["morning_barred_french"] = "Cher client,v otre demande n a pas ete executee. Vous pouvez souscrire a nouveau de 13h jusqu a 17h. Merci"

MESSAGES["afternoon_barred"] = "Tompoko, tsy tontosa ny fangatahanao. Efa feno ny hahafahanao mampiasa io tolotra io androany. Misaotra tompoko "
MESSAGES["afternoon_barred_french"] = "Cher client,votre demande n a pas ete executee. Vous avez atteint le nombre de souscription autorise pour ce jour. Merci"


MESSAGES['success_night'] = Template("Tontosa ny fangatahanao. Ianao dia manana $data hanaovana internet. Tsindrio ny *999*103# ahafantaranao ny ambiny afaka ampiasainao. Misaotra tompoko")

#MESSAGES['social'] = Template("Tontosa ny fangatahanao: 75Mo ho an ny $data manankery 1 andro. Tsindrio ny *999*$code# ahafantaranao ny ambina Kilooctet sy Megaoctet azo ampiasaina.")
MESSAGES['social'] = Template("Tontosa ny fangatahanao: 75Mo ho an ny $data manankery 1andro. Miampy 10 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao.")
MESSAGES['kozy'] = "Kozy Kozy: Manana 900 sec, 45 SMS sy 50 Mo ianao,manankery hatr@ 11:59 ora alina. Misaotra tompoko."
#MESSAGES['regional'] = "Tontosa ny fangatahanao hampiasa ny tolotra Internet Mlay, manakery hatramin ny 11:59 alina. Misaotra tompoko"
MESSAGES['regional'] = "Tafiditra ny Internet M'Lay manankery hatr@ 12 ora alina. Miampy 20 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."


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
#MESSAGES['unlimited_succ']['txt-2'] = "Tontosa ny fangatahanao hampiasa ny tolotra internet illimite. Misaotra tompoko"
MESSAGES['unlimited_succ']['txt-2'] = "Tafiditra ny tolotra Internet Illimite manankery 30andro. Miampy 60 ny isanao @ promo mifety55. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."

MESSAGES['unlimited_unsucc'] = {}
MESSAGES['unlimited_unsucc']['txt-1'] = "Your subscription to the Unlimited Internet offer was rejected. Please refill your account and try later. Thank you"
MESSAGES['unlimited_unsucc']['txt-3'] = "Votre souscription a I offer internet Illimite a ete rejetee. Veuillez rajouter du credit a votre compte et reessayer plus tard. Merci"
MESSAGES['unlimited_unsucc']['txt-2'] = "Tafiditra ny tolotra Internet Illimite manankery 30andro. Miampy 60 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa azonao."

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


KOZY_PACKAGE_ID = "17"
UNLIMITED_ID = "58"
REGIONAL_ID = "119"

DATA_USAGE = ['4', '6', '8', '9']

NIGHT_BUNDLES = ['31','32','33','34','35']
SOCIAL = ['19','20','21']

SOCIAL_PKGS = {}
SOCIAL_PKGS['19'] = '36'
SOCIAL_PKGS['20'] = '37'
SOCIAL_PKGS['21'] = '38'
