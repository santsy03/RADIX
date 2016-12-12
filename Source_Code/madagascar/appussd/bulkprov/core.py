import datetime
import random
import traceback
import cx_Oracle
import csv

from urllib import urlencode
from urllib2 import urlopen, Request
from datetime import datetime
from DBUtils.PooledDB import PooledDB
from config import AUTH_KEY, PROVISION_URL, ACCOUNT_ID, ROUTING_KEY
from configs.config import databases
from utilities.secure.core import decrypt


def read_file(filename):
    try:
        f = open(filename, 'rt')
        reader = csv.reader(f)
    except Exception, e:
        error = 'error while reading error: %s' % str(e)
        print error
        logger.error(error)
        raise e
    else:
        return reader


def process_bulk_request(path, filename):
    try:
        full_path = path + filename + ".csv"
        print "full path - {}".format(full_path)
        records = read_file(full_path)
        for record in records:
            msisdn = str(record[0])
            package = str(record[1])
            #can_renew = str(record[2])
            can_renew ='0'
            resp = enqueue_provision_request(package, msisdn, can_renew)
            info = "{}-|-{}".format(msisdn, resp)
            print info

    except Exception, e:
        print traceback.format_exc()



def enqueue_provision_request(package, msisdn, can_renew):
    '''
    enqueues a provisioning request
    '''
    transaction_type = 'A'
    b_msisdn = msisdn
    try:
        parameters = {}
        args = {}
        parameters['msisdn'] = msisdn
        parameters['b_msisdn'] = b_msisdn
        parameters['packageId'] = package
        parameters['authKey'] = AUTH_KEY
        parameters['accountId'] = ACCOUNT_ID
        parameters['transaction_type'] = transaction_type
        parameters['requestId'] = generate_req_id()
        args['routing_key'] = ROUTING_KEY
        args['can_renew'] = can_renew
        parameters['args'] = str(args)
            
        params = urlencode(parameters)
        url = PROVISION_URL
        resp = urlopen(Request(url, params))

    except IOError, err:
        error = 'operation: IO enqueue request, desc: \
        failed to submit provisioning request %s: %s, error:%s'\
         % (msisdn, package, str(err))
        print error
        print traceback.format_exc()
        raise err
                   
    except Exception, err:
        error = 'operation: n - enqueue request, desc: \
        failed to submit provisioning request %s: %s, error: %s'\
         % (msisdn, package, str(err))
        print error
        raise err
    else:
        return (resp.info()).get('Transaction-Id')



def generate_req_id():
    '''
    returns a request id
    '''
    return str(random.randrange(1, 40000000))



def db_setup():
    db = databases['core']
    pooled = PooledDB(cx_Oracle,maxcached = 5, maxconnections=100,\
            user = decrypt(db['username']), password = decrypt(db['password'])\
            ,dsn = db['string'], threaded = True)
    conn = pooled.connection()
    return conn


if __name__ == '__main__':
    package = '59'
    can_renew = '0'
    msisdn = '261330465390'
    #print get_sub_language(msisdn)
    print enqueue_provision_request(package, msisdn, can_renew)
