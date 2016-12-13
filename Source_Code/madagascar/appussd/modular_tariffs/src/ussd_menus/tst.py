#!/usr/bin/env python2.7
from string import Template
from twisted.internet import defer
from datetime import datetime, timedelta
from modular_tariffs.src.configs import RESPONSES
from utilities.logging.core import log
from modular_tariffs.src.configs.packages import PACKAGES

class menu0():
    def processAction(self,resources):
        resources['currentMenu'] = 'renew'
        return resources



class menuRenewal():
    def __init__(self):
        self.menuTxt = 'Select \n1 for Auto-renewal\n2 for one-time'

    def processAction(self,resources):
        request = (resources['ussdRequestString']).strip()
        if request == '1':
            renew = True
        elif request == '2':
            renew = False

        service_key = str(parameters['service_key']).replace('*', '')
        sequence = parameters['ussdRequestString']
        shortcut = '*%s*%s#' % (service_key, sequence)
        log(resources, shortcut, 'debug')

        resources['shortcut'] = shortcut
        resources['renew'] = renew
        resources['currentMenu'] = 'menuprocess'
        return resources

    def start(self,resources):
        resources['ussdResponseString']= self.menuTxt
        resources['action']='request'
        resources['status'] = '0'
        return resources


class menuProcess():
    def __init__(self):
        pass

    def processAction(self,resources):
        #return resources
        pass

    def start(self,resources):
        from core import validate, enqueue_request
        parameters = resources['parameters']
        language = parameters['language']

        '''
        shortcut   :  the user input from ussd.  i.e.  *XXX*Y#
        source     :  the short code.            i.e.  XXX
        opt        :  the direct dial shortcut.  i.e.  Y

        source = parameters['SERVICE_KEY']
        opt = parameters['SEQUENCE']
        shortcut = *XXX*Y#
        '''

        shortcut = resources['shortcut']
        parameters['renew'] = resources['renew']
        resources['parameters'] = parameters

        try:
            user_input = shortcut.split('*')
            source = user_input[1]
            opt = user_input[2].replace('#','')
            try:
                b_party = user_input[3].replace('#','')
            except IndexError:
                b_party = False
                transaction_type = 'a'
            except Exception, err:
                log(resources, 
                        'menus.start() b_party extraction error: %s' % str(err), 
                        'error')
                raise err
            else:
                transaction_type = 'b'
            
            try:
                package_id = PACKAGES[source][opt]
            except KeyError:
                log(resources, ' package not defined in packages conf', 'error')
            resources['parameters']['b_msisdn'] = b_party
            resources['parameters']['transaction_type'] = transaction_type
            resources['parameters']['package_id'] = str(package_id)
            resources['parameters']['ussd_req'] = [source, opt]
            ussd_req = 'shortcut: %s | source: %s | opt: %s | package: %s' % (
                    shortcut, source, opt, package_id )
            log(resources, ussd_req, 'debug')
        except Exception, err:
            ussd_req_err = 'operation: menus.start() Error: %s' % str(err)
            log(resources, ussd_req_err, 'error')
        msisdn = parameters['msisdn']
        resources['parameters']['shortcut'] = shortcut
        try:
            resources = validate(resources)
        except Exception,e:
            v_error = 'Error: could not process validity of the shortcut, error:%s' %(str(e))
            log(resources, v_error, 'error')
            resources['status'] = '1'  #failure
            menuTxt = RESPONSES['failure'][language]
        else:
            if str(resources['parameters']['validate']) == '1':
                menuTxt = RESPONSES['invalid_code'][language]
                resources['status'] = '2'    #invalid code
                menuTxt = RESPONSES['failure'][language]
            elif str(resources['parameters']['validate']) == '0':
                try:
                    enqueue_request(resources)   # enqueue request
                except Exception,e:
                    error = 'failed to enqueue request for msisdn: %s,shortcut:%s,error:%s' % ( 
                            str(msisdn), str(shortcut), str(e))
                    log(resources, error, 'error')
                    resources['status'] = '1'  #failure
                    menuTxt = RESPONSES['failure'][language]
                else:
                    resources['status'] = '0'  #successful
                    menuTxt = RESPONSES['success'][language]

        resources['ussdResponseString'] = menuTxt
        resources['action']= 'end'
        return resources


menus = {'home':menu0,'renew':menuRenewal,'menuprocess':menuProcess}

if __name__ == '__main__':
    resources = {}
    resources['msisdn'] = '261336173681'
    resources['parameters'] = {'msisdn':'261336173681','package_id':'0','language':'txt-1'}
    resources['shortcut'] = '*177*1#'
    resources['renew'] = False
    #test = menuRenewal()
    test = menuProcess()
    print test.start(resources)
