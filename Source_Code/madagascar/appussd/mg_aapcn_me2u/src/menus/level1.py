M2E1 = {
            'key' : '1',
            'nextMenuId':'1-0-2-1',
            'type':'static',
            'txt-1':'Enter your current password',
            'txt-2':'Ampidiro ny teny miafina  ankehitriny',
            'txt-3':'Veuillez entrer votre mot de passe actuel',
            'source':False
        }

L1M2 = {'id':'1-0-1-2','leaf':False,'title':'Select','footer':False,'response':'any','service':False,'package':False,'parameter':"curr_pin",'type':'static','checkpoint':True,'entries':[M2E1]}

M1E2 = {
            'key' : '2',
            'nextMenuId':'1-0-2-3',
            'type':'static',
            'txt-1':'2. Send in GB',
            'txt-2':'2. Mandefa Go',
            'txt-3':'2. Envoi en Go',
            'source': False
        }

M1E1 = {
            'key' : '1',
            'nextMenuId':'1-0-2-2',
            'type':'static',
            'txt-1':'1. Send in MB',
            'txt-2':'1. Mandefa Mo',
            'txt-3':'1. Envoi en Mo',
            'source':False
        }

L1M1 = {'id':'1-0-1-1','leaf':False,'title':'Select','footer':False,'response':'key','service':False,'package':False,'parameter':False,'type':'static','checkpoint':True,'entries':[M1E1,M1E2]}

level1 = {'id':0,'menus':[L1M1,L1M2]}
