from string import Template
URL = "http://127.0.0.1:8005/"
C_CODE = '261'

HOST_NAME = __import__('socket').gethostname()

CWD = "/appussd/mg_aapcn_me2u/src/consumer"
LOG_NAME = "internet-me2u-{}".format(HOST_NAME)
PID_FILE = '/appussd/mg_aapcn_me2u/src/consumer/prov_daemon-{}.pid'.format(HOST_NAME)
DEBUG = False
WORKERS = 50

#metrics
QUEUES = {}
QUEUES['test'] = 'test_internetme2u_queue'
QUEUES['prod'] = 'internetme2u_queue'

STATUS = {}
# Status code : definition mapping
STATUS['no_user'] = '1'
STATUS['auth_success'] = '0'
STATUS['auth_fail'] = '2'
STATUS['error'] = '3'
STATUS['user_created'] = '4'
STATUS['user_create_fail'] = '6'
STATUS['password_change_success'] = '7'
STATUS['password_change_fail'] = {}
STATUS['password_change_fail']['auth_fail'] = '8'
STATUS['password_change_fail']['create_user_fail'] = '9'
STATUS['account_locked'] = '10'
STATUS['password_reset_success'] = '11'
STATUS['password_reset_fail'] = '12'
STATUS['unlock_success'] = '13'
STATUS['unlock_fail'] = '14'
STATUS[''] = ''


UPDATE_CDR_METRIC = "application.me2u.db.cdrupdate"
UPDATE_CDR_TRACKER_METRIC = "application.me2u.db.trackerupdate"

MAX_TRANSACTIONS = "application.me2u.db.trackerupdate"
PRICE = 0
BILLABLE = False


MIN_AMOUNT = 50
PARABOLE_AMOUNT = 6144
DEFAULT_OFFER = 1011


ALLOWED_BUNDLES = [1021,1022,1024,1025,1026,1358,1359,1023,1171]
VOLUME_DA = 1011
VOLUME_UC_ID = 1011

PARABOLE_DA = 1071
PARABOLE_UC_ID = 1071
PARABOLE_OFFER = 1171



REQUEST_VALIDATE_FAIL = 1
SENDER_VALIDATE_FAIL = 2
SENDER_PROV_FAIL = 3
RECIPIENT_PROV_FAIL = 4
SUCCESS = 5

UNDEFINED = 0


STATUS_CODES = {}
STATUS_CODES = {}

MESSAGES = {}

MESSAGES['txt-1'] = {}
MESSAGES['txt-2'] = {}
MESSAGES['txt-3'] = {}


ACK = {}

'''
txt-1 english
txt-2 malagasy
txt-3 french
'''
ACK = {}
ACK['txt-1'] = "We have recieved your request, please wait as we process it"
ACK['txt-2'] = "Voaray ny fangatahanao. Miandrasa kely azafady. Misaotra tompoko"
ACK['txt-3'] = "Votre demande et en cours de traitement. Veuillez patienter SVP"


MESSAGES['txt-1']['error'] = "There was an error procesing your request. Please contact customer care for more details"
MESSAGES['txt-1']['success_sender'] = Template("The $amount MB offered to $recipient is done successfully. Thank you for sharing")
MESSAGES['txt-1']['success_sender_parabole'] = Template("The sending of 6Gb to $recipient has been performed with success. Thank you")
MESSAGES['txt-1']['success_recipient'] = Template("You have received $amount MB from $sender.Offer valid until $expiry. Enjoy it")
MESSAGES['txt-1']['success_recipient_parabole'] = Template("You have received 6GB from $sender.Offer valid until $expiry. Enjoy it")
MESSAGES['txt-1']['no_balance'] = "Your bundle is insufficient. Please subscribe to an internet offer"
MESSAGES['txt-1']['inadequate_validity'] = "Your bundle will be expired in few times. Please subscribe to a new internet offer. Thank you"
MESSAGES['txt-1']['not_whitelisted'] = "You are not allowed to access the service. Thank you" 
MESSAGES['txt-1']['invalid_bnumber'] = "The Airtel number of your correspondant is not valid. Please verify and try later"
MESSAGES['txt-1']['has_exceeded'] = "You have exceeded the maximum number of transactions per day. Try again tommorow"
MESSAGES['txt-1']['pin_invalid'] = "The pin you have entered is invalid. The pin must be 4 digits long"
MESSAGES['txt-1']['auth_fail'] = "The password is not valid. Please try again"
MESSAGES['txt-1']['no_funds'] = "You have insufficient funds and thus cannot do a me2u request"
MESSAGES['txt-1']['password_format_failed'] = "Your new password should contain 4 digits or alphanumeric"
MESSAGES['txt-1']['new_passwords_no_match'] = "Your new passwords do not match. Please verify and try later"
MESSAGES['txt-1']['successful_password_change'] = "Your password is changed successfully. Thank you"
MESSAGES['txt-1']['wrong_pin_password_change'] = "The password is not valid. Please verify and try later"
MESSAGES['txt-1']['below_min'] = "Dear customer, the minimum transfer authorized is %sMB. Thank you" % (str(MIN_AMOUNT))
MESSAGES['txt-1']['request_not_allowed'] = "Your request is not executed, please retry by sending 6Gb of internet. Thank you"

