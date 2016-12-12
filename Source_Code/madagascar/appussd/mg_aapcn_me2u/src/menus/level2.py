M3E1 = {
            'key' : False,
            'nextMenuId':"1-0-3-3",
            'type':'static',
            'txt-1':'Entrer le Go',
            'txt-2':'Entrer le Go',
            'txt-3':'Entrer le Go',
            'source':False,
        }

L2M3 = {'id':'1-0-2-3','leaf':True,'title':False,'footer':False,'response':"any",'service':False,'package':False,'parameter':"amount",'type':'static','checkpoint':False,'entries':[M3E1]}


M2E1 = {
            'key' : False,
            'nextMenuId':"1-0-3-2",
            'type':'static',
            'txt-1':'Entrer le Mo',
            'txt-2':'Entrer le Mo',
            'txt-3':'Entrer le Mo',
            'source':False,
        }

L2M2 = {'id':'1-0-2-2','leaf':True,'title':False,'footer':False,'response':"any",'service':False,'package':False,'parameter':"amount",'type':'static','checkpoint':False,'entries':[M2E1]}


M1E1 = {
            'key' : False,
            'nextMenuId':"1-0-3-1",
            'type':'static',
            'txt-1':'Enter your New Password',
            'txt-2':'Ampidiro ny teny miafina vaovao',
            'txt-3':'Veuillez entrer le nouveau mot de passe',
            'source':False,
        }

L2M1 = {'id':'1-0-2-1','leaf':True,'title':False,'footer':False,'response':"any",'service':False,'package':False,'parameter':"new_pin",'type':'static','checkpoint':False,'entries':[M1E1]}


level2 = {'id':0,'menus':[L2M1,L2M2,L2M3]}



