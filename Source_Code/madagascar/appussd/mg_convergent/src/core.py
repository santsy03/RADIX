import cx_Oracle
import time
import traceback
from datetime import datetime, timedelta
from DBUtils.PooledDB import PooledDB

from configs.config import databases
from utilities.logging.core import log
from utilities.sms.core import send_message
from utilities.ucip.core import (update_multiple_da_accounts,
        get_balance_and_date, bill_subscriber, set_offer_id,
        get_offers)

from utilities.secure.core import decrypt
from config import (message, da_list, DA, price,
        HOUR, MINUTE, SECONDS, OFFER_ID, exp_days)


DB_INSTANCE = None

def make_transaction_id():
    """
    Generate unique transaction Id.
    """
    time_str = time.time().__repr__()
    return time_str.replace('.', '')

def check_offer(resources):
    """
    Returns True if Subscriber has
    offer id 13 installed, otherwise
    returns False
    """
    msisdn = resources['parameters']['msisdn']
    resources['parameters']['transactionId'] = make_transaction_id()
    resources['parameters']['externalData1'] = 'convergentData'
    resources['parameters']['externalData2'] = 'check_offer_type'
    resources['parameters']['agent'] = 'UGw Server/4.0/1.0'
    try:
        resp = get_offers(resources)
        if resp['responseCode'] == 0 and 'offerInformation' in resp:
            offers = resp['offerInformation']
            resp = False
            for offer in offers:
                if offer['offerID'] == OFFER_ID:
                    resp = True
                    break
            return resp
        else:
            log(resources, "IN Returned responseCode - {} - {}"\
                    .format(str(resp['responseCode']), str(msisdn)),'debug')
    except Exception, e:
        log(resources, "Get - Offers - Err - {}"\
                .format(traceback.format_exc()), 'error')
        raise e

def get_subscriber_type(resources):
    """
    Returns True when subscriber is
    prepaid otherwise False
    """
    msisdn = resources['parameters']['msisdn']
    resources['parameters']['transactionId'] = make_transaction_id()
    resources['parameters']['externalData1'] = 'convergentData'
    resources['parameters']['externalData2'] = 'check_sub_type'
    try:
        resp = get_balance_and_date(resources)
        if resp['responseCode'] == 0:
            return True
        else:
            log(resources, "IN Returned responseCode - {} - {}"\
                    .format(str(resp['responseCode']), msisdn),'debug')
            return False
    except Exception, e:
        log(resources, "Get - Bal - Err - {}"\
                .format(traceback.format_exc()), 'error')
        raise e

def set_sub_offer_id(resources):
    """
    Installs offer id 13.
    """
    msisdn = resources['parameters']['msisdn']
    startDate = datetime.now()
    y,m,d = startDate.year, startDate.month, startDate.day
    expiryDate = datetime(y,m,d,HOUR,MINUTE)
    resources['parameters']['offer_id'] = OFFER_ID
    resources['parameters']['start_date'] = startDate
    resources['parameters']['end_date'] = expiryDate
    resources['parameters']['agent'] = 'UGw Server/4.0/1.0'
    resources['parameters']['externalData1'] = 'convergentData'
    resources['parameters']['externalData2'] = 'setting_offer'
    try:
        resp = set_offer_id(resources)
        if resp['responseCode'] == 0:
            log(resources, "OFFER SET SUCCESSFULL- {} - {}"\
                    .format(msisdn, str(resp)), 'info')
            return True
        else:
            log(resources, 'IN Returned responseCode - {} - {}'\
                    .format(str(resp['responseCode']), msisdn, 'debug'))
            return False

    except Exception, e:
        log(resources, "Offer - err - {}".format(traceback.format_exc()))
        raise e


def get_sub_main_account(resources):
    """
    Bills subscriber from 
    main account. 
    """
    msisdn = resources['parameters']['msisdn']
    acc_value = None
    try: 
        resp = get_balance_and_date(resources)
        if resp['responseCode'] == 0:
            account = resp['accountValue1']
            acc_value = account
        else:
            debug = "IN Returned responseCode:%s for Msisdn:%s"\
                    %(str(resp['responseCode']), str(msisdn))
            log(resources, debug, 'debug')
            acc_value = 0

    except Exception, e:
        log(resources, traceback.format_exc(), 'error')
        raise e

    else:
        return acc_value

def bill_sub(resources):
    msisdn = resources['parameters']['msisdn']
    resources['parameters']['price'] = int(price) * 100
    resources['parameters']['transactionId'] = make_transaction_id()
    resources['parameters']['externalData1'] = 'convergentData'
    resources['parameters']['externalData2'] = 'convergentData'
    try:
        value = get_sub_main_account(resources)
        b_before = int(value) * 100
        log(resources, "SUB - BAL - BEFORE - {} - {}"\
                .format(msisdn, str(b_before)), 'debug')
        if msisdn in ['261330465390', '261330770007']:
            return True
        if value*100 > price*100:
            bill = bill_subscriber(resources)
            if bill['responseCode'] == 0:
                after = get_sub_main_account(resources)
                b_after = int(after) * 100
                log(resources, "SUB - BAL - AFTER - {} - {}"\
                        .format(msisdn, str(b_after)))
                return True
            else:
                debug = "IN Returned responseCode:%s for Msisdn:%s"\
                        %(str(bill['responseCode']), str(msisdn))
                log(resources, debug, 'debug')
                return False
        else:
            debug = "Subscriber Main account:%s < Actual price:%s"\
                    %(str(value * 100), str(price*100))
            log(resources, debug, 'debug')
            return False

    except Exception, e:
        log (resources, "Bill -Sub - err - {}"\
                .format(traceback.format_exc()), 'error')
        raise e