MESSAGES['txt-2']['error'] = "Erreur"
MESSAGES['txt-2']['success_sender'] = Template("Ny $amount Mo nalefanao dia voarain ny $recipient Misaotra tompoko")
MESSAGES['txt-2']['success_sender_parabole'] = Template("Tontosa ny fandefasanao 6Go any @ $recipient. Misaotra tompoko")
MESSAGES['txt-2']['success_recipient'] = Template("Naharay $amount Mo avy $sender ianao. Tolotra manankery $expiry Ankafizo ary.")
MESSAGES['txt-2']['success_recipient_parabole'] = Template("Naharay 6Go avy $sender ianao. Tolotra manankery $expiry Ankafizo ary.")
MESSAGES['txt-2']['no_balance'] = "Tsy ampyyyy ny Mo tokony ampiasainao. Azafady, misafidiana Tolotra internet vaovao"
MESSAGES['txt-2']['inadequate_validity'] = "Efa ho lany andro ny Mo anananao. Azafady, misafidiana Tolotra internet vaovao. Misaotra tompoko"
MESSAGES['txt-2']['not_whitelisted'] = "Miala tsiny, tsy afaka mampiasa an io tolotra ianao. Misaotra tompoko"
MESSAGES['txt-2']['invalid_bnumber'] = "Diso ny nomerao Airtel nosafidianao. Azafady, hamarino ary avereno ny fangatahanao."
MESSAGES['txt-2']['has_exceeded'] = "You have exceeded the maximum number of transactions per day. Try again tommorow"
MESSAGES['txt-2']['pin_invalid'] = "The pin you have entered is invalid. The pin must be 4 digits long"
MESSAGES['txt-2']['auth_fail'] = "Diso ny teny miafina nampidirinao. Azafady hamarino ary avereno ny fangatahanao"
MESSAGES['txt-2']['no_funds'] = "Votre credit est insuffisant pour cette operation"
MESSAGES['txt-2']['password_format_failed'] = "Ny teny miafina vaovao dia tokony ahitana tarehimarika 4 na tarehimarika sy litera 4 miaraka."
MESSAGES['txt-2']['new_passwords_no_match'] = "Misy diso ny teny miafina nampidirinao. Hamarino azafady ary avereno ny fangatahanao"
MESSAGES['txt-2']['successful_password_change'] = "Tontosa ny fanovanao ny teny miafina. Misaotra tompoko"
MESSAGES['txt-2']['wrong_pin_password_change'] = "Diso ny teny miafina nampidirinao. Azafady hamarino ary avereno ny fangatahanao"
MESSAGES['txt-2']['below_min'] = "Ry Mpanjifa hajaina, %sMO ny fetra farany ambany afaka zaraina. Misaotra tompoko" % (str(MIN_AMOUNT))
MESSAGES['txt-2']['request_not_allowed'] = "Tsy tontosa ny fangatahanao, 6Go ny internet azonao zaraina @ tolotra izay ampiasainao. Misaotra tompoko"

MESSAGES['txt-3']['error'] = "Desole. Votre demande n'etais pas executee"
MESSAGES['txt-3']['success_sender'] = Template("Les $amount Mo sont recus par $recipient. Merci d avoir partage")
MESSAGES['txt-3']['success_sender_parabole'] = Template("L'envoi de 6Go au $recipient a ete effectue avec succes. Merci")
MESSAGES['txt-3']['success_recipient'] = Template("Vous avez recu $amount Mo de $sender. Offre valide $expiry.")
MESSAGES['txt-3']['success_recipient_parabole'] = Template("Vous avez recu 6Go Mo de $sender. Offre valide $expiry.")
MESSAGES['txt-3']['no_balance'] = "Votre forfait est insuffisant, veuillez souscrire a un forfait internet"
MESSAGES['txt-3']['inadequate_validity'] = "Votre forfait va expirer bientot. Veuillez souscrire a un nouveau forfait. Merci"
MESSAGES['txt-3']['not_whitelisted'] = "Desole, vous ne pouvez pas utiliser ce service. Merci"
MESSAGES['txt-3']['invalid_bnumber'] = "Le numero de votre correspondant est incorrect. Veuillez verifier et recommencer"
MESSAGES['txt-3']['has_exceeded'] = "You have exceeded the maximum number of transactions per day. Try again tommorow"
MESSAGES['txt-3']['pin_invalid'] = "The pin you have entered is invalid. The pin must be 4 digits long"
MESSAGES['txt-3']['auth_fail'] = "Votre mot de passe est incorrect. Veuillez reessayer s il vous plait"
MESSAGES['txt-3']['no_funds'] = "Votre credit est insuffisant pour cette operation"
MESSAGES['txt-3']['password_format_failed'] = "Votre nouveau mot de passe doit contenir 4 chiffres ou en alphanumerique"
MESSAGES['txt-3']['new_passwords_no_match'] = "Le nouveau mot de passe ne concorde pas. Veuillez verifier et reessayer plus tard"
MESSAGES['txt-3']['successful_password_change'] = "Votre mot de passe a ete change avec success. Merci"
MESSAGES['txt-3']['wrong_pin_password_change'] = "Votre mot de passe est incorrect. Veuillez reessayer s il vous plait"
MESSAGES['txt-3']['below_min'] = "Cher client, le transfert minimum autorise est %s Mo" % (str(MIN_AMOUNT))
MESSAGES['txt-3']['request_not_allowed'] = "Votre demande n a pas ete executee veuillez reessayer en envoyant  6Go de volume internet. Merci"
