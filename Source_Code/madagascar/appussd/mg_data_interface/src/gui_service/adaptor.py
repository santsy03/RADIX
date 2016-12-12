from twisted.web import server, resource
from twisted.internet import reactor, threads
from mg_data_interface.src.lib.core import enqueue_provision_request
from mg_data_interface.src.configs.config import NIGHT_BUNDLES as night_bundles
from mg_data_interface.src.lib.core import disable_renewal
from mg_data_interface.src.lib.database_handler import DataCDR
from mg_data_interface.src.lib.con import generate_connection

from utilities.secure.core import decrypt
from configs.config import databases

import logging
import random
import traceback
from urllib2 import urlopen
import cx_Oracle
from urllib import urlencode

logging.basicConfig(level=logging.DEBUG)

def get_params(request):
    '''
    retrieves values of HTTP Post or Get variables
    '''
    params = {}
    for key, val in request.args.items():
        params[key] = val[0]
    print "params:",params
    return params

def errorback(x):
    print x

def disable_web_renewal(msisdn):
    '''
    disables renewal
    '''
    resp = disable_renewal(msisdn)
    if resp[0] == 'SUCCESS':
        return str({'status':'10', 'date':resp[1]})
    elif resp[0] == 'NO_RENEWAL':
        return str({'status':'11'})

def is_night_bundle(package_id):
    '''
    returns a booleean depending on whether 
    a package id is true or false
    '''

    if package_id in night_bundles:
        return True
    else:
        return False


def generate_req_id(msisdn):
    '''
        Function that inserts a new request into a db table.
        It returns a transaction Id
        packs the result in resources
    '''
    connection = cx_Oracle.connect(decrypt(databases['core']['username']), 
            decrypt(databases['core']['password']), 
            databases['core']['string'],
            threaded=True)

    cursor = connection.cursor()
    try:
        req_id = int(cursor.callfunc('balance_req_proc',
            cx_Oracle.NUMBER,[
                msisdn,
                str(random.randint(1, 1000000000)),
                'web',
                ]))
        return req_id
    except Exception, err:
        print str(err)
        #log(self.resources, error, 'error')
        raise err


class ProvisionService():
    def render_POST(self, request):
        params = get_params(request)
        package = params['packageId']
        msisdn = params['msisdn']
        req_id = generate_req_id(msisdn)

        is_night = is_night_bundle(package)

        if params['auto_renewal'] == "False":
            print "NO RENEWAL"
            try:
                resp = enqueue_provision_request(package, msisdn, \
                        None, "0", req_id, is_night)
            except Exception, err:
                print "couldnt make web request for %s " % msisdn
                print traceback.format_exc()
            else:
                print "made request for %s " % msisdn
        else:
            print "RENEWAL REQUEST" 
            try:
                resp = enqueue_provision_request(package, msisdn, \
                        None, "1", req_id, is_night)
            except Exception, err:
                print "couldnt make web request for %s " % msisdn
                print traceback.format_exc()
            else:
                print "made request for %s " % msisdn
                print resp
        return str(req_id)


class BalanceService():
    def render_POST(self, request):
        params = get_params(request)
        package = params['packageId']
        msisdn = params['msisdn']
        req_id = generate_req_id(msisdn)

        is_night = is_night_bundle(package)

        try:
            resp = enqueue_provision_request(package, msisdn, \
                    None, "0", req_id, is_night)
        except Exception, err:
            import traceback
            print "couldnt make web request for %s " % msisdn
            print traceback.format_exc()
            raise err
        else:
            print "made request for %s " % msisdn

        return str(req_id)



class StopRenewalService():
    def render_POST(self, request):
        import traceback
        params = get_params(request)
        #req_id = generate_req_id()
        msisdn = params['msisdn']
        resp = ""
        try:
            resp = disable_web_renewal(msisdn)
        except Exception, err:
            print "couldnt make stop  request for %s " % msisdn
            resp = str({'status': '3'})
            print traceback.format_exc()
            raise err
        else:
            print "made request for %s " % msisdn

        return resp



class WebService(resource.Resource):
    def __init__(self):
        resource.Resource.__init__(self)
        #self.request_id = generate_req_id()
    def getChild(self, path, request):

        return self


    def render_GET(self, request):
        return "GETS NOT ALLOWED"

    def render_POST(self, request):
        params = get_params(request)

        if params['action'] == 'submitprovision':
            result = ProvisionService()

        elif params['action'] == 'submitbalance':
            result = BalanceService()

        elif params['action'] == 'stop':
            result = StopRenewalService()

        return result.render_POST(request)



class Factory(resource.Resource):
    def __init__(self):
       resource.Resource.__init__(self)
       self.putChild('process', WebService())

