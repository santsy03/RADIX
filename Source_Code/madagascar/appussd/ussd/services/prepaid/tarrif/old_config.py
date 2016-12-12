from string import Template
names = {}
names['6'] = 'jiaby_jiaby_with_international_per_min'
names['7'] = 'jiaby_jiaby_with_international_per_sec'
names['12'] = 'sky_with_international_per_min'
names['13'] = 'sky_with_international_per_sec'
names['98']  = 'RTA'
names['84']  = 'Business'
names['85']  = 'Business'


response = {}
response['txt-1'] = {}
response['txt-2'] = {}
response['txt-3'] = {}

response['txt-1']['successfullyCheckedTarrif'] = Template('You are currently on the $name tarrif.')
response['txt-2']['successfullyCheckedTarrif'] = Template('Tompoko, ianao dia mampiasa ny tarif $name.')
response['txt-3']['successfullyCheckedTarrif'] = Template('Votre tarif actuel est $name.')

response['txt-1']['errorAir'] = 'Error while processing your request. Please try again later. thank you'
response['txt-2']['errorAir'] = '(mg)Error while processing your request. Please try again later. thank you'
response['txt-3']['errorAir'] = 'Erreur lors du traitement de votre requete. Veuillez reessayer plus tard. Merci'

response['txt-1']['successfullySetServiceClass'] = 'Your tarrif plan change was successful'
response['txt-2']['successfullySetServiceClass'] = '(mg)Your tarrif plan change was successful'
response['txt-3']['successfullySetServiceClass'] = 'Vous utilisez actuelement le tarif'

response['txt-1']['insufficientFunds'] = 'Sorry, you do not have enough credit to make this request. thank you'
response['txt-2']['insufficientFunds'] = '(mg)Sorry, you do not have enough credit to make this request. thank you'
response['txt-3']['insufficientFunds'] = 'Desole, vous n avez pas assez de credit pour effectuer cette requete. Merci'

response['txt-1']['notAllowed'] = 'Sorry, you can not change your tariff yet. thank you' 
response['txt-2']['notAllowed'] = '(mg)Sorry, you can not change your tariff yet. thank you'
response['txt-3']['notAllowed'] = 'Desole, vous ne pouvez pas changer votre tarif pour le moment. Merci'
