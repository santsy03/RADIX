M5E1 = {
            'key' : False,
            'nextMenuId':"1-0-4-2",
            'type':'static',
            'txt-1':'Your have chosen to send $amount GB to $b_number. Enter password to proceed',
            'txt-2':'Nangataka ny handefa $amount Go ianao any $b_number.Ampidiro ny teny miafina hanatontosana izany',
            'txt-3':"Vous avez choisi d'envoyer $amount Go a $b_number. Entrez votre mot de passe pour y proceder",
            'source':False,
        }

L3M5 = {'id':'1-0-3-5','leaf':False,'title':False,'footer':False,'response':"any",'service':False,'package':False,'parameter':"pin",'type':'static','checkpoint':False,'entries':[M5E1]}


M4E1 = {
            'key' : False,
            'nextMenuId':"1-0-4-1",
            'type':'static',
            'txt-1':'Your have chosen to send $amount MB to $b_number. Enter password to proceed',
            'txt-2':'Nangataka ny handefa $amount Mo ianaoi any $b_number. Ampidiro ny teny miafina hanatontosana izany',
            'txt-3':"Vous avez choisi d'envoyer $amount Mo a $b_number. Entrez votre mot de passe pour y proceder",
            'source':False,
        }

L3M4 = {'id':'1-0-3-4','leaf':False,'title':False,'footer':False,'response':"any",'service':False,'package':False,'parameter':"pin",'type':'static','checkpoint':False,'entries':[M4E1]}



M3E1 = {
            'key' : False,
            'nextMenuId':"1-0-3-5",
            'type':'static',
            'txt-1':'Your have chosen to send $amount GB. Enter the mobile number',
            'txt-2':'Nangataka ny handefa $amount Go ianao. Ampidiro ny laharana finday andefasana azy.',
            'txt-3':"Vous avez choisi d'envoyer $amount Go. Entrez le numero de telephone",
            'source':False,
        }

L3M3 = {'id':'1-0-3-3','leaf':False,'title':False,'footer':False,'response':"any",'service':False,'package':False,'parameter':"b_number",'type':'static','checkpoint':False,'entries':[M3E1]}


M2E1 = {
            'key' : False,
            'nextMenuId':"1-0-3-4",
            'type':'static',
            'txt-1':'Your have chosen to send $amount MB. Enter the mobile number',
            'txt-2':'Nangataka ny handefa $amount Mo ianao. Ampidiro ny laharana finday andefasana azy.',
            'txt-3':"Vous avez choisi d'envoyer $amount Mo. Entrez le numero de telephone",
            'source':False,
        }

L3M2 = {'id':'1-0-3-2','leaf':False,'title':False,'footer':False,'response':"any",'service':False,'package':False,'parameter':"b_number",'type':'static','checkpoint':False,'entries':[M2E1]}


M3E1 = {
            'key' : False,
            'nextMenuId':"1-0-4-3",
            'type':'static',
            'txt-1':'Confirm your New Password',
            'txt-2':'Fanamafisana ny teny miafina vaovao',
            'txt-3':'Confirmer le nouveau mot de passe',
            'source':False,
        }

L3M1 = {'id':'1-0-3-1','leaf':False,'title':False,'footer':False,'response':"any",'service':False,'package':False,'parameter':"confirm_pin",'type':'static','checkpoint':False,'entries':[M3E1]}

level3 = {'id':0,'menus':[L3M1,L3M2,L3M3,L3M4,L3M5]}

