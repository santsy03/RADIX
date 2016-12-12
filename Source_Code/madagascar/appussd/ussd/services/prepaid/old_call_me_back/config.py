# coding: utf-8
msgcount = 10
responses = {}
message = {}
responses['True']={}
responses['False']={}
responses['invalid'] = {}

(responses['True'])['txt-3'] = "Votre appel m'a Retour Demander à $recipient a été envoyé. Vous avez utilisé $requests de vos 10 Rappelez-moi messages pour aujourd'hui."
(responses['True'])['txt-1'] = 'Your call me back request to $recipient has been sent. You have used $requests of your 10 call me back messages for today.'
(responses['True'])['txt-2'] = '(mg)Your call me back request to $recipient has been sent. You have used $requests of your 10 call me back messages for today.'

(responses['False'])['txt-3'] = "Vous avez déjà utilisé l'ensemble de vos demandes de Rappelez-moi."
(responses['False'])['txt-1'] = 'You have already used all of your Call Me Back requests.'
(responses['False'])['txt-2'] = '(mg)You have already used all of your Call Me Back requests.'

(responses['invalid'])['txt-3'] = "Vous avez entré un numéro non valide."
(responses['invalid'])['txt-1'] = "(eng)Vous avez entré un numéro non valide."
(responses['invalid'])['txt-2'] = "(mg)Vous avez entré un numéro non valide."

message['txt-3'] = "Veuillez m'appeler au $msisdn. Merci."
message['txt-1'] = "(eng)Veuillez m'appeler au $msisdn. Merci."
message['txt-2'] = "(mg)Veuillez m'appeler au $msisdn. Merci."
