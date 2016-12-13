"""
module containing library functions to be
used by me2u
"""
from mg_aapcn_me2u.src.lib.database_handler import ME2UDb
from mg_aapcn_me2u.src.lib.validation import pin_is_valid
from mg_aapcn_me2u.src.lib.validation import is_authenticated
from mg_aapcn_me2u.src.lib.validation import has_exceeded_max_transactions
from mg_aapcn_me2u.src.lib.validation import is_whitelisted
from mg_aapcn_me2u.src.lib.validation import b_number_is_valid
from mg_aapcn_me2u.src.lib.validation import can_afford
from mg_aapcn_me2u.src.lib.validation import can_send_bundle,can_send_bundle_amount_check
from mg_aapcn_me2u.src.lib.validation import has_validity_of_more_than_one_day
from mg_aapcn_me2u.src.lib.validation import has_entered_default_pin
from mg_aapcn_me2u.src.lib.validation import has_allowed_set_of_bundles
from mg_aapcn_me2u.src.lib.validation import is_min_trans_amount


from mg_aapcn_me2u.src.lib.common import get_da_balance,get_da_id
from mg_aapcn_me2u.src.lib.common import generate_air_tagging_params
from mg_aapcn_me2u.src.lib.common import bill
from mg_aapcn_me2u.src.lib.common import provision_da_uc
from mg_aapcn_me2u.src.lib.common import IncompleteBillingException
from mg_aapcn_me2u.src.lib.common import update_b_offers
from mg_aapcn_me2u.src.lib.common import make_request


from aapcn.src.common.core import get_usage2, get_offerings2

from mg_aapcn_me2u.src.configs.config import BILLABLE
from mg_aapcn_me2u.src.configs.config import MESSAGES
from mg_aapcn_me2u.src.configs.config import PARABOLE_DA
from mg_aapcn_me2u.src.configs.config import C_CODE as country_code


from mg_aapcn_me2u.src.configs.config import REQUEST_VALIDATE_FAIL 
from mg_aapcn_me2u.src.configs.config import SENDER_VALIDATE_FAIL
from mg_aapcn_me2u.src.configs.config import SENDER_PROV_FAIL
from mg_aapcn_me2u.src.configs.config import RECIPIENT_PROV_FAIL
from mg_aapcn_me2u.src.configs.config import SUCCESS
from mg_aapcn_me2u.src.configs.config import UNDEFINED



from utilities.sms.core import send_message

def get_transaction_id(sender_msisdn, recipient, amount, logger):
    '''
    inserts the initial transaction details into the DB
    @params:
        1)sender msisdn: the guy about to give data
        2)recipient: the guy about to recieve data
        3)amount: the amount the sender intends to give
        4)logger: to log operations
    @return
        transaction_id: to be used in tracking and logging this request
    '''
    _db = ME2UDb()
    trans_id = _db.generate_trans_id(sender_msisdn, 
            recipient, 
            amount, logger)
    return trans_id


def get_profile(msisdn, setting, trans_id, logger, DA=1011):
    '''
    gets the sender profile
    @params:
        recipient:  the number to recieve the bundle
    @return: the profile as a dict
    '''
    res = {}
    params = {}
    res['parameters'] = params
    tag = 'get_profile_%s' % (msisdn)
    res = generate_air_tagging_params(res, tag)

    res['parameters']['transactionId'] = str(trans_id)
    res['parameters']['msisdn'] = msisdn
    res['logger'] = logger


    res = get_usage2(res)

    res = get_offerings2(res)

    if setting in ['sender','sender_after']:
        DA = get_da_id(res,logger)

    DA_ID = DA
    da_balance = get_da_balance(res, DA_ID, logger)


    profile = {}

    profile[setting] = {}
    profile[setting]['msisdn'] = msisdn
    profile[setting]['da'] = DA_ID
    profile[setting]['active_usage'] = res['parameters']['usage_list']
    profile[setting]['depleted_usage'] = res['parameters']['depleted']
    profile[setting]['active_offers'] = res['parameters']['active_offers']
    profile[setting]['inactive_offers'] = res['parameters']['inactive_offers']
    profile[setting]['da_balance'] = {}
    profile[setting]['da_balance'][DA_ID] = {}
    profile[setting]['da_balance'][DA_ID]['value'] = da_balance[0]
    profile[setting]['da_balance'][DA_ID]['expiry'] = da_balance[1]

    profile[setting]['trans_id'] = str(trans_id)

    info = "trans_id: %s: %s 's profile: %s " % (str(trans_id),
            msisdn, str(profile))
    logger.debug(info)

    return (profile, str(trans_id))



