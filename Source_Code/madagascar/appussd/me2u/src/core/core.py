from utilities.logging.core import log
from utilities.ucip.core import bill_subscriber
from utilities.ucip.core import get_balance_and_date
from utilities.ucip.core import update_dedicated_account
from utilities.common.core import get_date_from_timestamp
from me2u.src.common import verify_params, convert_da_time
from me2u.src.common import resolve_expiry
from me2u.src.common import send_sms
from me2u.src.common import resolve_da_value
from me2u.src.common import bill
from me2u.src.common import log_transaction
from me2u.src.common import fetch_package_volumes
from me2u.src.config import ALLOWED_PACKAGES
from me2u.src.config import AIR
from me2u.src.config import MINIMUM_MB_ALLOWED
from me2u.src.config import STATUS_CODES
from me2u.src.config import BILL
from datetime import datetime

from utilities.metrics.core import send_metric
from me2u.src.config import METRICS

da_id = AIR['dedicated_account']
ext1 = AIR['externalData1']


def get_sub_balance(resources, party):
    ''' get the data balance of either the sender or recipient

    @params: 
        1. resources: dict with sender and / or recipient msisdn
        2. party:     subscriber <msisdn/recipient>
           NB: party should be a key in resources['parameters'] dict
            
    @return: dict with:
        main account balance
        data balance
        expiry date
    '''
    retval = {}
    units = ' MB'
    parameters = resources['parameters']
    _msisdn = parameters['msisdn']
    parameters['msisdn'] = parameters[party]
    resources['parameters'] = parameters
    try:
        start = datetime.now()
        resp = get_balance_and_date(resources)
        print resp
        mtrcs = {'name_space':METRICS['air_getbalance'],
                'start_time':start}
        send_metric(mtrcs, 'timer')
        del(mtrcs)

        try:
            # pick balance and expiry from data DA Only
            for DA in resp['dedicatedAccountInformation']:
                #if int(DA['dedicatedAccountID']) == 1011:
                if int(DA['dedicatedAccountID']) == int(da_id):
                    resp_data_balance = DA['dedicatedAccountValue1']
                    resp_expiry_date = DA['expiryDate']
                    break
                else:
                    continue
            log( resources, '%s-%s - data bal: %s - exp date: %s' % (
                party, parameters[party], str(resp_data_balance), str(resp_expiry_date)) )
        except Exception, err:
            da_error = 'op:get_sub_balance - failed to get DA value for %s %s - %s' % (
                    party, parameters[party], str(err) )
            log( resources, da_error, 'error' )
            raise err


        resp_ma_balance = resp['accountValue1']
        
        # convert AIR time to datetime
        expiry_date = convert_da_time(resp_expiry_date)
        # convert DA value to corresponding data value
        data_balance = resolve_da_value(resources, resp_data_balance, 'da_to_mb')

        retval['data_balance'] = data_balance
        retval['units'] = units
        retval['expiry_date'] = expiry_date
        retval['main_account'] = resp_ma_balance
    except Exception, err:
        data_error = 'Failed to retrieve data balance for: %s || \
                Error: %s' % (parameters[party], str(err))
        raise err
    resources['parameters']['msisdn'] = _msisdn
    return retval

def get_max_mb_allowed(amount):
    '''
    calculate maximum bundle allowed, given sub's current balance
    '''
    return eval('0.5 * %d' % float(amount))


