# coding: utf8
from string import Template
cost = 2
fafId=1

response = {}
response['txt-1'] = {}
response['txt-2'] = {}
response['txt-3'] = {}

response['txt-1']['successfullyAdded'] = {}
response['txt-2']['successfullyAdded'] = {}
response['txt-3']['successfullyAdded'] ={}
response['txt-1']['successfullyAdded'] = Template('$fafNumber successfully added')
response['txt-2']['successfullyAdded'] = Template('(mg)$fafNumber successfully added')
response['txt-3']['successfullyAdded'] = Template('Numero $fafNumber ajoute avec succes. Merci')


response['txt-1']['successfullyDeleted'] = {}
response['txt-2']['successfullyDeleted'] = {}
response['txt-3']['successfullyDeleted'] ={}
response['txt-1']['successfullyDeleted'] = Template('$fafNumber successfully deleted')
response['txt-2']['successfullyDeleted'] = Template('(mg)$fafNumber successfully deleted')
response['txt-3']['successfullyDeleted'] = Template('(fr)You have successfully deleted this number $fafNumber')

response['txt-1']['fafList'] = {}
response['txt-2']['fafList'] = {}
response['txt-3']['fafList'] ={}
response['txt-1']['fafList'] = Template('Your friends are $list')
response['txt-2']['fafList'] = Template('Ireo friends anao dia $list')
response['txt-3']['fafList'] = Template('Vos numéros Friends sont $list')

response['txt-1']['numberDoesNotExist'] = {}
response['txt-2']['numberDoesNotExist'] = {}
response['txt-3']['numberDoesNotExist'] ={}
response['txt-1']['numberDoesNotExist'] = Template('Number $fafNumber does not exist in the list')
response['txt-2']['numberDoesNotExist'] = Template('Number $fafNumber does not exist in the list') 
response['txt-3']['numberDoesNotExist'] = Template('(fr)Number $fafNumber does not exist in the list')


response['txt-1']['invalidFaf'] = {}
response['txt-2']['invalidFaf'] = {}
response['txt-3']['invalidFaf'] ={}
response['txt-1']['invalidFaf'] = Template('The number you have entered is incorrect.Please insert a correct one')
response['txt-2']['invalidFaf'] = Template('(mg)The number you have entered is incorrect.Please insert a correct one')
response['txt-3']['invalidFaf'] = Template('Le numero entre est incorect. Veuillez corriger et reessayer. Merci')

response['txt-1']['fafAlreadyExists'] = {}
response['txt-2']['fafAlreadyExists'] = {}
response['txt-3']['fafAlreadyExists'] ={}
response['txt-1']['fafAlreadyExists'] = Template('$fafNumber already exists in another plan')
response['txt-2']['fafAlreadyExists'] = Template('(mg)$fafNumber already exists in another plan')
response['txt-3']['fafAlreadyExists'] = Template('Numero $fafNumber existe déjà dans votre liste.Merci')

response['txt-1']['confirmationText'] = {}
response['txt-2']['confirmationText'] = {}
response['txt-3']['confirmationText'] ={}
response['txt-1']['confirmationText'] = 'Your request is being processed.You will recieve a confirmation message shortly'
response['txt-2']['confirmationText'] = '(mg)Your request is being processed.You will recieve a confirmation message shortly'
response['txt-3']['confirmationText'] = 'Veuillez patienter, nous procedons a votre demande. Merci'

response['txt-1']['insufficientFunds'] = {}
response['txt-2']['insufficientFunds'] = {}
response['txt-3']['insufficientFunds'] ={}
response['txt-1']['insufficientFunds'] = 'Sorry, you do not have enough credit to make this request. thank you'
response['txt-2']['insufficientFunds'] = '(mg)Your request is being processed.You will recieve a confirmation message shortly'
response['txt-3']['insufficientFunds'] = 'Desole, vous n avez pas assez de credit pour effectuer cette requete. Merci'

response['txt-1']['fafAlreadyFull'] = {}
response['txt-2']['fafAlreadyFull'] = {}
response['txt-3']['fafAlreadyFull'] ={}
response['txt-1']['fafAlreadyFull'] = 'You have reached the maximum number of fafs.'
response['txt-2']['fafAlreadyFull'] = '(mg)You have reached the maximum number of fafs.'
response['txt-3']['fafAlreadyFull'] = 'You have reached the maximum number of fafs.'

response['txt-1']['errorAir'] = {}
response['txt-2']['errorAir'] = {}
response['txt-3']['errorAir'] ={}
response['txt-1']['errorAir'] = 'Error while processing your request. Please try again later. thank you'
response['txt-2']['errorAir'] = '(mg)Error while processing your request. Please try again later. thank you'
response['txt-3']['errorAir'] = 'Erreur lors du traitement de votre requete. Veuillez reessayer plus tard. Merci'
