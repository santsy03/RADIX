
M1E1 = {

            'key' : False,
            'nextMenuId':False,
            'type':'dynamic',
            'source' : False,
            'txt-1': False,
            'txt-2': False,
            'source':'http://127.0.0.1:7991/process?msisdn=$msisdn&input=$ussdRequestString&can_renew=0&is_bparty=1',

        }

L4M1 = {'id':'1-0-4-1','leaf': True,'title':False,'footer':False,'response':False,'service':False,'package':False,'parameter':False,'type':'dynamic','checkpoint':False,'entries':[M1E1]}

level4 = {'id':0,'menus':[L4M1]}