def validate_request(resources):
    ''' validates the request to assert that it meets
    business requirements before further processing

    Business rules checked:
    0. Sender data balance check
    1. Amount should not be less than minimum allowed
    2. Amount should not be more than half of current balance
    3. Subscriber should have sufficient data balance
    *4. Check that volume corresponds to pre-configured bundle

    * controlled by toggle in config

    @params: resources dict containing:
        msisdn:     sender's number 
        amount:     data volume to be shared
        recipient:  recipient's number 

    @return: tuple with status and status_code.
        status: bool <True/False>
        =========================
        True: transaction meets business rules and can proceed
        False: transaction fails at one of the business rules

        status_code: str
        ================
        a numerical status indicating the reason for status
        1: sender has insufficient data balance 
        2: amount is greater than half of sender's remaining balance
        3: amount is less than the defined minimum
        4: sender has no bundle
        None: error
        5: successfully validated
        8: volume not allowed - as it does not correspond to 
           any pre-configured bundle
    '''
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    recipient = parameters['recipient']
    amount = parameters['amount']
    sender_profile = parameters['sender_profile']
    recipient_profile = parameters['recipient_profile']
    sender_ma_balance = sender_profile['main_account']
    sender_data_balance = sender_profile['data_balance']

    #0. Sender data balance check  #
    try:
        assert str(sender_data_balance) not in ('0', '0.0')
    except AssertionError:
        sender_data_err = 'Validation failed || Sender has no data balance || %s - %s' % (
                msisdn, str(sender_data_balance) )
        log( resources, sender_data_err, 'debug' )
        status = STATUS_CODES['no_bundle']
        return (False, status)

    #1. Amount should not be less than minimum allowed #
    try:
        assert int(amount) >= int(MINIMUM_MB_ALLOWED)
    except AssertionError:
        min_err = 'Validation Failed || Amount %s less than minimum\
                amount %s || msisdn %s || recipient %s' % (
                        amount, str(MINIMUM_MB_ALLOWED), msisdn, recipient)
        log(resources, min_err, 'debug')
        status = STATUS_CODES['amount_min']
        return (False, status)

    #2. Amount should not be more than half of current balance #
    try:
        max_mb_allowed = get_max_mb_allowed(sender_data_balance)
        assert int(amount) <= max_mb_allowed
    except AssertionError:
        max_error = 'Validation Failed || Amount %s greater than max \
                allowed %s || msisdn %s || recipient %s' % (
                        str(amount), str(max_mb_allowed), msisdn, recipient)
        log(resources, max_error, 'debug')
        status = STATUS_CODES['amount_max']
        return (False, status)

    #3. Subscriber should have sufficient data balance #
    try:
        assert int(float(sender_data_balance)) > int(amount)
    except AssertionError:
        bal_error = 'Validation Failed || Amount %s is greater than current balance %s \
                || msisdn %s || recipient %s' % (str(amount), str(sender_data_balance), 
                        msisdn, recipient)
        log(resources, bal_error, 'debug')
        #status = STATUS_CODES['insufficient_data_balance']
        status = STATUS_CODES['amount_max']
        return (False, status)

    #4. Volume to correspond to pre-configured packages #
    if ALLOWED_PACKAGES['toggle'] == 'on':
        '''if toggle is on, volume validation will be executed.
        Else, any volume will be allowed'''
        try:
            resources = fetch_package_volumes(resources)
            parameters = resources['parameters']
            volumes = parameters['allowed_volumes']
            assert str(amount) in volumes
        except AssertionError:
            vol_error = 'Validation failed || Amount %s not in pre-configured packages\
                    || msisdn %s || recipient %s' % (str(amount), msisdn, recipient)
            log(resources, vol_error, 'debug')
            status = STATUS_CODES['volume_not_allowed']
            return (False, status)
        except Exception, err:
            volume_validation_error = 'operation:validate_request. Failed \
                    in volume validation: %s' % (str(err))
            log(resources, volume_validation_error, 'error')
            raise err

    return (True, STATUS_CODES['success'])


def process_sender(resources):
    ''' perform IN operations on sender
    - deducts amount from sender's DA
    @return: True when successful
    '''
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    amount = resolve_da_value(resources, parameters['amount'], 'mb_to_da')
    da_amount = '-%s' % amount
    expiry_date = parameters['sender_profile']['expiry_date']
    sender_details = 'Sender Update DA Details || Amount %s|| DA to update %s || Expiry to set %s' % (str(da_amount), str(da_id),expiry_date)
    
    log(resources,sender_details,'debug')
    try:
        resp = update_dedicated_account(resources, int(da_id), int(da_amount), expiry_date)
        air_resp = resp['responseCode']
    except Exception, err:
        air_error = 'Failed to update DA for sender %s \
                || Error %s || ' % (msisdn, str(err))
        log(resources, air_error, 'error')
        raise err
    else:
        if str(air_resp) == '0':
            return (True, air_resp)
        else:
            return (False, air_resp)

def process_recipient(resources):
    ''' perform IN operations on recipient
    - credits recipient's DA with amount
    @return: True when succesful
    '''
    parameters = resources['parameters']
    recipient = parameters['recipient']
    amount = resolve_da_value(resources, parameters['amount'], 'mb_to_da')

    #--- temp overwrite of msisdn key
    _msisdn = parameters['msisdn'] #persist msisdn in memory
    parameters['msisdn'] = recipient #overwrite msisdn key in parameters
    resources['parameters'] = parameters #bundle parameters into resources
    #---

    sender_expiry_date = parameters['sender_profile']['expiry_date']
    recipient_expiry_date = parameters['recipient_profile']['expiry_date']
    expiry_date = resolve_expiry(resources, sender_expiry_date, recipient_expiry_date)
    try:
        resp = update_dedicated_account(resources, int(da_id), int(amount), expiry_date)
        air_resp = resp['responseCode']
    except Exception, err:
        air_error = 'Failed to update DA for recipient %s \
                || Error %s || ' % (recipient, str(err))
        log(resources, air_error, 'error')
        raise err
    else:
        if str(air_resp) == '0':
            return (True, air_resp)
        else:
            return (False, air_resp)
    finally:
        #-- restore msisdn key in parameters
        resources['parameters']['msisdn'] = _msisdn
        #----