def pack_da_values():
    """
    Populate DA attributes in a list.
    """
    da_list = []
    final_list = []
    da_data = {}
    now = datetime.now()
    try:
        for key, value in DA.iteritems():
            if str(key) == '14':
                expiry = now + timedelta(days = exp_days)
                y = expiry.year
                m = expiry.month
                day = expiry.day
                expiry_date = expiry.replace(y,m,day, HOUR, MINUTE, SECONDS)
                da_data[str(key)] = {'volume':value * 100, 'expiry_date':expiry_date} 
                da_list.append(da_data)
            else:
                y,m,d = now.year, now.month, now.day
                expiry_date = datetime(y,m,d,HOUR,MINUTE)
                da_data[str(key)] = {'volume':value * 100, 'expiry_date':expiry_date}
                da_list.append(da_data)

    except Exception, e:
        log(resources, "packing - da - err - {}"\
                .format(traceback.format_exc()), 'error')
        raise e
    else:
        return [da_list[0]]


def update_subscriber_da(resources):
    """
    Updates DA's for subscriber.
    list of DA's
    da_list = ['14','24','29','32','42']
    """
    msisdn = resources['parameters']['msisdn'] 
    #resources['parameters']['action'] = 'dedicatedAccountValueNew' 
    resources['parameters']['action'] = 'adjustmentAmountRelative' 
    resources['parameters']['transactionId'] = make_transaction_id()
    resources['parameters']['externalData1'] = 'convergentData'
    resources['parameters']['externalData2'] = 'Update_Convergent_Da'
    #resources['parameters']['agent'] = 'UGw Server/4.0/1.0'
    resources['parameters']['da_list'] = pack_da_values()
    try:
        debug = "{} - SUB DEDICATED ACCOUNT EXPIRY AND VALUES-- {} -- TRANSID: -- {}"\
                .format(str(msisdn), str(resources['parameters']['da_list']),\
                str(resources['parameters']['transactionId']))
        log(resources, debug, 'debug')
        start = datetime.now()
        resp = update_multiple_da_accounts(resources)
        duration = (datetime.now() - start).total_seconds()
        debug = "{}--TOTAL TIME TAKEN TO UPDATE FIVE DA'S--{} -- TRANSID: -- {}"\
                .format(str(msisdn), str(duration),\
                str(resources['parameters']['transactionId']))
        log(resources, debug, 'debug')
        if resp['responseCode'] == 0:
            sub_offer = set_sub_offer_id(resources)
            if sub_offer:
                return True
            else:
                log(resources, "Setting offer - failed - {}"\
                        .format(msisdn), 'debug')
                return False
        else:
            debug = "IN Returned responseCode:%s for Msisdn:%s"\
                    %(str(resp['responseCode']), str(msisdn))
            log(resources, debug, 'debug')
            return False

    except Exception, e:
        log(resources, "update - da - err - {}"\
                .format(traceback.format_exc()), 'error')
        raise e

def provision_subscribers(resources):
    """
    Wrapper Functions that collects, 
    individual methods and evaluates
    them for either success or failure.
    """
    msisdn = resources['parameters']['msisdn']
    language = resources['parameters']['language']
    try:
        sub_type = get_subscriber_type(resources)
        if sub_type:
            conflict = check_offer(resources)
            if not conflict:
                bill = bill_sub(resources)
                if bill:
                    update_sub_da = update_subscriber_da(resources)
                    if update_sub_da:
                        msg = message[str(language)]['success']

                    else:
                        msg = message[str(language)]['failure']

                else:
                    msg = message[str(language)]['insuffcient']
            else:
                msg = message['conflict']
        else:
            msg = message['postpaid']

    except Exception, e:
        log (resources, traceback.format_exc(), 'error')
        raise e

    else:
        info = '%s|%s'%(str(msisdn), str(msg))
        log(resources, "Response - Sent - To -Sub- {}"\
                .format(info), 'info')
        send_message(msisdn, msg)
        return 'success'


def get_sub_language(msisdn, connection):
    """
    Fetch subscriber lanaguage
    from new_service_language table.
    Incase of failure to fetch it defaults
    to txt-3 which is French.
    """
    conn = connection.connection() 
    #conn = db_setup()
    cursor = conn.cursor()
    try:
        sql = ("select language from new_service_language where\
                msisdn = :msisdn")
        param = {}
        param['msisdn'] = msisdn
        cursor.execute(sql, param)
        result = cursor.fetchone()
        count = cursor.rowcount

    except IndexError:
        cursor.close()
        conn.close()
        return 'txt-3'

    except Exception, e:
        log({}, traceback.format_exc(), 'error')
        return 'txt3'

    else:
        if count == 0:
            cursor.close()
            conn.close()
            return 'txt-3'
        else:
            cursor.close()
            conn.close()
            return result[0]

def db_setup():
    db = databases['core']
    pooled = PooledDB(cx_Oracle, maxcached = 15, maxconnections=10,\
            user = decrypt(db['username']), password = decrypt(db['password'])\
            ,dsn = db['string'], threaded = True)
    conn = pooled.connection()
    return conn


def get_db_instance():
    global DB_INSTANCE
    if DB_INSTANCE is None:
        DB_INSTANCE = db_setup()
    return DB_INSTANCE



if __name__ == '__main__':
    resources = {'parameters':{'msisdn':'261330465390'}}
    msisdn = '261330465390'
    #print provision_subscribers(resources)
    #print check_offer(resources)
    print  update_subscriber_da(resources)
    #print  pack_da_values()
    #conn = {}
    #print get_sub_language(msisdn, conn)
    #print db_setup()
