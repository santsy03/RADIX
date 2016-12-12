# coding: utf8
from string import Template

cost = '510'
names = {}
names['6'] = {}
names['7'] = {}
names['12'] = {}
names['13'] = {}
names['14'] = {}
names['20'] = {}
names['21'] = {}
names['22'] = {}
names['23'] = {}
names['27'] = {}
names['28'] = {}
names['29'] = {}
names['84'] = {}
names['85'] = {}
names['98'] = {}
names['515'] = {}

names['6']['txt-1'] = 'Tariff Jiaby Jiaby with international access per Minute'
names['6']['txt-2'] = 'Tarif Jiaby Jiaby miaraka @ international isa minitra'
names['6']['txt-3'] = 'Tarif Jiaby Jiaby avec international a la Minute'

names['7']['txt-1'] = 'Tariff Jiaby Jiaby with international access per Second'
names['7']['txt-2'] = 'Tarif Jiaby Jiaby miaraka @ international isa tsegondra'
names['7']['txt-3'] = 'Tarif Jiaby Jiaby avec international a la Seconde'

names['12']['txt-1'] = 'Tariff SKY with international access per Minute'
names['12']['txt-2'] = 'Tarif SKY  miaraka @ international isa minitra'
names['12']['txt-3'] = 'Tarif SKY avec international a la Minute'

names['13']['txt-1'] = 'Tariff SKY with international access per Second'
names['13']['txt-2'] = 'Tarif SKY miaraka @ international isa tsegondra'
names['13']['txt-3'] = 'Tarif SKY avec international a la Seconde'

names['14']['txt-1'] = 'Tariff credit Speed'
names['14']['txt-2'] = 'Tarif credit Speed'
names['14']['txt-3'] = 'Tarif credit Speed'

names['20']['txt-1'] = 'Tariff Jiaby Jiaby with international access per Minute'
names['20']['txt-2'] = 'Tarif Jiaby Jiaby miaraka @ international isa minitra'
names['20']['txt-3'] = 'Jiaby Jiaby avec international a la Minute'

names['21']['txt-1'] = 'Tariff Jiaby Jiaby with international access per Second' 
names['21']['txt-2'] =  'Tarif Jiaby Jiaby miaraka @ international isa tsegondra'
names['21']['txt-3'] = 'Tarif Jiaby Jiaby avec international a la Seconde'

names['22']['txt-1'] = 'Jiaby Jiaby with international access per Minute' 
names['22']['txt-2'] = 'Tarif Jiaby Jiaby miaraka @ international isa minitra'
names['22']['txt-3'] = 'Jiaby Jiaby avec international a la Minute'

names['23']['txt-1'] = 'Jiaby Jiaby with international access per Second'
names['23']['txt-2'] = 'Tarif Jiaby Jiaby miaraka @ international isa tsegondra'
names['23']['txt-3'] = 'Tarif Jiaby Jiaby avec international a la Seconde'

names['27']['txt-1'] = 'Airtel Community'
names['27']['txt-2'] = 'Airtel Community'
names['27']['txt-3'] = 'Airtel Community'

names['28']['txt-1'] = 'Airtel Community'
names['28']['txt-2'] = 'Airtel Community'
names['28']['txt-3'] = 'Airtel Community'

names['29']['txt-1'] = 'Tariff employee perso'
names['29']['txt-2'] = 'Tarif employe perso'
names['29']['txt-3'] = 'Tarif employe perso'

names['84']['txt-1']  = 'Tariff Business'
names['84']['txt-2']  = 'Tarif Business'
names['84']['txt-3']  = 'Tarif Business'

names['85']['txt-1']  = 'Tariff Business default'
names['85']['txt-2']  = 'Tarif Business default'
names['85']['txt-3']  = 'Tarif Business default'

names['98']['txt-1'] = 'RTA Mobile'
names['98']['txt-2'] = 'RTA Mobile'
names['98']['txt-3'] = 'RTA Mobile'

names['515']['txt-1'] = 'Tariff KORANA'
names['515']['txt-2'] = 'Tarif KORANA'
names['515']['txt-3'] = 'Tarif KORANA'

response = {}
response['txt-1'] = {}
response['txt-2'] = {}
response['txt-3'] = {}

response['txt-1']['successfullyCheckedTarrif'] = Template('You are currently on the $name.')
response['txt-2']['successfullyCheckedTarrif'] = Template('Tompoko, ianao dia mampiasa ny $name.')
response['txt-3']['successfullyCheckedTarrif'] = Template('Votre tarif actuel est $name.')

response['txt-1']['errorAir'] = 'Error while processing your request. Please try again later. thank you'
response['txt-2']['errorAir'] = 'Erreur lors du traitement de votre requete. Veuillez reessayer plus tard. Merci'
response['txt-3']['errorAir'] = 'Erreur lors du traitement de votre requete. Veuillez reessayer plus tard. Merci'

response['txt-1']['successfullySetServiceClass'] = 'Your tarrif plan change was successful'
response['txt-2']['successfullySetServiceClass'] = 'Tontosa ny fangatahanao.Misaotra Tompoko.'
response['txt-3']['successfullySetServiceClass'] = 'Vous utilisez actuelement le tarif'

response['txt-1']['insufficientFunds'] = 'Sorry, you do not have enough credit to make this request. thank you'
response['txt-2']['insufficientFunds'] = 'Tsy ampy ahafahanao manova ny friend-nao ny toe bolanao.Misaotra Tompoko'
response['txt-3']['insufficientFunds'] = 'Desole, vous n avez pas assez de credit pour effectuer cette requete.Merci'

response['txt-1']['notAllowed'] = 'Sorry, you can not change your tariff yet. thank you' 
response['txt-2']['notAllowed'] = 'Tompoko,Mbola tsy afaka manova ny tarif-nao ianao ankehitriny.Misaotra Tompoko.'
response['txt-3']['notAllowed'] = 'Desole, vous ne pouvez pas changer votre tarif pour le moment. Merci'

response['txt-1']['sos'] = 'Your request is not executed, your number is not allowed to perform this change. Please clean up your SOS CREDIT account prior to change. Thanks'
response['txt-2']['sos'] = 'Mbola tsy afaka manao fanovana tarif ny nomeraonao. Azafady, mampidira fahana hanadiovana ny kaonty SOS CREDIT nao. Misaotra tompoko'
response['txt-3']['sos'] = 'Votre demande ne peut pas etre executee pour le moment. Veuillez prealablement apurer votre compte SOS CREDIT. Merci'

# list of service classes that are not eligible for tarrif change
disallowed_sc = [66, 67, 69, 105, 106, 107, 108, 109, 110]
