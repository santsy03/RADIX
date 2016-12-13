import traceback
import cx_Oracle

from datetime import datetime
from urllib import urlencode
from urllib2 import urlopen, Request
from string import Template, upper

from DBUtils.PooledDB import PooledDB

from utilities.logging.core import log
from utilities.secure.core import decrypt
from utilities.sms.core import send_message
from configs.config import databases

from mdg_devices.src.configs.messages import MESSAGE
from mdg_devices.src.configs.status import STATUS
from mdg_devices.src.configs.general import (RANGE, AUTH_KEY
        , ACCOUNT_ID, PROVISION_URL, QUEUES)
from mdg_devices.src.common.retailer import Retailer
from mdg_devices.src.common.whitelists import Whitelist
from mdg_devices.src.common.subscriber import Subscriber

def process_requests(resources):
    resources = unpack_request(resources)
    parameters = resources['parameters']
    message = parameters['message']
    try:
        action = ''
        if 'action' in parameters:
            action = parameters['action']
        msisdn = parameters['msisdn']
        transaction_id = parameters['transaction_id']
        if action == 'retailer':
            resources = process_retailer(resources)
        elif action == 'imei':
            resources = process_imei(resources)
        else:
            resources = process_response(resources)
    except Exception, err:
        error = ("%s, %s operation process_requests "
                "processing %s requests failed: %s") % (str(msisdn), str(transaction_id),
                        str(action), str(err))
        log(resources, error, 'error')
        log(resources, traceback.format_exc(), 'error')
        parameters['status'] = STATUS['tx_error']
    notify(resources)
    update_transaction(resources)
    return resources

def unpack_request(resources):
    '''
    gets the message out of resources
    and makes loads everything into parameters
    '''
    parameters = resources['parameters']
    message = parameters['message']
    action = ''
    for key, value in message.iteritems():
        parameters[key] = value
    if ('args' in parameters) :
        parameters['provisioning_id'] = parameters['transactionId']
        parameters.update(parameters['args'])
    if 'action' in parameters:
        action = parameters['action']
    return resources

def get_status_by_value(num):
    for key, value in STATUS.iteritems():
        if value == num:
            return key

def process_response(resources):
    parameters = resources['parameters']
    status = int(parameters['status'])
    msisdn = parameters['msisdn']
    name = parameters['name']
    con = parameters['connection']
    transaction_id = parameters['transaction_id']
    sub = Subscriber(msisdn, transaction_id)
    parameters['sub'] = sub
    imei = parameters['args']['imei']
    cdr = ("%s %s, %s, %s processing dp response" % (str(transaction_id),
        str(msisdn), str(imei), str(name)))
    log(resources, cdr, 'info')
    if status == 5:
        parameters['status'] = STATUS['tx_success']
        mark_used(resources)
        w_lists = Whitelist('use', imei, con)
        w_lists.run_action()
    else:
        parameters['status'] = STATUS['tx_queued']
    update_transaction(resources)
    return resources

def process_imei(resources):
    '''
    processes the imei
    '''
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    transaction_id = parameters['transaction_id']
    sub = Subscriber(msisdn, transaction_id, None, resources['logger'])
    action = parameters['action']
    con = parameters['connection']
    status = STATUS['tx_queued']
    parameters['status'] = status
    is_pre = is_prepaid(resources)
    created = create_transaction(resources)
    sub.get_imei()
    #imei = sub.imei
    imei = getattr(sub, 'imei', None)
    parameters['sub'] = sub
    if not is_pre:
        status = STATUS['tx_postpaid']
        parameters['status'] = status
        return resources
    if imei:
        cdr = '%s | %s IMEI Found was :%s' % (str(msisdn),
                str(transaction_id), str(imei))
        log(resources, cdr, 'info')
        imei_details = get_imei_details(imei,resources['logger'], con)
        log(resources, "RETURNED IMEI DETAILS::: %s" %str(imei_details))
        if imei_details:
            parameters['imei_details'] = imei_details
            status = imei_details['state']
        else:
            status = STATUS['imei_not_whitelisted']
    else:
        status = STATUS['imei_absent']
    parameters['status'] = status
    resources = provision(resources)
    log(resources, "MY IMEI PROCESSED REQUEST:::: %s" %str(resources))
    return resources