def process_sender(sender_msisdn, amount, a_profile, b_profile, setting, logger):
    '''
    deducts data balance and main account balance (if configured) 
    from the sender
    Process:
    1)bill (if billable)
    2)update da (old amount - sent amount)
    3)update uc ut ( with amount used in DA provisioning)

    @params:
        1) msisdn: the sender_msisdn
        2) amount: the amount to be provisioned in MB
        3) profile: the senders profile

    @return:
        boolean 
    '''
    recipient = b_profile[0]['recipient']['msisdn']

    if BILLABLE:
        bill_res = bill(sender_msisdn, a_profile, logger)

        if bill_res:
            res = provision_da_uc(sender_msisdn, recipient, 
                    amount, a_profile, b_profile, setting, logger)
        else:
            raise IncompleteBillingException("process_sender",
                    a_profile['1'],
                    sender_msisdn)
    else:
        res = provision_da_uc(sender_msisdn, recipient, 
                amount, a_profile, b_profile, setting, logger)
    
    return res


def process_recipient(recipient, amount, a_profile, b_profile, setting, logger):
    '''
    deducts data balance and main account balance (if configured) 
    from the sender
    Process:
    1)update da (old amount - sent amount)
    2)update uc ut ( with amount used in DA provisioning)

    @params:
        1) recipient: the recipient_msisdn
        2) amount: the amount to be provisioned in MB
        3) profile: the recipients profile
        4) setting: the recipients setting
        6) logger: the logger to be used

    @return:
        boolean 
    '''
    res = provision_da_uc(recipient, recipient,
            amount, a_profile, b_profile, setting, logger)
    return res


def validate_provisioning_request(sender_msisdn, recipient, amount, pin, lang, logger):
    '''
    validates that the:
    1) sender number is whitelisted and can do me2u transactions
    2) recipient number is a valid msisdn
    3) sender hasnt exceeded maximum transactions allowed
    4) sender can afford to pay for the transaction
    5) that the pin entered is the correct pin

    @params:
        1) sender_msisdn: the number sending the data
        2) recipient: the number to recieve the data
        3) amount: the amount to be sent in MB
        4) pin: the pin the user entered, if any
        5) logger: to log transactions

    @return
        booelean
    '''
    validation = False
    '''
    if not is_whitelisted(sender_msisdn, logger):
        message = MESSAGES[lang]['not_whitelisted']
        logger.info("not whitelisted: %s" % (sender_msisdn))

        send_message(sender_msisdn, message, logger)
        return validation
    '''
    if not b_number_is_valid(recipient, logger):
        message = MESSAGES[lang]['invalid_bnumber']
        logger.info("invalid b number:%s  a number: %s" % (
            sender_msisdn,
            recipient))
        send_message(sender_msisdn, message, logger)
        return validation
    elif has_exceeded_max_transactions(sender_msisdn, logger):
        message = MESSAGES[lang]['has_exceeded']
        logger.info("max transactions exceeded: %s" % (sender_msisdn))

        send_message(sender_msisdn, message, logger)
        return validation
    elif not pin_is_valid(pin):
        message = MESSAGES[lang]['pin_invalid']
        logger.info("invalid_pin: %s" % (sender_msisdn))

        send_message(sender_msisdn, message, logger)
        return validation
    elif not is_authenticated(sender_msisdn, pin, logger):
        message = MESSAGES[lang]['auth_fail']
        logger.info("wrong pin: %s" % (sender_msisdn))

        send_message(sender_msisdn, message, logger)
        return validation
    elif not can_afford(sender_msisdn, logger):
        message = MESSAGES[lang]['no_funds']
        logger.info("cant afford: %s" % (sender_msisdn))

        send_message(sender_msisdn, message, logger)
        return validation

    elif not is_min_trans_amount(amount, sender_msisdn, logger):
        message = MESSAGES[lang]['below_min']
        logger.info("below min amount: %s" % (sender_msisdn))
        
        send_message(sender_msisdn, message, logger)
        return validation
    else: 
        validation = True
        return validation

