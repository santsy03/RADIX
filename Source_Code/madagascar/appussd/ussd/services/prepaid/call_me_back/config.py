# coding: utf-8

time_1 = '2015-01-07'
time_2 = '2015-01-08'

responses = {}
responses['True']={}
responses['False']={}


(responses['True'])['txt-1'] = 'Request successfully sent to $recipient. You can send $requestsdiff more requests today'
(responses['True'])['txt-2'] = "Nangataka ho antsoin'ny laharana $recipient ianao.Ambiny: $requestsdiff"
(responses['True'])['txt-3'] = "Vous avez demande a etre rappele par le numero $recipient.Reste: $requestsdiff"

(responses['False'])['txt-1'] = 'You have already used all of your Call Me Back requests.'
(responses['False'])['txt-2'] = 'Tratra ny FONEO 10 afaka ampiasainao anio. Misaotra Tompoko'
(responses['False'])['txt-3'] = "Vous avez utilisez les 10 FONEO que vous disposez pour aujourd'hui. Merci."

responses['failedValidation'] = {}
responses['failedValidation']['txt-1'] = 'Request is not processed. The number you have entered is incorrect. Please try again.'
responses['failedValidation']['txt-2'] = "Misy diso ny nomerao nampidirinao.Misaotra Tompoko."
responses['failedValidation']['txt-3'] = "Le numero entre est incorect. Veuillez corriger et reessayer. Merci"

responses['success'] = {}
#responses['success']['txt-1'] = 'You have asked $recipient to call you back. Out of credit? No worry, use SOS Credit.Press *500#'
responses['success']['txt-1'] = 'You have asked $recipient to call you back.Enjoy long call with FUN COOL: OAr to friends, Ar1 to Airtel, Ar3 off network.Press *100*12# for 950Ar'
#responses['success']['txt-2'] = "Nangataka ho antsoin ny laharana $recipient ianao. Mila miantso maikave ianao nefa tsy manana fahana? ampiasao SOS Credit , antsoy *500#"
responses['success']['txt-2'] = "Nangataka ho antsoin ny laharana $recipient ianao. Te hiresaka ela? Mampiasa FUN COOL: OAr miantso friends,1Ar Airtel,3Ar ny hafa.Antsoy *100*12# . Sarany 950Ar"
#responses['success']['txt-3'] = "Vous avez demande a etre rappele par $recipient.En panne de credit? SOS Credit est la solution.Tapez *500#"
responses['success']['txt-3'] = "Vous avez demande a etre rappele par $recipient. Parlez sans vous retenir avec FUN COOL: OAr friends,1Ar Airtel,3Ar autres operateurs.Code *100*12#.Cout: 950Ar"


responses['one']={}
responses['one']['txt-1'] = 'Request successfully sent to $recipient. You can send $requestsdiff more request today'
responses['one']['txt-2'] = "Nangataka ho antsoin'ny laharana $recipient ianao.Ambiny: $requestsdiff"
responses['one']['txt-3'] = "Vous avez demande a etre rappele par le numero $recipient.Reste: $requestsdiff"

responses['zero'] = {}
responses['zero']['txt-1'] = 'You have already used all of your Call Me Back requests.'
responses['zero']['txt-2'] = 'Tratra ny FONEO 10 afaka ampiasainao anio. Misaotra Tompoko'
responses['zero']['txt-3'] = "Vous avez utilisez les 10 FONEO que vous disposez pour aujourd'hui. Merci."

responses['offnet'] = {}
responses['offnet']['txt-1'] = 'Request is not processed. PCM service is available only for Airtel Customers.'
responses['offnet']['txt-2'] = 'Misy fahadisoana ny fangatahana nataonao.'
responses['offnet']['txt-3'] = 'Desole, la commande que vous avez effectue n est pas valide. Merci'

responses['wrongNumber'] ={}