def process_retailer(resources):
    '''
    processes retailer requests
    '''
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    code = parameters['code']
    transaction_id = parameters['transaction_id']
    status = STATUS['tx_error']
    parameters['status'] = status
    created = create_transaction(resources)
    sub = Subscriber(msisdn, transaction_id)
    sub.code = code
    parameters['sub'] = sub
    action = parameters['action']
    claim_details = imei_transaction_details(resources)
    log(resources, claim_details)
    parameters['claim_details'] = claim_details
    if not (retailer_is_whitelisted(resources)):
        status = STATUS['retailer_not_whitelisted']
    elif not claim_details:
        status = STATUS['invalid_id']
    else:
        if not claim_details['state']:
            resources = claim_unique_code(resources)
            status = STATUS['successful_claim']
        else:
            status = STATUS['claimed_unique_code']
    parameters['status'] = status
    update_transaction(resources)
    return resources

def is_prepaid(resources):
    """
    checks if the user has IN profile
    if not, he is considered a postpaid sub
    """
    parameters = resources['parameters']
    parameters['externalData1'] = 'subscriber_type_check'
    parameters['externalData2'] = 'subscriber_type_check'
    return True


def retailer_is_whitelisted(resources):
    '''
    Checks if the retailer is whitelsited
    '''
    exists = False
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    con = parameters['connection']
    w_list = Whitelist('retailer', msisdn, con, resources['logger'])
    w_list.run_action()
    if get_attributes_from_objects('retailer_found', w_list):
        exists = w_list.retailer_found
    return exists

def imei_transaction_details(resources):
    '''
    checks for the imei transaction details
    '''
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    code = parameters['code']
    con = parameters['connection']
    imei_details = False
    try:
        sql = ("select * from whitelist_imei where transaction_id = :code")
        params = {'code': code}
        con_object = con.connection()
        cur = con_object.cursor()
        cur.execute(sql, params)
        ret = cur.fetchall()
        log(resources, ret, 'info')
        cur.close()
        con_object.close()
        for item in ret:
            state = item[8]
            imei = item[0]
            imei_details = {}
            imei_details['state'] = state
            imei_details['transaction_imei']  = imei
        return imei_details
    except Exception, err:
        error = '%s %s could not retrieve details from db error:%s' % (
                str(code),
                str(msisdn),
                str(err))
        log(resources, error, 'error')
        try:
            cur.close()
            con_object.close()
        except:
            pass
    

def claim_unique_code(resources):
    '''
    claims the unique code entered by sub
    '''
    now = datetime.now()
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    con = parameters['connection']
    transaction_id = parameters['transaction_id']
    code = parameters['code']
    transaction_imei = parameters['claim_details']['transaction_imei']
    status = STATUS['claimed_unique_code']
    cdr = ("%s claiming device %s with unique code %s" % (str(msisdn),
        str(transaction_imei), str(code)))
    log(resources, cdr, 'info')
    try:
        sql = ("update whitelist_imei set retailer = :msisdn,claim_status = :status, claimed_at = :now"
                " where imei = :transaction_imei")
        params = {'now': now, 'status':status,
                'msisdn':msisdn,
                'transaction_imei':str(transaction_imei)}
        cur = con.connection().cursor()
        cur.execute(sql, params)
        cur.connection.commit()
        cur.close()
    except Exception, err:
        error = "%s, %s could not claim unique code error: %s" % (
                str(transaction_id), str(msisdn),
                str(err))
        log(resources, error, 'error')
        try:
            cur.close()
        except:
            pass
    return resources


def get_attributes_from_objects(attribute, _object):
    """
    checks if the object has an attribute
    if not returns None
    """
    try:
        assert hasattr(_object, attribute)
        return True
    except:
        pass