def validate_sender_profile(profile, sender_msisdn, amount, lang, logger):
    '''
    validates that the:
    1) sender number has enough to send
    2) that the sender number a valdity of
    more than one day
    @params:
        1) profile: the senders profile
        2) amount: the amount to be sent
    @return:
        boolean
    '''
    validation = False
    if not can_send_bundle(profile, amount, profile[0]['sender']['da'], logger):
        message = MESSAGES[lang]['no_balance']
        logger.info("inadequate balance: %s" % (sender_msisdn))

        send_message(sender_msisdn, message, logger)
        return validation

    elif not can_send_bundle_amount_check(profile, amount, logger):
        message = MESSAGES[lang]['request_not_allowed']
        logger.info("Request is NOT allowed %s" % (sender_msisdn))

        send_message(sender_msisdn, message, logger)
        return validation

    elif not has_validity_of_more_than_one_day(profile, logger):
        message = MESSAGES[lang]['inadequate_validity']
        logger.info("inadequate validty %s" % (sender_msisdn))

        send_message(sender_msisdn, message, logger)
        return validation

    elif not has_allowed_set_of_bundles(profile, logger):
         message = MESSAGES[lang]['no_balance']
         logger.info("no offer: %s" % (sender_msisdn))

         send_message(sender_msisdn, message, logger)
         return validation
    else:
        validation = True

    return validation


def process_provision_request(sender_msisdn, recipient, amount, pin, lang, logger):
    '''
    processes a request specifically for
    data transfer
    @params:
        1) sender_msisdn: the sender msisdn
        2) recipient: the recipient msisdn
        3) amount: the amount to send
        4) the pin: the pin the user entered
        5) logger: to log transactions

    @return:
        boolean

    
    REQUEST_VALIDATE_FAIL = 1
    SENDER_VALIDATE_FAIL = 2
    SENDER_PROV_FAIL = 3
    RECIPIENT_PROV_FAIL = 4
    SUCCESS = 5

    UNDEFINED = 0
    '''

    status = UNDEFINED
    success = False
    a_profile = None
    b_profile = None

    trans_id = get_transaction_id(sender_msisdn, recipient, amount, logger)

    if validate_provisioning_request(sender_msisdn, recipient, amount, pin, lang, logger):

        a_profile = get_profile(sender_msisdn, 'sender', trans_id, logger)

        #then validate a profile

        if validate_sender_profile(a_profile, sender_msisdn, amount, lang, logger):
            #validation complete
            #now to provision
            #get b_profile
            #country_code + b_msisdn[-9:]
            recipient = country_code + recipient[-9:]
            b_profile = get_profile(recipient, 'recipient', trans_id, logger,a_profile[0]['sender']['da'] )

            if process_sender(sender_msisdn, amount, a_profile, b_profile, 'sender', logger):
                if process_recipient(recipient, amount, a_profile, b_profile, 'recipient', logger):
                    res = update_b_offers(a_profile, b_profile, amount, logger)
                    if res[0]:
                        status = SUCCESS
                        send_success_messages(sender_msisdn,
                                recipient, amount, res[1],
                                lang,a_profile[0]['sender']['da'], logger)
                        get_profiles_after(sender_msisdn, recipient, trans_id, a_profile[0]['sender']['da'], logger)
                        success = True
                    else:
                        send_fail_message(sender_msisdn, lang, logger)

                else:
                    status = RECIPIENT_PROV_FAIL
                    send_fail_message(sender_msisdn, lang, logger)
            else:
                status = SENDER_PROV_FAIL
                send_fail_message(sender_msisdn, lang, logger)
        else:
            # log that validation failed
            status = SENDER_VALIDATE_FAIL
            info = 'trans_id: %s, error processing sender: %s' % (
                    trans_id, sender_msisdn)
            logger.info(info)
    else:
        status = REQUEST_VALIDATE_FAIL
        info = 'trans_id: %s, error validating sender: %s' % (
                trans_id, sender_msisdn)
        logger.info(info)

    log_transaction(a_profile, b_profile, status, amount, trans_id, logger)
    update_tracker(sender_msisdn, status, trans_id, logger)
    return success