responses['wrongNumber']['txt-1'] = 'Request is not processed. The number you have entered is incorrect. Please try again.'
responses['wrongNumber']['txt-2'] = 'Misy diso ny nomerao nampidirinao.Misaotra Tompoko.'
responses['wrongNumber']['txt-3'] = 'Le numero entre est incorect. Veuillez corriger et reessayer. Merci'

responses['b_party_message'] = {}
#responses['b_party_message']['txt-1'] = 'FONEO:The %s would like to recieve a call or credit from you. Enjoy 6 times more with BOOST. Press *100*101# .Cost Ar 1000.Thanks'
responses['b_party_message']['txt-1'] = 'FONEO:The %s would like to receive a call or credit from you. But u can also offer FUN COOL as a gift.Just press *100*12*recipient# ok.Cost 950Ar'
#responses['b_party_message']['txt-2'] = '%s FONEO aho na andefaso fahana azafady.Mibontsina avo 6 heny ny 1000Ar miaraka @ BOOST. Andramo anie. Fidirana *100*100#'
responses['b_party_message']['txt-2'] = '%s FONEO aho na andefaso fahana azafady.Azo atao ihany koa ny mandefa FUN COOL. Tsindrio *100*12*nomerao andefasana# ok.Sarany 950Ar'
#responses['b_party_message']['txt-3'] = 'FONEO:Le %s demande a etre rappele ou recevoir de credit de votre part.Misez sur BOOST a Ar1000 et gagnez 6 fois plus de credit.Code *100*101#. Merci'
responses['b_party_message']['txt-3'] = 'FONEO:le %s demande a etre rappele ou recevoir de credit de votre part. Ou offrez lui plutot FUN COOL en cadeau *100*12*destinataire# ok. Cout 950Ar'

responses['message_1'] = {}
responses['message_1']['txt-1'] = ("You have asked %s to call you back . "
        +"You know what ? Lowest pack is at Airtel."
        +"With FUN 100 , you can get 40sec for  100Ar.Press *100*1#")
responses['message_1']['txt-2'] = ("Nangataka ho antsoin ny laharana %s ianao."
        +" Vita hatreo ny mi-bip na miandry antsoina miaraka @ FUN100,"
        +" Ar 100 dia ahafahanao miantso. Tsindrio *100*1#")
responses['message_1']['txt-3'] = ("Vous avez demande a etre rappele par %s."
        +" Le saviez vous ? FUN 100 de Airtel vous offre 40 sec d appel pour"
        + "seulement 100 Ar .Acces *100*1#")


responses['message_2'] = {}
responses['message_2']['txt-1'] = ("You have asked %s to call you back . "
        +"Out of credit ? No worry ,use SOS CREDIT. Press *500#")
responses['message_2']['txt-2'] = ("Nangataka ho antsoin ny laharana %s"
        +" ianao. Mila miantso maika ve ianao nefa tsy manana fahana,"
        +" ampiasao SOS Credit, antsoy *500#")
responses['message_2']['txt-3'] = ("Vous avez demande a etre rappele par %s."
        +" En panne de credit ? SOS Credit est la solution. Tapez *500#")

responses['message_3'] = {}
responses['message_3']['txt-1'] = ("You have asked %s to call you back."
        +"You know what ? Lowest pack is at Airtel.With FUN 100 ,"
        +" you can get 40sec for  100Ar.Press *100*1#")
responses['message_3']['txt-2'] = ("Nangataka ho antsoin ny laharana %s"
        +" ianao. Vita hatreo ny mi-bip na miandry antsoina miaraka"
        +" @ FUN100, Ar 100 dia ahafahanao miantso. Tsindrio *100*1#")
responses['message_3']['txt-3'] = ("Vous avez demande a etre rappele par %s."
        +" Le saviez vous ? FUN 100 de Airtel vous offre 40 sec d appel"
        +" pour seulement 100 Ar .Acces *100*1#")

'''madagascar'''
countryCode = '261'
messageSender = '298'
