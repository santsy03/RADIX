# -*- coding: utf-8 -*-
PORT = {}
PORT['adaptor'] = '5054'


DA = {}
DA['14'] = 100 * 1024 #Data Night
DA['24'] = 250 * 1024# Facebook
DA['29'] = 900#FAF
DA['32'] = 250 * 1024# Whatsapp
DA['42'] = 30#Video Call
DA_LIST = [DA]


da_list = ['14','24','29','32','42']

HOUR = 23
MINUTE = 59
SECONDS = 59
OFFER_ID = 13

exp_days = 1

message = {}
message['txt-1'] = {}
message['txt-2'] = {}
message['txt-3'] = {}
message['txt-1']['success'] = 'Your subscription to COMBI offer was performed with success. Press *999*114*24# to know all benefits. Thank you'
message['txt-2']['success'] = 'Tontosa ny fangatahanao hampiasa ny tolotra COMBI. Tsindrio ny *999*114*24# hamantaranao ireo tombotsoa maro azonao. Misaotra tompoko'
message['txt-3']['success'] = 'Votre souscription a l offre COMBI a ete effectue avec succes. Tapez *999*114*24# pour connaitre les differentes avantages. Merci'
message['txt-1']['failure'] = 'Your request is not executed. Please retry later. Thank you'
message['txt-2']['failure'] = 'Tsy tontosa ny fangatahanao. Avereno afaka fotoana fohy azafady. Misaotra tompoko.'
message['txt-3']['failure'] = 'Votre souscription n a pas ete executee. Veuillez reessayer plus tard. Merci'
message['postpaid'] = 'Dear customer, this is service is not available for postpaid subscribers. Thank you for your interest.'
message['txt-1']['insuffcient'] = 'You have not enough credit to subscribe to  this offer. Please refill your account and retry. Thanks'
message['txt-2']['insuffcient'] = 'Tsy ampy hanaovanao an io tolotra io ny toe bolanao. Mampidira fahana azafady. Misaotra tompoko'
message['txt-3']['insuffcient'] = 'Vous n avez pas assez de credit pour souscrire a cette offre. Veuillez recharger votre compte avant de souscrire a nouveau . Merci'
message['wait'] = 'Dear customer your request has been received. You will receive a confirmation message shortly.'
message['conflict'] = 'Dear customer you are already subscribed to this service'
price = 2000
#price = 0