def get_profiles_after(sender_msisdn, recipient, trans_id, DA, logger):
    '''
    gets the profiles after provisioning
    @params:
        1) sender_msisdn: the sender msisd
        2) recipient: the recipient msisdn
        3) trans_id: the transaction id
        4) logger: the logger to log transactions

    @return
        NOTHING 

    '''
    info = "profiles AFTER: trans_id: %s, msisdn: %s, recipient: %s" % (
            trans_id, sender_msisdn, recipient)
    logger.info(info)

    get_profile(sender_msisdn, 'sender_after', trans_id, logger)
    get_profile(recipient, 'recipient_after', trans_id, logger, DA)


def send_success_messages(sender_msisdn, recipient, amount, expiry, lang, sender_da, logger):
    '''
    sends the messages showung a successful transaction
    @params:
        1) sender_msisdn: the benefactors msisdn
        2) recipient: the recipient msisdn
        3) amount: the amount sent
        4) expiry: the expiry to provision
        5) lang: the language to use
        6) logger: the logger to use
    @return:
        NOTHING 
    '''
    from time import strftime
    expiry = expiry.strftime('%Y-%m-%d %H:%M')

    if sender_da ==PARABOLE_DA:
        a_message = MESSAGES[lang]['success_sender_parabole']
        b_message = MESSAGES[lang]['success_recipient_parabole']

        a_message = a_message.safe_substitute(recipient=recipient)
        b_message = b_message.safe_substitute(expiry=expiry, sender=sender_msisdn)
    else:
        a_message = MESSAGES[lang]['success_sender']
        b_message = MESSAGES[lang]['success_recipient']

        b_message = b_message.safe_substitute(amount=amount,
                expiry=expiry, sender=sender_msisdn)
        a_message = a_message.safe_substitute(amount=amount,
                expiry=expiry, recipient=recipient)

    send_message(sender_msisdn, a_message, logger)
    send_message(recipient, b_message, logger)


def send_fail_message(sender_msisdn, lang, logger):
    '''
    sends the error message
    @params:
        1) sender_msisdn: the msisdn doing the transaction
        2) lang: the language setting
        3) logger: the transaction logger
    '''

    message = MESSAGES[lang]['error']

    send_message(sender_msisdn, message, logger)

def log_transaction(a_profile, b_profile, status, amount, trans_id, logger):
    '''
    updates the cdr in the DB:
    @params
        1) a_profile: the a profile
        2) b_profile: the b profile
        3) status: the status showing what kind of failure
        4) logger: to log transactions

    @return:
        boolean
    '''
    amount = int(amount) * (1024*1024)
    #DA_ID = a_profile[0]['sender']['da']
    if a_profile:
        DA_ID = a_profile[0]['sender']['da']
        a_amount_before = a_profile[0]['sender']['da_balance'][DA_ID]['value']
        a_amount_after = int(a_amount_before) - amount
    if b_profile:
        DA_ID = a_profile[0]['sender']['da']
        b_amount_before = b_profile[0]['recipient']['da_balance'][DA_ID]['value']
        b_amount_after = int(b_amount_before) + amount

    params = {}
    params['status'] = status
    params['trans_id'] = trans_id
    if status == 1:
        params['bal_before'] = '-'
        params['bal_after'] = '-'
        params['rec_bal_before'] = '-'
        params['rec_bal_after'] = '-'
    elif status == 2:
        params['bal_before'] = a_amount_before
        params['bal_after'] = a_amount_before
        params['rec_bal_before'] = '-'
        params['rec_bal_after'] = '-'
    elif status == 3:
        params['bal_before'] = a_amount_before
        params['bal_after'] = a_amount_before
        params['rec_bal_before'] = b_amount_before
        params['rec_bal_after'] = b_amount_before

    elif status == 4:
        params['bal_before'] = a_amount_before
        params['bal_after'] = a_amount_after
        params['rec_bal_before'] = b_amount_before
        params['rec_bal_after'] = b_amount_before

    elif status == 5:
        params['bal_before'] = a_amount_before
        params['bal_after'] = a_amount_after
        params['rec_bal_before'] = b_amount_before
        params['rec_bal_after'] = b_amount_after

    _db = ME2UDb()
    return _db.update_cdr(params, trans_id, logger)


