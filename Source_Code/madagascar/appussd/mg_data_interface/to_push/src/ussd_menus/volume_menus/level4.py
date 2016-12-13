M7E1 = {

            'key' : False,
            'nextMenuId':False,
            'type':'dynamic',
            'source' : False,
            'txt-1': False,
            'txt-2': False,
            'source':'http://127.0.0.1:7867/process?msisdn=$msisdn&input=$ussdRequestString',

        }

L4M7 = {'id':'1-0-4-7','leaf': True,'title':False,'footer':False,'response':False,'service':False,'package':False,'parameter':False,'type':'dynamic','checkpoint':False,'entries':[M7E1]}

M6E1 = {

            'key' : False,
            'nextMenuId':False,
            'type':'dynamic',
            'source' : False,
            'txt-1': False,
            'txt-2': False,
            'source':'http://127.0.0.1:4045/process?msisdn=$msisdn&input=$ussdRequestString&can_renew=0&package_id=59',

        }

L4M6 = {'id':'1-0-4-6','leaf': True,'title':False,'footer':False,'response':False,'service':False,'package':False,'parameter':False,'type':'dynamic','checkpoint':False,'entries':[M6E1]}


M5E1 = {

            'key' : False,
            'nextMenuId':False,
            'type':'dynamic',
            'source' : False,
            'txt-1': False,
            'txt-2': False,
            'source':'http://127.0.0.1:2031/process?msisdn=$msisdn&action=activate&sessionId=$sessionId',

        }

L4M5 = {'id':'1-0-4-5','leaf': True,'title':False,'footer':False,'response':False,'service':False,'package':False,'parameter':False,'type':'dynamic','checkpoint':False,'entries':[M5E1]}


M4E1 = {

            'key' : False,
            'nextMenuId':False,
            'type':'dynamic',
            'source' : False,
            'txt-1': False,
            'txt-2': False,
            'source':'http://127.0.0.1:7990/process?msisdn=$msisdn&input=$ussdRequestString&is_bparty=1',

        }

L4M4 = {'id':'1-0-4-4','leaf': True,'title':False,'footer':False,'response':False,'service':False,'package':False,'parameter':False,'type':'dynamic','checkpoint':False,'entries':[M4E1]}


M3E1 = {

            'key' : False,
            'nextMenuId':False,
            'type':'dynamic',
            'source' : False,
            'txt-1': False,
            'txt-2': False,
            'source':'http://127.0.0.1:7990/process?msisdn=$msisdn&input=$ussdRequestString&disable_renew=1',

        }


L4M3 = {'id':'1-0-4-3','leaf': True,'title':False,'footer':False,'response':False,'service':False,'package':False,'parameter':False,'type':'dynamic','checkpoint':False,'entries':[M3E1]}


M2E1 = {

            'key' : False,
            'nextMenuId':False,
            'type':'dynamic',
            'source' : False,
            'txt-1': False,
            'txt-2': False,
            'source':'http://127.0.0.1:7990/process?msisdn=$msisdn&input=$ussdRequestString&can_renew=1',

        }


L4M2 = {'id':'1-0-4-2','leaf': True,'title':False,'footer':False,'response':False,'service':False,'package':False,'parameter':False,'type':'dynamic','checkpoint':False,'entries':[M2E1]}


M1E1 = {

            'key' : False,
            'nextMenuId':False,
            'type':'dynamic',
            'source' : False,
            'txt-1': False,
            'txt-2': False,
            'source':'http://127.0.0.1:7990/process?msisdn=$msisdn&input=$ussdRequestString&can_renew=0',

        }

L4M1 = {'id':'1-0-4-1','leaf': True,'title':False,'footer':False,'response':False,'service':False,'package':False,'parameter':False,'type':'dynamic','checkpoint':False,'entries':[M1E1]}

level4 = {'id':0,'menus':[L4M1,L4M2,L4M3,L4M4,L4M5,L4M6,L4M7]}