def get_imei_details(imei, log, con):
    """
    gets all the imei details
    """
    imei_details = False
    try:
        w_lists = Whitelist('imei', imei, con, log)
        w_lists.run_action()
        if w_lists.cached_imei:
            imei_details = w_lists.cached_imei
    except Exception, err:
        raise err
    return imei_details

def provision(resources):
    parameters = resources['parameters']
    status = int(parameters['status'])
    language = parameters['language']
    sub = parameters['sub']
    if status == 0:
        imei_details = parameters['imei_details']
        imei_range = imei_details['range']
        cdr = ("%s, %s provisioning for imei range %s" % (
            str(sub.msisdn), str(sub.imei), str(imei_range)))
        log(resources, cdr, 'info')
        ## provision here
        ### sends a request to provisioning
        parameters['status'] = STATUS['tx_queued']
        t_id = enqueue_provision_request(imei_range, sub, 
                language, resources['logger'])
        if not t_id:
            parameters['status'] = STATUS['tx_error']
    return resources

def notify(resources):
    '''
    sends sms to sub
    '''
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    sub = parameters['sub']
    transaction_id = parameters['transaction_id']
    language = parameters['language']
    status = int(parameters['status'])
    validity = parameters.get('validity')
    message = None
    pack_name = None
    if 'name' in parameters:
        pack_name = parameters['name']
    imei = getattr(sub, 'imei', None)
    code = getattr(sub, 'code', None)
    if not status == STATUS['tx_queued']:
        message = MESSAGE[get_status_by_value(status)]
        if isinstance(message, dict):
            message = message[language]
        message = Template(message).safe_substitute(imei = imei, 
                code = code, transaction_id = transaction_id
                , pack_name = pack_name, validity = validity)
        cdr = '%s | %s| %s' % (str(transaction_id), str(msisdn),
                str(message))
        log(resources, cdr, 'info')
        send_message(msisdn, message, resources['logger'])


def enqueue_provision_request(package, sub, language, log):
    '''
    enqueues a provisioning request
    '''
    transaction_type = 'A'
    msisdn = sub.msisdn
    try:
        parameters = {}
        args = {}
        parameters['msisdn'] = sub.msisdn
        parameters['b_msisdn'] = sub.msisdn
        packageId = get_package_id(package)
        parameters['packageId'] = packageId
        parameters['authKey'] = AUTH_KEY
        parameters['accountId'] = ACCOUNT_ID
        parameters['transaction_type'] = transaction_type
        parameters['requestId'] = sub.transaction_id 
        args['routing_key'] = QUEUES['routing_key']
        args['imei'] = str(sub.imei)
        args['transaction_id'] = sub.transaction_id
        args['language'] = language
        args['validity'] = get_package_validity(package)
        parameters['args'] = str(args)
            
        params = urlencode(parameters)
        url = PROVISION_URL
        resp = urlopen(Request(url, params))
        cdr = 'IMEI:%s, MSISDN:%s, PACKAGE_ID: %s sent to provisioning' % (
                str(sub.imei),
                sub.msisdn, str(packageId))
        log.info(cdr)

    except Exception, err:
        error = 'operation: n - enqueue request, desc: \
        failed to submit provisioning request %s: %s, error: %s'\
         % (msisdn, package, str(err))
        log.error(error)
        raise err
    else:
        return (resp.info()).get('Transaction-Id')

def get_package_validity(imei_range):
    imei_range = upper(imei_range.strip())
    try:
        return RANGE[imei_range]['validity']
    except:
        pass
def get_package_id(imei_range):
    imei_range = upper(imei_range.strip())
    try:
        return RANGE[imei_range]['package_id']
    except:
        pass

