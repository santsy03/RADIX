# coding: utf8
from string import Template
cost = '2150'
fafId = 1

response = {}
response['txt-1'] = {}
response['txt-2'] = {}
response['txt-3'] = {}

response['txt-1']['successfullyAdded'] = {}
response['txt-2']['successfullyAdded'] = {}
response['txt-3']['successfullyAdded'] ={}
response['txt-1']['successfullyAdded'] = Template('$fafNumber successfully added')
response['txt-2']['successfullyAdded'] = Template('Tontosa ny fampidiranao ny nomerao $fafNumber ho isan ny Friends-nao.')
response['txt-3']['successfullyAdded'] = Template('Le numero $fafNumber a ete rajoute avec success a votre liste de Friends')


response['txt-1']['successfullyDeleted'] = {}
response['txt-2']['successfullyDeleted'] = {}
response['txt-3']['successfullyDeleted'] ={}
response['txt-1']['successfullyDeleted'] = Template('You have successfully deleted this number $fafNumber ')
response['txt-2']['successfullyDeleted'] = Template('Tonotosa ny famafana ny nomerao $fafNumber nataonao')
response['txt-3']['successfullyDeleted'] = Template('Le numero $fafNumber a ete supprime avec succes')

response['txt-1']['fafList'] = {}
response['txt-2']['fafList'] = {}
response['txt-3']['fafList'] ={}
response['txt-1']['fafList'] = Template('Your friends are $list')
response['txt-2']['fafList'] = Template('Ireo friends anao dia $list')
response['txt-3']['fafList'] = Template('Vos numeros Friends sont $list')

response['txt-1']['numberDoesNotExist'] = {}
response['txt-2']['numberDoesNotExist'] = {}
response['txt-3']['numberDoesNotExist'] ={}
response['txt-1']['numberDoesNotExist'] = Template('Number $fafNumber does not exist in the list')
response['txt-2']['numberDoesNotExist'] = Template('Ny nomerao $fafNumber dia tsy anisan friends-nao ny') 
response['txt-3']['numberDoesNotExist'] = Template('le numero $fafNumber ne figure pas parmi vos numeros friends')


response['txt-1']['invalidFaf'] = {}
response['txt-2']['invalidFaf'] = {}
response['txt-3']['invalidFaf'] ={}
response['txt-1']['invalidFaf'] = Template('The number you have entered is incorrect.Please insert a correct one')
response['txt-2']['invalidFaf'] = Template('Misy diso ny nomerao nampidirinao.Misaotra Tompoko.')
response['txt-3']['invalidFaf'] = Template('Le numero entre est incorect. Veuillez corriger et reessayer. Merci')

response['txt-1']['fafAlreadyExists'] = {}
response['txt-2']['fafAlreadyExists'] = {}
response['txt-3']['fafAlreadyExists'] ={}
response['txt-1']['fafAlreadyExists'] = Template('$fafNumber already exists in the list')
response['txt-2']['fafAlreadyExists'] = Template('Efa anisan ny nomerao $fafNumber frinds-nao ny nomerao nampidirinao.Misaotra Tompoko')
response['txt-3']['fafAlreadyExists'] = Template('Numero $fafNumber existe déjà dans votre liste.Merci')

response['txt-1']['confirmationText'] = {}
response['txt-2']['confirmationText'] = {}
response['txt-3']['confirmationText'] ={}
response['txt-1']['confirmationText'] = 'Your request is in progress. You will shortly receive a confirmation by message.'
response['txt-2']['confirmationText'] = 'Ho alefanay sms tsy ho ela aminao ny valin ny fangatahanao.'
response['txt-3']['confirmationText'] = 'Nous avons recu votre demande, nous vous enverrons la confirmation par sms.'

response['txt-1']['insufficientFunds'] = {}
response['txt-2']['insufficientFunds'] = {}
response['txt-3']['insufficientFunds'] ={}
response['txt-1']['insufficientFunds'] = 'Sorry, you do not have enough credit to make this request. thank you'
response['txt-2']['insufficientFunds'] = 'Tsy ampy ahafahanao manova ny friend-nao ny toe bolanao.Misaotra Tompoko'
response['txt-3']['insufficientFunds'] = 'Desole, vous n avez pas assez de credit pour effectuer cette requete. Merci'

response['txt-1']['fafAlreadyFull'] = {}
response['txt-2']['fafAlreadyFull'] = {}
response['txt-3']['fafAlreadyFull'] ={}
response['txt-1']['fafAlreadyFull'] = 'The maximum number of friends has been reached'
response['txt-2']['fafAlreadyFull'] = 'Tratra ny isa na nomerao 3 friends afaka ampidirinao'
response['txt-3']['fafAlreadyFull'] = 'Vous avez atteint le nombre maximun de numero friends'

response['txt-1']['errorAir'] = {}
response['txt-2']['errorAir'] = {}
response['txt-3']['errorAir'] ={}
response['txt-1']['errorAir'] = 'Error while processing your request. Please try again later. thank you'
response['txt-2']['errorAir'] = 'Erreur lors du traitement de votre requete. Veuillez reessayer plus tard. Merci'
response['txt-3']['errorAir'] = 'Erreur lors du traitement de votre requete. Veuillez reessayer plus tard. Merci'
