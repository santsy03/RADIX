"""
core data provisioning functions
"""
from mg_data_interface.src.configs.config import MESSAGES as messages
from mg_data_interface.src.configs.config import DA_FACTOR
from mg_data_interface.src.configs.config import VALIDITY as validity
from mg_data_interface.src.configs.config import SUCCESS_HIT, FAIL_HIT
from mg_data_interface.src.configs.config import MAX_PURCHASES_PER_BLOCK 
from mg_data_interface.src.configs.config import BARRED_AFTERNOON_QUOTA 
from mg_data_interface.src.configs.config import BARRED_MORNING_QUOTA 
from mg_data_interface.src.configs.config import TIME_BARRED
from mg_data_interface.src.configs.config import MY_MEG_10

from mg_data_interface.src.lib.database_handler import DataCDR
from mg_data_interface.src.lib.con import generate_connection
from utilities.metrics.core import count
from utilities.sms.core import send_message

from ast import literal_eval
from datetime import datetime, timedelta

import traceback
import json

res = generate_connection()


def execute_provision_response(message, logger):
    '''
    determines if a message is aparty or bparty
    '''
    message = literal_eval(message)
    logger.info(message)
    message = json.loads(message)

    transaction_type = message['transaction_type']

    if transaction_type == 'A':
        return process_self(message, logger)
    else:
        return process_b_party(message, logger)

def process_self(message, logger):
    '''
    processes a self data response

    '''
    msisdn = str(message['msisdn']).strip()
    status = int(str(message['status']).strip())
    package_id = str(message['package_id'])

    body = message
    args = message['args']

    can_renew = int(args['can_renew'])
    is_night = str(args['is_night'])

    logger.info("renew: %s" % str(args['can_renew']))

    db  = DataCDR()
    if int(message['package_id']) != 0:
        if status == 5:
            process_status_five(message, logger)

        elif status == 7:
            db.insert_cdr(message, logger)
            text = messages['insufficient_funds']
            logger.info(text)
            send_message(msisdn, text, logger)
            count(FAIL_HIT % 'self.nofunds')


        elif status == 6:
            db.insert_cdr(message, logger)
            text = messages['conflicting_bundle']
            logger.info(text)
            send_message(msisdn, text, logger)
            count(FAIL_HIT % 'self.conflicting')


        elif status == 9:
            process_status_nine(message, logger)

        else:
            db.insert_cdr(message, logger)
            text = messages['error']
            logger.info(text)
            send_message(msisdn, text, logger)
            count(FAIL_HIT % 'self.nofunds')

    if 'web_id' in args:
        '''
        insert request info into table
        '''
        db.insert_web_response(msisdn, args['web_id'], body, logger)

        
def process_b_party(message, logger):
    '''
    process an a party b party message

    '''
    msisdn = str(message['msisdn']).strip()
    status = int(str(message['status']).strip())
    b_msisdn = str(message['b_msisdn']).strip()
    package_id = str(message['package_id']).strip()
    args = message['args']

    if status == 5:
        process_status_five(message, logger)
    
    elif status == 7:
        db.insert_cdr(message, logger)
        text = messages['insufficient_funds']
        logger.info(text)
        send_message(msisdn, text, logger)
        count(FAIL_HIT % 'self.nofunds')
    
    elif status == 6:
        db.insert_cdr(message, logger)
        text = messages['conflicting_bundle']
        logger.info(text)
        send_message(msisdn, text, logger)
        count(FAIL_HIT % 'self.conflicting')
    
    elif status == 9:
        process_status_nine(message, logger)

    else:
        db.insert_cdr(message, logger)
        text= messages['error']
        logger.info(text)
        send_message(msisdn, text, logger)
        count(FAIL_HIT % 'self.nofunds')



    db = DataCDR()

    if 'web_id' in args:
        '''
        insert request info into table
        '''
        db.insert_web_response(msisdn, args['web_id'], body, logger)




def process_status_nine(message, logger):
    '''
    processes all status nine messages
    '''
    msisdn = str(message['msisdn']).strip()
    status = int(str(message['status']).strip())
    b_msisdn = str(message['b_msisdn']).strip()
    package_id = str(message['package_id']).strip()
    
    block = get_current_time_block(logger)
    if is_time_barred(b_msisdn, logger):
        status = TIME_BARRED
        if msisdn == b_msisdn:

            text = messages['time_barred']
            logger.info(text)
            send_message(msisdn, text, logger)
            '''
            text_two = messages['time_barred_french']
            logger.info(text_two)
            send_message(msisdn, text_two, logger)
            '''
        else:
            text_three = messages['time_barred_bparty']
            logger.info(text_three)
            send_message(msisdn, text_three, logger)

    else:
        if block == 'morning':
            status = BARRED_MORNING_QUOTA
            text = messages['morning_barred']
            logger.info(text)
            send_message(msisdn, text, logger)
            '''
            text_two = messages['morning_barred_french']
            logger.info(text_two)
            send_message(msisdn, text_two, logger)
            '''

        elif block == 'afternoon':
            status = BARRED_AFTERNOON_QUOTA 
            text_three = messages['afternoon_barred']
            logger.info(text_three)
            send_message(msisdn, text_three, logger)
            '''
            text_four = messages['afternoon_barred_french']
            logger.info(text_four)
            send_message(msisdn, text_four, logger)
            '''


    db = DataCDR()
    db.insert_cdr(message, logger, status)