def mark_used(resources):
    '''
    changes the state of an imei to used
    '''
    claim = 0
    status = 1
    now = datetime.now()
    parameters = resources['parameters']
    conn = parameters['connection']
    transaction_id = parameters['transaction_id']
    msisdn = parameters['msisdn']
    imei = parameters['imei'][:14]
    bundle = parameters['name']
    cdr = ("%s %s marking %s as used" % (str(bundle),str(msisdn),
        str(imei)))
    log(resources, cdr, 'info')
    try:
        sql = ("update whitelist_imei set claim_status = :claim, msisdn = :msisdn, bundle = :bundle,"
                " transaction_id = :transaction_id, status = :status, PROVISIONED_AT = :now"
                " where substr(imei,1,14) = :imei")
        params = {'transaction_id': int(transaction_id),
                'msisdn': msisdn,
                'bundle': bundle,
                'imei': str(imei),
                'claim':claim,
                'status': status,
                'now': now}
        log(resources, params, 'info')
        con_object = conn.connection()
        cus = con_object.cursor()
        cus.execute(sql, params)
        log(resources, cus.rowcount, 'info')
        cus.connection.commit()
        cus.close()
        con_object.close()
    except Exception, err:
        error = ("%s, %s operation mark_used failed. Error: %s" % (str(imei),
                str(msisdn), str(err)
                ))
        log(resources, error, 'error')
        try:
            cus.close()
            con_object.close()
        except:
            pass

def create_transaction(resources):
    '''
    records the final state of the transaction
    '''
    imei = ''
    code = ''
    now = datetime.now()
    parameters = resources['parameters']
    conn = parameters['connection']
    transaction_id = parameters['transaction_id']
    msisdn = parameters['msisdn']
    if 'sub' in parameters:
        sub = parameters['sub']
        imei = getattr(sub, 'imei', None)

    if 'imei' in parameters:
        imei = parameters['imei']
    if 'code' in parameters:
        code = parameters['code']
    status = parameters['status']
    try:
        sql = ("insert into device_requests (id, status, imei, created_at, "
                "retailer_code, msisdn) values (:transaction_id, :status,:imei,:now,"
                " :code, :msisdn)")
        params = {'status': status,
                'msisdn': msisdn,
                ''
                'imei': imei,
                'now': now,
                'code' : code,
                'transaction_id' : transaction_id}
        con_object = conn.connection()
        cus = con_object.cursor()
        cus.execute(sql, params)
        cus.connection.commit()
        cus.close()
        con_object.close()
        return True
    except Exception, err:
        error = '%s, %s create_transaction failed.Error: %s' % (
                str(transaction_id), str(msisdn), str(err))
        log(resources, error, 'error')
        try:
            cus.close()
            con_object.close()
        except:
            pass
        return False

def update_transaction(resources):
    '''
    records the final state of the transaction
    '''
    imei = ''
    code = ''
    now = datetime.now()
    parameters = resources['parameters']
    conn = parameters['connection']
    transaction_id = parameters['transaction_id']
    msisdn = parameters['msisdn']
    if 'imei' in parameters:
        imei = parameters['imei']
    if 'code' in parameters:
        code = parameters['code']
    status = parameters['status']
    try:
        sql = ("update device_requests set status= :status, imei = :imei, created_at = :now,"
                " retailer_code = :code where id = :transaction_id")
        params = {'status': status,
                'imei': imei,
                'now': now,
                'code' : code,
                'transaction_id' : transaction_id}
        con_object = conn.connection()
        cus = con_object.cursor()
        cus.execute(sql, params)
        cus.connection.commit()
        cus.close()
        con_object.close()
    except Exception, err:
        error = '%s, %s update_transaction failed.Error: %s' % (
                str(transaction_id), str(msisdn), str(err))
        log(resources, error, 'error')
        try:
            cus.close()
            con_object.close()
        except:
            pass


def setup():
    '''
    setting up db
    '''
    core = databases['core']
    pooled = PooledDB(cx_Oracle,
        maxcached = 5,
        maxconnections = 100,
        user = decrypt(core['username']),
        password = decrypt(core['password']),
        dsn = core['string'],
        threaded = True)
    return pooled