def update_tracker(sender_msisdn, status, trans_id, logger):
    '''
    updates the me2u tracker
    @params:
        1) sender_msisdn: the number sending the bundles
        2) status: the status of the transaction
        3) the logger to log transactions:
    @return:
        nothing
    '''
    if status != 5:
        dbg = "not updating tracker for msisdn: %s, trans_id: %s" %(
                sender_msisdn, trans_id)
        logger.debug(dbg)
    else:
        _db = ME2UDb()
        is_todays = _db.is_todays_record(sender_msisdn, logger)

        if is_todays:
            _db.update_count(sender_msisdn, logger)
        else:
            _db.rebase_to_today(sender_msisdn, logger)
            _db.update_count(sender_msisdn, logger)


def process_change_password(curr_pin, new_pin, confirm_pin, lang, msisdn):
    '''
    processes a change password request
    first checks length of sent password:
        if new_pin and curr_pin  length ==4:
            proceed
    second checks if new_pin == confirm_pin:
        if true: proceed
        else: send message
    third authenticates:
        if is_authentic:
          change password
          if is good: send success
          else: send fail
        elif is new:
        create user with current password:
        if is good: send message
        else: send message
            
    '''
    params = {}
    params['username'] = msisdn
    params['password'] = curr_pin
    params['channel'] = "me2u"

    if not pin_is_valid(new_pin):
        info = "msisdn: %s new pin in incorrect format" % (
                msisdn)
        print info
        message = MESSAGES[lang]['password_format_failed']
        send_message(msisdn, message)

    elif not pin_is_valid(confirm_pin):
        info = "msisdn: %s confirmation pin in incorrect format" % (
                msisdn)
        print info
        message = MESSAGES[lang]['password_format_failed']
        send_message(msisdn, message)
    elif not(confirm_pin == new_pin):
        info = "confirm pin = %s new pin = %s : msisdn: %s" % (
                confirm_pin,
                new_pin,
                msisdn)
        print info
        message = MESSAGES[lang]['new_passwords_no_match']
        send_message(msisdn, message)
    else:
        resp = make_request(params, 'authenticate')
        if resp == '0':
            info = "auth passed: msisdn: %s entered correct pin" % (msisdn)
            print info
            del params['password']
            params['username'] = msisdn
            params['current_password'] = curr_pin
            params['new_password'] = confirm_pin

            make_request(params, 'change_password')

            message = MESSAGES[lang]['successful_password_change']
            send_message(msisdn, message) 

        elif resp == '1':
            info = "auth passed: msisdn: %s's first time." % (msisdn)
            print info
            if has_entered_default_pin(curr_pin):
                # create user with the pin he entered (first time)

                params['password'] = new_pin
                make_request(params, 'create_user')

                message = MESSAGES[lang]['successful_password_change']
                send_message(msisdn, message)
            else:
                info = "msisdn: %s entered wrong (default) pin" % (msisdn)
                print info
                # create  with default pin

                del params['password']
                make_request(params, 'create_user')
                message = MESSAGES[lang]['wrong_pin_password_change']
                send_message(msisdn, message)

        elif resp == '2':
            info = "auth failed: msisdn: %s entered wrong pin" % (msisdn)
            print info

            message = MESSAGES[lang]['wrong_pin_password_change']
            send_message(msisdn, message)

        elif resp == "3":
            info = "auth failed: msisdn: %s  AUTH ERROR" % (msisdn)
            message = MESSAGES[lang]['error']
