M4E1 = {

            'key' : False,
            'nextMenuId':False,
            'type':'dynamic',
            'source' : False,
            'txt-1': False,
            'txt-2': False,
            'source':'http://127.0.0.1:5550/process?msisdn=$msisdn&input=$ussdRequestString&is_bparty=1',

        }

L4M4 = {'id':'1-0-4-4','leaf': True,'title':False,'footer':False,'response':False,'service':False,'package':False,'parameter':False,'type':'dynamic','checkpoint':False,'entries':[M4E1]}


M3E1 = {

            'key' : False,
            'nextMenuId':False,
            'type':'dynamic',
            'source' : False,
            'txt-1': False,
            'txt-2': False,
            'source':'http://127.0.0.1:5550/changepin?msisdn=$msisdn&curr_pin=$curr_pin&new_pin=$new_pin&confirm_pin=$confirm_pin&lang=$language',

        }


L4M3 = {'id':'1-0-4-3','leaf': True,'title':False,'footer':False,'response':False,'service':False,'package':False,'parameter':False,'type':'dynamic','checkpoint':False,'entries':[M3E1]}


M2E1 = {

            'key' : False,
            'nextMenuId':False,
            'type':'dynamic',
            'source' : False,
            'txt-1': False,
            'txt-2': False,
            'source':'http://127.0.0.1:5550/provision?msisdn=$msisdn&b_number=$b_number&unit=GB&pin=$pin&amount=$amount&lang=$language',

        }


L4M2 = {'id':'1-0-4-2','leaf': True,'title':False,'footer':False,'response':False,'service':False,'package':False,'parameter':False,'type':'dynamic','checkpoint':False,'entries':[M2E1]}


M1E1 = {

            'key' : False,
            'nextMenuId':False,
            'type':'dynamic',
            'source' : False,
            'txt-1': False,
            'txt-2': False,
            'source':'http://127.0.0.1:5550/provision?msisdn=$msisdn&b_number=$b_number&unit=MB&pin=$pin&amount=$amount&lang=$language',

        }

L4M1 = {'id':'1-0-4-1','leaf': True,'title':False,'footer':False,'response':False,'service':False,'package':False,'parameter':False,'type':'dynamic','checkpoint':False,'entries':[M1E1]}

level4 = {'id':0,'menus':[L4M1,L4M2,L4M3,L4M4]}