def process_status_five(message, logger):
    '''
    processes status five messages
    '''
    msisdn = str(message['msisdn']).strip()
    status = int(str(message['status']).strip())
    b_msisdn = str(message['b_msisdn']).strip()
    package_id = str(message['package_id']).strip()

    logger.info(message)
    package_name = str(message['name'])
    expiry = str(message['balance']['meg_15']['expiry'])
    balance = str(message['balance']['meg_15']['amount'])
    balance = int(balance)/ DA_FACTOR
    if balance == 0 or balance < 0:
        balance = '1'
    else:
        balance = str(balance)
        
    if status == 5:
        if expiry != 'False':
            date = expiry.split('T')[0].split('-')
            expiry_date = date[2]+'-'+date[1]+'-'+date[0]
            metrics_name = package_name.replace(' ','_')
        else:
            expiry_date = (datetime.now()+timedelta(days=int(validity[package_id]))).replace(hour = 23, minute =59)
            metrics_name = package_name.replace(' ','_')
        

    # first insert CDR
    db = DataCDR()
    db.insert_cdr(message, logger)

    block = get_current_time_block(logger)
    if block != 'undefined':
        db.update_count(message, logger, block)
    else:
        logger.info("succesful purchase for %s happened OUTSIDE defined time block"% (b_msisdn))


    # send messages
    if msisdn == b_msisdn:
        "info: %s's transaction is self. Load correct message"% (msisdn)
        if block == 'morning':
            text = messages['success_15_morn']
            if package_id == MY_MEG_10:
                text = messages['success_mymeg_10_morn']

        elif block == 'afternoon':
            text = messages['success_15_afte']
            if package_id == MY_MEG_10:
                text = messages['success_mymeg_10_afte']

        else:
            text = messages['success_15']
            if package_id == MY_MEG_10:
                text = messages['success_mymeg_10']

        logger.info(text)
        send_message(msisdn, text, logger)

        '''
        #send french message
        text_two = messages['success_15_french']
        logger.info(text_two)
        send_message(msisdn, text_two, logger)
        '''
        try:
            count(SUCCESS_HIT % 'self.'+metrics_name)
        except Exception:
            pass


    else:
        response = messages['subscriber']['success'].safe_substitute(\
                b_msisdn = b_msisdn, data = package_name, days = validity[package_id])
        response_rec = messages['recipient']['success'].safe_substitute(\
                benefactor = msisdn, data = package_name, balance = balance, expiry = expiry_date)

        logger.info(response)
        logger.info(response_rec)
 
        send_message(msisdn, response)
        send_message(b_msisdn, response_rec)

        try:
            count(SUCCESS_HIT % 'b_party.'+metrics_name)
        except Exception:
            pass



def is_time_barred(msisdn, logger):
    """
    checks whether a sub is barred due to the current time
    """
    barred = False

    now = datetime.now()

    if now.hour in range(17, 25):
        info = "current time: %s, my meg 15 not available: msisdn: %s" % (str(now), msisdn)
        logger.info(info)

        barred = True
    elif now.hour in range(0, 8):
        info = "current time: %s, my meg 15 not available: msisdn: %s" % (str(now), msisdn)
        logger.info(info)

        barred = True
    elif now.hour == 12:
        info = "current time: %s, my meg 15 not available: msisdn: %s" % (str(now), msisdn)
        logger.info(info)

        barred = True

    return barred

def is_quota_blocked(msisdn, logger):
    '''
    gets whether thhe number is blocked based on number of purchase per block
    '''
    quota = False
    block = get_current_time_block()
    db = DataCDR()
    conf = db.get_current_status(message, logger)

    if block == 'undefined':
        quota = False
    else:
        if conf:
            count = conf[block]
            if count >= MAX_PURCHASES_PER_BLOCK:
                info = "msisdn: %s purchases: %s block: %s" % (msisdn, str(count), str(block))
                logger.info(info)
                quota = True
            else:
                info = "msisdn: %s purchases: %s block: %s" % (msisdn, str(count), str(block))
                logger.debug(info)
                info = "sub: %s is eligible, purchases: %s block: %s" % (msisdn, str(count), str(block))
                logger.debug(info)
                quota = False
        else:
            info = "subscriber: %s not in MEG_15 db. Hes therefore ELIGIBLE" % (msisdn)
            logger.debug(info)
            quota = False


    return quota


def get_current_time_block(logger):
    '''
    returns whether its morning or afternoon based on time
    '''
    current_block = 'undefined'
    now = datetime.now()

    if now.hour in range(8,12):
        info = "current time: %s" % (str(now))
        logger.info(info)
        current_block = 'morning'
        logger.info(current_block)

    elif now.hour in range(13, 18):
        info = "current time: %s" % (str(now))
        logger.info(info)
        current_block = 'afternoon'
        logger.info(current_block)

    return  current_block

