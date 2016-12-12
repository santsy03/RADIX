from data_provisioning.src.configs.core import web_services_port

HOST_NAME = __import__('socket').gethostname()

message = {}
message['txt-1'] = {}
message['txt-2'] = {}
message['txt-3'] = {}

message['txt-1']['first_before_one'] = "Your subscription to MyMeg30 is successfuly excecuted, offer valid 4hours. Your next subscription will be billed 150 Ar only. Thank you."
message['txt-2']['first_before_one'] = "Tontosa ny fangatahanao hampiasa ny MyMeg30, manankery adiny 4.Ny saran ny fidiranao fanindroany dia hihena ho 150 Ariary. Misaotra tompoko"
#message['txt-2']['first_before_one'] = "Tafiditra ny fidirana voalohany @ MyMeg30, manankery adiny 4. Miampy 10 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."
message['txt-3']['first_before_one'] = "Votre souscription a MyMeg30 est executee, valable 4 heures. Votre 2eme souscription de la journee sera facturee a 150 Ariary seulement.Merci"


message['txt-1']['first_after_one'] = "Your subscription to MyMeg30 is successfully executed, offer valid till 5 pm. Your next subscription will be billed 150 Ar. Thank you"

message['txt-2']['first_after_one'] = "Tontosa ny fangatahanao hampiasa ny MyMeg30, manankery hatr@5 hariva. Ny saran ny fidiranao fanindroany dia hihena ho 150 Ariary. Misaotra tompoko"

message['txt-3']['first_after_one'] = "Votre souscription a MyMeg30 est executee, valable jusqu a 17 heures. Votre 2eme souscription de la journee sera facturee 150 Ariary seulement. Merci"

message['txt-1']['second_before_three'] = "Your second subscription to MyMeg30 is successfully executed, offer valid 2 hours. Your third subscription will be billed 50 Ariary only. Thank you"

message['txt-2']['second_before_three'] = "Tontosa ny fidiranao faharoa @ MyMeg30 mananakery adiny 2.Ny saran ny fidiranao fahatelo androany dia hihena ho 50 Ariary. Misaotra tompoko."
#message['txt-2']['second_before_three'] = "Tafiditra ny fidirana faharoa @ MyMeg30, manankery adiny 2. Miampy 10 ny isanao @ promo fahaleovantena. Tsindrio ny *999*55# raha hijery ireo isa efa azonao."

message['txt-3']['second_before_three'] = "Votre 2eme souscription a MyMeg30 est executee, valable pendant 2h. Votre 3eme souscription de la journee sera facturee a 50 Ariary seulement .Merci"


message['txt-1']['second_after_three'] = "Your second subscription to MyMeg30 is successfully executed, offer valid till 5 pm. Your third subscription will be billed 50 Ar only. Thank you"

message['txt-2']['second_after_three'] = "Tontosa ny fidiranao faharoa @MyMeg30, manankery hatr@ 5 hariva. Ny saran ny fidiranao fahatelo androany dia hihena ho 50 Ariary. Misaotra tompoko"

message['txt-3']['second_after_three'] = "Votre 2eme souscription a MyMeg30 est executee, offre valable jusqu a 17h. Votre 3eme sourscription de la journee sera facturee a 50 Ariary. Merci"

message['txt-1']['third'] = "Your third subscription to MyMeg30 is successfully executed, offer valid till 5 pm. Thank you"

message['txt-2']['third'] = "Tontosa ny fidiranao fahatelo @MyMeg30, manankery hatr@5 hariva. Misaotra tompoko"

message['txt-3']['third'] = "Votre 3eme souscription a MyMeg30 est executee offre valable jusqu a 17h. Merci"

message['txt-1']['past_time'] = "MyMeg30 is availble till 5 pm only. Please use MyMy50 *114*4#"

message['txt-2']['past_time'] = "Ny fidirana @ io tolotra io dia misokatra hatr@ 5 ora hariva ihany. Manasa anao hampiasa MyMeg50 *114*4#. Misaotra tompoko"

message['txt-3']['past_time'] = "Cette offre est disponible jusqu a 17 h. Veuillez utiliser MyMeg50 *114*4#. Merci"

message['txt-1']['wait'] = "Your request is being processed, please wait. You will receive confirmation shortly. Thank you"

message['txt-2']['wait'] = "Eto ampanatontosana ny fangatahanao. Mahandrasa kely azafady. Misaotra tompoko"

message['txt-3']['wait'] = "Votre demande est en cours de traitement, veullez patienter. Nous voucs enverrons une confirmation. Merci"

message['error'] = 'An error occured. Please try again later or contact customer care.'

message['insufficient_funds'] = "Vous n'avez pas assez de credit pour vous abonner. Merci de recharger votre compte"

message['txt-1']['exceed_three_subscription'] = 'You have reached the maximum count of subscriptions authorized today. Thank you'
message['txt-2']['exceed_three_subscription'] = 'Efa tratra ny fetra hahafahanao mampiasa an\'io tolotra io anio. Misaotra tompoko.'
message['txt-3']['exceed_three_subscription'] = 'Vous avez atteint le nombre de souscription autorise pour ce jour. Merci'

PROVISION_URL =  "http://127.0.0.1:%s/submitProvision?"%str(web_services_port)
AUTH_KEY = 'mgaapcnuser'
ACCOUNT_ID = 'mgaapcn'
ROUTING_KEY = "tel_mg_data"
queue_name = 'telescopic_data_queue'
LOG_NAME = 'data_telescopic_log-{}'.format(HOST_NAME)
PID_FILE = '/appussd/telescopic_interface/consumer/telescopic_daemon-{}.pid'.format(HOST_NAME)
CWD = '/appussd/telescopic_interface/consumer/'

ONE = 13
THREE = 15
