"""
module that contains all the validation functions required 
before ME2U provisioning happens
"""
from mg_aapcn_me2u.src.configs.config import C_CODE as country_code
from mg_aapcn_me2u.src.configs.config import PRICE
from mg_aapcn_me2u.src.configs.config import MAX_TRANSACTIONS
from mg_aapcn_me2u.src.configs.config import PARABOLE_DA
from mg_aapcn_me2u.src.configs.config import ALLOWED_BUNDLES
from mg_aapcn_me2u.src.configs.config import MIN_AMOUNT,PARABOLE_AMOUNT
from mg_aapcn_me2u.src.lib.common import make_request
from mg_aapcn_me2u.src.lib.common import get_highest_expiry

from mg_aapcn_me2u.src.lib.database_handler import ME2UDb 
from mg_aapcn_me2u.src.lib.common import generate_air_tagging_params
from utilities.data_ucip.core import get_balance_and_date

from datetime import datetime, timedelta

def pin_is_valid(pin):
    '''
    checks:
    1) the length of the pin
    2) that the pin is 4
    @params:
        1) pin: the pin entered
    @return
        boolean
    '''
    validation = False
    if len(pin) == 4 and pin.isdigit():
        validation = True
    else:
        pass
    return validation


def is_whitelisted(msisdn, logger):
    '''
    returns a boolean based on whether
    an msisdn is whitelsited for me2u
    @params:
        msisdn
    @return:
        boolean
    '''
    can_me2u = False
    _db = ME2UDb()
    can_me2u = _db.is_allowed(msisdn, logger)
    return can_me2u

def has_exceeded_max_transactions(msisdn, logger):
    '''
    checks whether a number has exceeded the max
    number of transactions
    @params:
        1)msisdn: the msisdn whose transaction
                count we are checking
        2)logger: the logger
    @return:
        boolean
    '''
    has_exceeded = True
    try:
        _db = ME2UDb()
        res = _db.get_status(msisdn, logger)
    except Exception, err:
        raise err
    else:
        if res:
            logger.debug(res)
            count = int(res['count'])
            if count >= MAX_TRANSACTIONS:
                info = '''sub %s has exceededed transaction 
                limit: COUNT %s''' % (msisdn, str(count))
                logger.info(info)
                has_exceeded = True

            else:
                has_exceeded = False
        else:
            has_exceeded = False

    #return has_exceeded
    #return False for now(business rule not in play)
    has_exceeded = False
    return has_exceeded



def has_entered_default_pin(pin):
    '''
    checks if the user has entered
    the correct default pin
    @params:
        1) pin: the pin entered
    @return:
        boolean
    '''
    if pin == '1234':
        return True
    else:
        return False

def is_authenticated(msisdn, pin, logger):
    '''
    returns the response after calling the
    authentication api
    @params:
        1)msisdn: the authenticating number
        2)pin: the pin entered
        logger. the logger
    @return:
        boolean
    '''
    is_auth = False
    params = {}
    params['username'] = msisdn
    params['password'] = pin
    params['channel'] = "me2u"

    resp = make_request(params, 'authenticate', logger)
    info = "undefined"

    if resp == '0':
        info = "auth passed: msisdn: %s entered correct pin" % (msisdn)
        is_auth = True
    elif resp == '1':
        info = "auth passed: msisdn: %s's first time." % (msisdn)
        if has_entered_default_pin(pin):
            is_auth = True
            del params['password']
            make_request(params, 'create_user', logger)
        else:
            info = "msisdn: %s entered wrong (default) pin" % (msisdn) 
            logger.info(info)
            is_auth = False
            del params['password']
            make_request(params, 'create_user', logger)
    elif resp == '2':
        info = "auth failed: msisdn: %s entered wrong pin" % (msisdn)
    elif resp == "3":
        info = "auth failed: msisdn: %s  AUTH ERROR" % (msisdn)

    logger.debug(info)
    return is_auth


def b_number_is_valid(b_msisdn, logger):
    '''
    checks whether a number is valid
    @params:
        1) b_msisdn: the recipient msisdn
        2) logger: a transaction logger
    @return:
        boolean
    '''
    resources = {}
    parameters = {}
    resources['parameters'] = parameters
    resources = generate_air_tagging_params(resources, "validate_number")
    resources['parameters']['msisdn'] = country_code + b_msisdn[-9:]

    try:
        resp = get_balance_and_date(resources)
    except IOError, err:
        logger.error("msisdn: %s. op|| b_number is valid %s: " %(str(err),
            b_msisdn))
        return False
    except Exception, err:
        logger.error("msisdn: %s. op|| b_number is valid %s " %(str(err),
            b_msisdn))
        return False
    else:
        logger.debug("msisdn: %s. IN resp code %s" % (b_msisdn, 
            str(resp['responseCode'])))
        if resp['responseCode'] == 0:
            return True
        else:
            return False

