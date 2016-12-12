"""
core data provisioning functions
"""
import time
import cx_Oracle
from DBUtils.PooledDB import PooledDB
from datetime import datetime

from utilities.metrics.core import response_time
from utilities.logging.core import log
from utilities.secure.core import decrypt
from utilities.metrics.core import count
from utilities.sms.core import send_message
from utilities.data_ucip import core as ucip
from configs.config import databases

import config


def setup(resources={}):
    database = databases['core']
    user = decrypt(database['username'])
    password = decrypt(database['password'])
    string = database['string']
    resources['connections'] = PooledDB(cx_Oracle,  maxcached=5,
                                        maxconnections=100, user=user,
                                        password=password,
                                        dsn=string, threaded=True)
    return resources


def generate_air_tagging_params(resources):
    '''
    generates a transaction_id for air transactions
    alongside other parameters required to tag transactions
    on air
    '''
    parameters = resources['parameters']
    parameters['externalData1'] = 'goodmorningmada'
    parameters['externalData2'] = 'goodmorningmada'
    trans_id = str(time.time()).replace('.', '')
    parameters['transactionId'] = trans_id
    resources['parameters'] = parameters
    return resources


def check_language(resources):
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    try:
        sql = ('select language from service_language where '
               'msisdn = :msisdn and id = (select max(id) '
               'from service_language where msisdn =:msisdn)')
        connection = resources['connections'].connection()
        cursor = connection.cursor()
        cursor.execute(sql, {'msisdn': msisdn})
        result = cursor.fetchone()
        print result
        count = cursor.rowcount
        cursor.close()
        connection.close()
        if count != 0:
            language = result[0]
        else:
            language = 'txt-3'
        print '%s|%s' % (msisdn, language)
    except Exception, err:
        error = ('error, failed checking language for:%s '
                 'error: %s' % (msisdn, str(err)))
        print error
        try:
            cursor.close()
            connection.close()
        except Exception, err:
            pass
        return 'txt-3'
    else:
        return language


def check_if_whitelisted(resources):
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    try:
        sql = ('select count(*) from goodmorning_whitelist '
               'where msisdn = :msisdn')
        connection = resources['connections'].connection()
        cursor = connection.cursor()
        cursor.execute(sql, {'msisdn': msisdn})
        result = cursor.fetchone()
        cursor.close()
        connection.close()
    except Exception, err:
        error = ('error, failed checking whitelist for:%s '
                 'error: %s' % (msisdn, str(err)))
        print error
        try:
            cursor.close()
            connection.close()
        except Exception, err:
            pass
        return False
    else:
        if int(result[0]) > 0:
            return True
        else:
            return False


def provision_request(resources):
    '''
    enqueues a provisioning request
    '''
    count(config.HIT)
    resources = generate_air_tagging_params(resources)
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    action = parameters['action']
    try:
        if msisdn not in config.WHITELIST:
            resp = ("Nifarana io promotion io. Manasa anao hampiasa MyMeg15 "
                    "*114*40# @ sarany Ar100 monja ary mahazoa isa 10 @ promo "
                    "fety55. Misaotra tompoko")
            print '%s| %s' % (msisdn, resp)
        else:
            if action == 'activate':
                resp = process_activation(resources)
            else:
                resp = 'invalid request'
        return resp
    except Exception, err:
        error = ('provision_request failed '
                 'for:%s|%s|error:%s' % (msisdn, action, str(err)))
        log(resources, error, 'error')


def get_offer_information(resources):
    '''
    Return current offer in subscriber profile.
    '''
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    offer = False
    response = ucip.get_offers(resources)
    print '%s Get resp_code %s' % (msisdn, str(response['responseCode']))
    if response['responseCode'] == 0:
        if 'offerInformation' in response:
            offers = response['offerInformation']
            log(resources, str(response['offerInformation']), 'info')
            for items in offers:
                offer_id = items['offerID']
                if offer_id == config.OFFER_ID:
                    offer = True
    return offer


def correct_time_of_day():
    '''
    check allowed subscription time
    if allowed returns true else returns false
    '''
    now = datetime.now()
    resp = False
    if now.hour < 7 and now.hour > 0:
        resp = True
        if now.hour == 1 and now.minute < 30:
            resp = False
    return resp


def process_activation(resources):
    '''
    process all activation requests
    '''
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    parameters['offer_id'] = config.OFFER_ID
    try:
        info = '%s-%s' % (msisdn, '')
        lang = check_language(resources)
        if check_if_whitelisted(resources):
            print '%s-%s' % (msisdn, 'Whitelisted')
            if correct_time_of_day():
                print '%s-%s' % (msisdn, 'Correct time of day')
                nw = datetime.now()
                start = nw
                if nw.hour < 5:
                    start = datetime(nw.year, nw.month, nw.day, 05, 59, 59)
                parameters['start_date'] = start
                parameters['end_date'] = datetime(nw.year, nw.month, nw.day, 06, 59, 59)
                cdr = '%s-%s-%s' % (msisdn, str(start), str(parameters['end_date']))
                print cdr
                active = get_offer_information(resources)
                if not active:
                    resp = ucip.set_value_offer_id(resources)
                    info = '%s SET-resp_code:%s' % (msisdn, str(resp['responseCode']))
                    log(resources, info, 'info')
                    if resp['responseCode'] == 0:
                        status = config.STATUS['success']
                        msg = config.MESSAGES['success'][lang]
                    else:
                        status = config.STATUS['error']
                        msg = config.MESSAGES['error']
                else:
                    print '%s-%s' % (msisdn, 'Already subscribed')
                    msg = config.MESSAGES['notallowed'][lang]
                    status = config.STATUS['notallowed']
            else:
                print '%s-%s' % (msisdn, 'Invalid time of day')
                msg = config.MESSAGES['notallowed'][lang]
                status = config.STATUS['notallowed']
        else:
            print '%s-%s' % (msisdn, 'Not whitelisted')
            msg = config.MESSAGES['notallowed'][lang]
            status = config.STATUS['notallowed']
        info = '%s| %s' % (msisdn, msg)
        log(resources, info, 'info')
        send_message(msisdn, msg)
        resources['status'] = status
        try:
            create_cdr(resources)
        except Exception, err:
            print str(err)
            pass
        return msg
    except Exception, err:
        error = ('process_activation, failed for:%s '
                 'error: %s' % (msisdn, str(err)))
        log(resources, error, 'error')
        raise err


def create_cdr(resources):
    '''
    insert cdr records in db
    '''
    parameters = resources['parameters']
    status = resources['status']
    msisdn = parameters['msisdn']
    action = parameters['action']
    start = datetime.now()
    try:
        params = {}
        params['msisdn'] = msisdn
        params['status'] = status
        params['action'] = action
        sql = '''insert into goodmorning_cdrs (id, msisdn, action,
                                               status, created_at)
                 values(gmg_seq.nextval, :msisdn,
                        :action, :status, systimestamp)'''
        connection = resources['connections'].connection()
        cursor = connection.cursor()
        cursor.execute(sql, params)
        cursor.connection.commit()
        cursor.close()
        connection.close()
        response_time(config.TIMER % 'db', start)
    except Exception, e:
        error = ('operation:create_cdr,desc:failed '
                 'for:%s, error: %s' % (msisdn, str(e)))
        log(resources, error, 'error')
        try:
            cursor.close()
        except Exception, e:
            pass
        raise e
    else:
        msg = 'cdr created for: %s' % (msisdn)
        log(resources, msg, 'info')
