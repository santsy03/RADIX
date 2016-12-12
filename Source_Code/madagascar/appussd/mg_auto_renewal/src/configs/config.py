'''
config for the bf auto renewal app app

'''

from string import Template

HOST_NAME = __import__('socket').gethostname()

RENW_CWD = "/appussd/mg_auto_renewal/src/renewals_consumer"
CWD = "/appussd/mg_auto_renewal/src/consumer"

LOG_NAME = "dprenewalcall-{}".format(HOST_NAME)
PID_FILE = '{}/dp_provdaemon-{}.pid'.format(CWD, HOST_NAME)
LOG_FOLDER = 'logs'

RENEWAL_LOG_NAME = "data_renewal_log-{}".format(HOST_NAME)
RENEWAL_PID_FILE = '{}/renw_prov_daemon-{}.pid'.format(RENW_CWD, HOST_NAME)
RENEWAL_LOG_FOLDER = 'renw_logs'



NOW_SMS_EVENT_ID = 1
POSTPONED_SMS_EVENT_ID = 3
THIRD_DAY_SMS_EVENT_ID = 4
DAY_OF_RENEWAL_EVENT_ID = 5

RENEW_EVENT_ID = 2


RENEWAL_SPACING = 3
RENEWAL_TRIES = 3
FREQUENCY_TRIES = 3
RENEWAL_DAYS = 3

DEBUG = False
MIN_AMOUNT = 5
DA_FACTOR = 100
DA_ACTION = 'dedicatedAccountValueNew'
DA_ID = 8
WORKERS = 20
DEBUG = True

MSISDN_LENGTH = 8

ALLOWED_PREFIXES = ['76','77','66','74','75','65','64']

PROVISION_URL =  "http://127.0.0.1:9002/submitProvision?"
BALANCE_URL =  "http://127.0.0.1:9002/submitBalance"


ACK = {}
ACK['txt-1'] = "chere client nous avons recu votre demande. Sil vous plait attendez que nous traitons"
ACK['txt-2'] = "We have recieved your request, please wait as we process it"
ACK['postpaid'] = "Cher client vous n'etes pas autorise a acceder a ce service"
ACK['wrong_rec'] = "Le nombre que vous avez envoyez n'est pas valide"
ACK['wrong'] = "demande meconnu"

SPECIAL_NUMBERS = []

MESSAGES = {}
MESSAGES['subscriber'] ={}
MESSAGES['subscriber']['same'] = "cher client vous ne pouvez pas ajoutez votre numero comme numero magique"
MESSAGES['subscriber']['is_barred'] = "Desole vous ne pouvez pas souscrire ce numero a numero magique"

#metrics

SUCCESS_HIT = "application.renewal.success.%s"
FAIL_HIT = "application.renewal.fail.%s"

AUTH_KEY = 'modularP4ss'
ACCOUNT_ID = 'modular'
ROUTING_KEY = 'mg_data_renewal'

QUEUES = {}
QUEUES['internal'] = {}
QUEUES['internal']['test'] = 'test_make_dpcall_queue'
QUEUES['internal']['prod'] = 'make_dpcall_queue'


QUEUES['renewal'] = {}
QUEUES['renewal']['test'] = 'test_renewal_mg_data_interface'
QUEUES['renewal']['prod'] = 'renewal_mg_data_interface'



#MESSAGES['success'] = Template('Dear customer you have successfully subscribed to the $data plan expiring on $expiry.')
MESSAGES['renewal_success'] = Template("Chere client, votre forfait Internet de $data a ete renouvele avec succes pour $days. Pour arreter le renouvellemnt automatique tapez *114*0*2#")
MESSAGES['is_barred'] = 'Dear customer you are not allowed to purchase this product. Airtel.'
MESSAGES['will_renew_today'] = Template("Cher client, votre forfait Internet de $package sera automatiquement renouvele aujourdhui. Pour arreter le renouvellement automatique, repondez avec *114*0*2#")
MESSAGES['will_renew'] = Template("Cher client, votre forfait Internet de $package sera automatiquement renouvele le $expiry. Pour arreter le renouvellement automatique, Tapez *114*0*2#")

MESSAGES['no_renew_funds'] = 'Le renouvellement automatique de votre forfait n a pas ete effectue. Veuillez recharger puis souscrire a nouveau a un forfait Internet'

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
VALIDITY["1"] = "1"
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



KOZY_PACKAGE_ID = "17"

NIGHT_BUNDLES = ['31','32','33','34','35']
SOCIAL = ['19','20','21']

SOCIAL_PKGS = {}
SOCIAL_PKGS['19'] = '36'
SOCIAL_PKGS['20'] = '37'
SOCIAL_PKGS['21'] = '38'

PACKAGES = {}
PACKAGES["4"] = "My Meg 50"
PACKAGES["6"] = "My Meg 100"
PACKAGES["8"] = "My Meg 250"
PACKAGES["9"] = "My Meg 500"
PACKAGES["11"] = "My Gig 1"
PACKAGES["12"] = "My Gig 2"
PACKAGES["14"] = "My Gig 5"
PACKAGES["15"] = "My Gig 10"
PACKAGES["16"] = "My Gig 30"