def can_afford(msisdn, logger):
    '''
    checks whether a number is valid
    @params:
        1) msisdn: the sender msisdn
        2) logger: a transaction logger
    @return:
        boolean
    '''
    resources = {}
    parameters = {}
    resources['parameters'] = parameters
    resources = generate_air_tagging_params(resources, "validate_number")
    resources['parameters']['msisdn'] = country_code + msisdn[-9:]

    try:
        resp = get_balance_and_date(resources)
    except IOError, err:
        logger.error("msisdn: %s. op|| b_number is valid %s: " %(str(err),
            msisdn))
        return False
    except Exception, err:
        logger.error("msisdn: %s. op|| b_number is valid %s " %(str(err),
            msisdn))
        return False
    else:
        logger.debug("msisdn: %s. IN resp code %s" % (str(resp['responseCode']),
            msisdn))
        if resp['responseCode'] == 0:
            if int(int(resp['accountValue1']) /100) >= PRICE:
                logger.info("msisdn: %s can afford: current bal: %s" % (msisdn, 
                    str(resp['accountValue1'])))
                return True
            else:
                return False
        
        else:
            return False

def can_send_bundle(profile, amount, DA_ID, logger):
    '''
    checks whether the sender can send the bundle
    @param:
        1)profile: the sender's current profile
        2)amount: the amount to be sent in MB's
    @return:
        boolean
    '''
    byte_amount = int(amount) * (1024*1024)
    curr_amount = int(profile[0]['sender']['da_balance'][DA_ID]['value'])

    msisdn = profile[0]['sender']['msisdn']
    trans_id = profile[1]

    if curr_amount > byte_amount:
        return True
    else:
        info = '''
        trans_id: %s, curr_amount: %s, amount to transfer: %s
        msisdn: %s amount to transfer is greater cannot proceed
        ''' % (trans_id, str(curr_amount), str(byte_amount),
                msisdn)
        logger.info(info)
        return False
def can_send_bundle_amount_check(profile, amount, logger):
    '''
    checks whether the sender can send the bundle
    @param:
        1)profile: the sender's current profile
        2)amount: the amount to be sent in MB's
    @return:
        boolean
    '''
    byte_amount = int(amount)

    msisdn = profile[0]['sender']['msisdn']
    trans_id = profile[1]

    if int(profile[0]['sender']['da']) == PARABOLE_DA:
        if byte_amount == PARABOLE_AMOUNT:
            return True
        else:
            info = '''
            trans_id: %s, msisdn: %s, amount to transfer: %s
            is NOT allowed for Parabole bundle
            ''' % (trans_id, msisdn, str(byte_amount))
            logger.info(info)
            return False
    else:
        return True


def has_validity_of_more_than_one_day(profile, logger):
    '''
    checks whether has a subscriber has 
    a validity of more than one day
    @params:
        1) profile: the sender
    @return:
        boolean
    '''
    msisdn = profile[0]['sender']['msisdn']
    trans_id = profile[1]

    active_offers = profile[0]['sender']['active_offers']
    if len(active_offers) > 0: 
        tommorrow = datetime.now() + timedelta(days=1)
        largest_expiry = get_highest_expiry(active_offers)
        if largest_expiry > tommorrow:
            return True
        else:
            info = '''
            trans_id: %s: msisdn: %s has a validity of less than a day: 
            expiry: %s cannot proceed''' % (
                    trans_id,
                    msisdn,
                    str(largest_expiry))
            logger.info(info)
            return False
    else:
        info = "trans_id: %s, %s' has no active offers: active_offers %s cannot proceed" % (
                trans_id,
                msisdn,
                str(active_offers))
        logger.info(info)
        return False

def has_allowed_set_of_bundles(a_profile, logger):
    '''
    checks whether a number has any of the bundles 
    with which one can perform a me2u 
    transaction.
    Bundles allowed:
    a) My GiG 1: 1021
    b) My GiG 2: 1022
    c) My GiG 5: 1024
    d) My GiG 10: 1025
    e) My GiG 30: 1026
    @params:
        1) a profile: the benefactors IN profile
        2) looger: a logger to log transactions
    @return
        boolean
    '''

    _ret = False

    active_offers = a_profile[0]['sender']['active_offers']
    msisdn = a_profile[0]['sender']['msisdn']
    trans_id = a_profile[1]
    offer_list = []
    for each_offer in active_offers:
        offer_list.append(int(each_offer['offer_id']))

    res = set(offer_list) & set(ALLOWED_BUNDLES)

    if res:
        info = "trans_id: %s msisdn: %s has an allowed offer: %s" % (
                trans_id, msisdn, str(res))
        logger.info(info)
        _ret = True
    else:
        _ret = False

    return _ret


def is_min_trans_amount(amount, msisdn, logger):
    '''
    checks whether the minimum transaction has been met
    '''
    if int(amount) < MIN_AMOUNT:
        info = "msisdn: %s is trying to send %s which is less than min amount" %(
                msisdn, amount)
        logger.info(info)
        return False
    else:
        return True
        