def get_params(resources):
    ''' 
    populate extra parameters
    '''
    parameters = resources['parameters']
    parameters['transactionId'] = '9'
    parameters['externalData1'] = ext1
    parameters['externalData2'] = parameters['amount']
    parameters['action'] = AIR['action']
    resources['parameters'] = parameters
    sender_profile = get_sub_balance(resources, 'msisdn')
    recipient_profile = get_sub_balance(resources, 'recipient')
    parameters['sender_profile'] = sender_profile
    parameters['recipient_profile'] = recipient_profile
    log(resources, 'Sender Profile Before || %s || %s' % ( 
        parameters['msisdn'], sender_profile ) , 'info')
    log(resources, 'Recipient Profile Before || %s || %s' % ( 
        parameters['recipient'], recipient_profile ), 'info')
    if BILL['toggle'] == 'on':
        parameters['price'] = BILL['price']
    resources['parameters'] = parameters
    return resources

def get_profiles(resources):
    '''
    get subscriber details from IN
    '''
    after_sender = get_sub_balance(resources, 'msisdn')
    after_recipient = get_sub_balance(resources, 'recipient')
    parameters = resources['parameters']
    parameters['sender_profile']['after'] = after_sender
    parameters['recipient_profile']['after'] = after_recipient
    s_after = 'Sender Profile After || %s || %s' % (
            parameters['msisdn'], after_sender)
    r_after = 'Recipient Profile After || %s || %s' % (
            parameters['recipient'], after_recipient)
    log(resources, s_after)
    log(resources, r_after)
    resources['parameters'] = parameters


def process_request(resources):
    '''
    wrapper function to perform entire me2u operation
    '''
    params = ['msisdn','recipient','amount']
    verify_params(resources['parameters'], params)
    resources = get_params(resources)
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    recipient = parameters['recipient']
    amount = parameters['amount']
    try:
        validated = validate_request(resources)
        parameters['status_code'] = validated[1]
        if validated[0] == True:
            mtrcs = {'name_space':METRICS['passed_validation']}
            send_metric(mtrcs, 'counter')
            del(mtrcs)
            billed = bill(resources)
            if billed == True:
                bill_summ = 'Billed %s || Amount %s' % (msisdn, BILL['price'])
            elif billed == False:
                '''--- insufficient funds ---'''
                bill_summ = 'Insufficient Funds || %s' % msisdn
                parameters['status_code'] = STATUS_CODES['insufficient_funds']
            log(resources, bill_summ)
            deducted = process_sender(resources)
            if deducted[0] == True:
                provisioned = process_recipient(resources)
                if provisioned[0] == True:
                    '''--- successful provisioning ---'''
                    provisioned_resp = 'Successfully provisioned || Sender %s || \
                            Recipient %s || Amount %s' % (msisdn, recipient, amount)
                    log(resources, provisioned_resp, 'info')
                else:
                    rec_resp = 'Failed to Provision Recipient %s || AIR Resp %s' % (
                            recipient, provisioned[1])
                    log(resources, rec_resp, 'debug')
            else:
                sender_resp = 'Not Provisioned || Updating sender \
                        profile failed: %s || AIR Resp: %s' % (msisdn, deducted[1])
                log(resources, sender_resp, 'debug')
                parameters['status_code'] = STATUS_CODES['error']
        elif validated[0] == False:
            mtrcs = {'name_space':METRICS['failed_validation']}
            send_metric(mtrcs, 'counter')
            parameters['status_code'] = validated[1]

    except Exception, err:
        process_error = 'Failed to provision || Sender %s || Recipient %s \
                || Amount %s' % (msisdn, recipient, amount)
        log(resources, process_error, 'error')
        raise err
    else:
        status = parameters['status_code']
        if status:
            get_profiles(resources)
            log_transaction(resources)
            send_sms(resources, 'msisdn')
            if str(status) == '5':
                send_sms(resources, 'recipient')
            return '%s||%s||%s' % (msisdn, recipient, parameters['status_code'])


if __name__ == '__main__':
    pass
