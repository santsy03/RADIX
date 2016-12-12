"""
common methods to be used through out the app
"""


from urllib import urlopen, urlencode
from datetime import datetime, timedelta
from mg_aapcn_me2u.src.configs.config import URL
from mg_aapcn_me2u.src.configs.config import VOLUME_UC_ID,PARABOLE_UC_ID
from mg_aapcn_me2u.src.configs.config import VOLUME_DA,PARABOLE_DA,PARABOLE_OFFER
from mg_aapcn_me2u.src.configs.config import PRICE
from mg_aapcn_me2u.src.configs.config import DEFAULT_OFFER
from utilities.data_ucip.core import get_balance_and_date
from utilities.data_ucip.core import bill_subscriber2
from utilities.data_ucip.core import set_value_offer_id
from utilities.data_ucip.core import update_da_account
from utilities.data_ucip.core import updateUsageThresholdsAndCounters2

from aapcn.src.common.core import convert_time
from aapcn.src.common.core import sort_expiry

import random
import traceback

class RefillException(Exception):
    """
    Exception raised when a refill 
    fails du to resp code
    """
    def __init__(self, resp_code):
        super(RefillException, self).__init__(resp_code)
        error = 'REFILL FAILED: RESP CODE %s' % resp_code
        self.value = error

    def __str__(self):
        return repr(self.value)


class UpdateUCUTException(Exception):
    """
    Exception raised when an update uc ut
    fails due to resp code
    """
    def __init__(self, resp_code):
        super(UpdateUCUTException, self).__init__(resp_code)
        error = 'UPDATE UC UT FAILED: RESP CODE %s' % resp_code
        self.value = error

    def __str__(self):
        return repr(self.value)

class IncompleteProvisioningException(Exception):
    """
    Exception raised when ANY of the provisioning commands 
    fails due to some other error
    """
    def __init__(self, method_name, trans_id, msisdn):
        super(IncompleteProvisioningException, self).__init__(method_name, trans_id, msisdn)
        error = "%s- error at: %s. PROVISIONING FAILED %s" % (str(trans_id),
                method_name,
                msisdn)
        self.value = error

    def __str__(self):
        return repr(self.value)

class IncompleteBillingException(Exception):
    """
    Exception raised when ANY of the provisioning commands 
    fails due to some other error
    """
    def __init__(self, method_name, trans_id, msisdn):
        super(IncompleteBillingException, self).__init__(method_name, trans_id, msisdn)
        error = "%s- error at: %s. PROVISIONING FAILED %s" % (str(trans_id),
                method_name,
                msisdn)
        self.value = error

    def __str__(self):
        return repr(self.value)



class IncompleteProvisioningInfoException(Exception):
    """
    Exception raised when ANY of the IN commands run 
    before provisioning fail due to any error
    """
    def __init__(self, method_name, trans_id, msisdn):
        super(IncompleteProvisioningInfoException, self).__init__(method_name, trans_id, msisdn)
        error = '%s - error at: %s. CANNOT PROCEED. %s' % (str(trans_id),
                method_name,
                msisdn)
        self.value = error

    def __str__(self):
        return repr(self.value)


def make_request(params, method, logger=None):
    '''
    makes a request to the authenticateion engine
    @params:
        1)params: the parameters encode before making the api call
        2) method: the url to call on the authentication API
        3)logger: the logger object
    '''
    args = urlencode(params)
    try:
        url = URL + method + "?%s" % (str(args))
        if logger:
            logger.debug(url)
        else:
            print url
        resp = urlopen(url)
    except Exception, err:
        if logger:
            logger.error(str(err))
        else:
            print str(err)
    else:
        result = resp.read()
        info = "method: %s params: %s resp: %s" % (method,
                str(params), result)
        if logger:
            logger.debug(info)
        else:
            print info
        return result


def generate_air_tagging_params(resources, trans_type):
    '''
    generates a transaction_id for air transactions
    alongside other parameters required to tag transactions
    on air
    @params:
         1)resources: a dict containing a dict containing air
         tagging params
         2)trans_type: the transaction type
    @return:
        the resources dict with the parameters packed
    '''
    parameters = resources['parameters']
    parameters['externalData1'] = 'me2u'
    parameters['externalData2'] = trans_type
    trans_id = generate_req_id()
    parameters['transactionId'] = trans_id
    resources['parameters'] = parameters
    return resources

def generate_req_id():
    '''
    returns a request id
    '''
    return str(random.randrange(1, 10000000000))


def get_da_balance(resources, da_id, logger):
    '''
    gets the balance as per the given DA ID
    @params:
        1) da id : the da whose details are to be retrieved
        2) resources: a dict containing tagging info and the msisdn
    @return:
        tuple(balance, expiry)
    '''

    parameters = resources['parameters']
    if 'externalData1' not in parameters:
        parameters['externalData1'] = 'get_balance'
    if 'externalData2' not in parameters:
        parameters['externalData2'] = 'get_balance'

    resources['parameters'] = parameters
    msisdn = resources['parameters']['msisdn']
    trans_id = str(resources['parameters']['transactionId'])

    balance = 0
    expiry = None
    try:
        resp = get_balance_and_date(resources)
    except Exception, err:
        error = "op: get_balance: %s" % (str(err))
        logger.error(error)
        logger.error(traceback.format_exc())
        raise IncompleteProvisioningInfoException("get_da_balance", trans_id, msisdn)
    else:
        if resp['responseCode'] == 0:
            ded_info = resp['dedicatedAccountInformation']
            for da in ded_info:
                if da['dedicatedAccountID'] == da_id:
                    balance = da['dedicatedAccountValue1']
                    expiry = convert_time(da['expiryDate'])
            info = "trans_id: %s - da id: %s, balance = %s, msisdn: %s " % (str(trans_id),
                    str(da_id),
                    str(balance),
                    str(msisdn))
            logger.info(info)
    return (balance, expiry)


def bill(msisdn, profile, logger):
    '''
    bills a subscriber
    @params:
        1) msisdn: the sender_msisdn
        2) profile: the senders profile
        3) logger
    @return
        returns a boolean
    '''
    res = {}
    params = {}
    res['parameters'] = params
    tag = 'me2ubill_%s' % (msisdn)
    trans_id = profile[1]
    res = generate_air_tagging_params(res, tag)
    res['parameters']['transactionId'] = trans_id
    res['parameters']['msisdn'] = msisdn
    res['parameters']['price'] = PRICE
    res['logger'] = logger

    try:
        resp = bill_subscriber2(res)
    except Exception, err:
        logger.error(traceback.format_exc())
        error = "BILLING FAILED: trans_id: %s, msisdn: %s, err: %s" %(
                msisdn,
                trans_id,
                str(err))
        logger.error(error)
        return False
    else:
        if resp['responseCode'] == 0:
            return True
        else:
            error = "BILLING FAILED: trans_id: %s, msisdn: %s, RESP: %s" %(
                    msisdn,
                    trans_id,
                    str(resp['responseCode']))
            logger.error(error)
            return False

def update_offers(msisdn, offer_id, trans_id, start, expiry, logger):
    '''
    set an offer withe the parameters supplied
    @params:
        1) msisdn: the msisdn to provision
        2) offer_id: the offer_id to set
        3) expiry: the expiry for the offer id
        4) logger: the logger to log transactions
    @return:
        boolean
    '''
    res = {}
    params = {}
    res['parameters'] = params
    tag = 'me2usetoffer_%s' % (msisdn)
    res = generate_air_tagging_params(res, tag)
    res['parameters']['transactionId'] = trans_id
    res['parameters']['msisdn'] = msisdn
    res['parameters']['end_date'] = expiry
    res['parameters']['offer_id'] = offer_id
    res['parameters']['start_date'] = start
    res['logger'] = logger

    try:
        resp = set_value_offer_id(res)
    except Exception, err:
        logger.error(traceback.format_exc())
        error = "UPDATE OFFERS: trans_id: %s, msisdn: %s, err: %s" %(
                msisdn,
                trans_id,
                str(err))
        logger.error(error)
        return False
    else:
        if resp['responseCode'] == 0:
            return True
        else:
            error = "UPDATE_OFFERS: trans_id: %s, msisdn: %s, RESP: %s" %(
                    msisdn,
                    trans_id,
                    str(resp['responseCode']))
            logger.error(error)
            return False


def update_threshold(msisdn, previous_amount, byte_amount, setting, trans_id, a_profile, logger):
    '''
    set an offer withe the parameters supplied
    @params:
        1) msisdn: the msisdn to provision
        2) offer_id: the offer_id to set
        3) expiry: the expiry for the offer id
        4) logger: the logger to log transactions
    @return:
        boolean
    '''
    res = {}
    params = {}
    res['parameters'] = params
    tag = 'me2uthresholds_%s' % (msisdn)
    res = generate_air_tagging_params(res, tag)
    res['parameters']['transactionId'] = trans_id
    if int(a_profile[0]['sender']['da']) == PARABOLE_DA:
        res['parameters']['uc_id'] = PARABOLE_UC_ID
        res['parameters']['ut_id'] = PARABOLE_UC_ID
    else:
        res['parameters']['uc_id'] = VOLUME_UC_ID
        res['parameters']['ut_id'] = VOLUME_UC_ID
    res['parameters']['msisdn'] = msisdn
    if setting == 'sender':
        amount = int(previous_amount) - int(byte_amount)
    else:
        amount = int(previous_amount) + int(byte_amount)
    res['parameters']['threshold_value'] = amount
    res['logger'] = logger

    try:
        resp = updateUsageThresholdsAndCounters2(res)
    except Exception, err:
        logger.error(traceback.format_exc())
        error = "UPDATE UC_UT: trans_id: %s, msisdn: %s, err: %s" %(
                msisdn,
                trans_id,
                str(err))
        logger.error(error)
        return False
    else:
        if resp['responseCode'] == 0:
            info = "success: UPDATE UC_UT: trans_id: %s, msisdn: %s, RESP: %s" %(
                    msisdn,
                    trans_id,
                    str(resp['responseCode']))
            logger.info(info)
            return True
        else:
            error = " fail: UPDATE UC_UT: trans_id: %s, msisdn: %s, RESP: %s" %(
                    msisdn,
                    trans_id,
                    str(resp['responseCode']))
            logger.error(error)
            return False



def update_da(msisdn, b_msisdn, byte_amount, expiry, setting, trans_id, a_profile, logger):
    '''
    updates the da amount with the expiry passed 
    @params:
        1) msisdn: the msisdn to provision
        2) b_msisdn: the recipient msisdn
        3) byte_amount: the amount to adjust
        4) expiry: the expiry for da
        5) trans_id: the transaction id to use
        5) logger: the logger to log transactions
    @return:
        boolean
    '''
    res = {}
    params = {}
    res['parameters'] = params
    tag = 'me2uda_%s' % (b_msisdn)
    res = generate_air_tagging_params(res, tag)
    res['parameters']['transactionId'] = trans_id
    res['parameters']['msisdn'] = msisdn
    if setting == 'sender':
        res['parameters']['adjustmentAmount'] = '-'+str(byte_amount)
    else:
        res['parameters']['adjustmentAmount'] = str(byte_amount)

    res['parameters']['expiryDate'] = expiry
    res['parameters']['dedicatedAccountId'] = a_profile[0]['sender']['da']
    res['parameters']['daAction'] = 'adjustmentAmountRelative'

    res['logger'] = logger

    try:
        resp = update_da_account(res)
    except Exception, err:
        logger.error(traceback.format_exc())
        error = "UPDATE DA: trans_id: %s, msisdn: %s, err: %s" %(
                msisdn,
                trans_id,
                str(err))
        logger.error(error)
        return False
    else:
        if resp['responseCode'] == 0:
            info = "success: UPDATE DA: trans_id: %s, msisdn: %s, RESP: %s" %(
                    msisdn,
                    trans_id,
                    str(resp['responseCode']))
            logger.info(info)

            return True
        else:
            error = "fail: UPDATE DA: trans_id: %s, msisdn: %s, RESP: %s" %(
                    msisdn,
                    trans_id,
                    str(resp['responseCode']))
            logger.error(error)
            return False




def provision_da_uc(msisdn, b_msisdn, amount, a_profile, b_profile, setting, logger):
    '''
    provisions the da and uc
    @params
        1) msisdn: the msisdn to be provisioned
        2) amount: the amount to set in bytes
        3) previous_amount: the previous uc ut amount
        4) expiry: the expiry to set
        5) trans_id: the trans_id
        6) logger: the logger

    @return
        1) boolean
    '''
    
    # first convert amount to bytes
    byte_amount = int(amount) * (1024*1024)
    trans_id = a_profile[1]
    DA_ID = a_profile[0]['sender']['da']

    if setting == 'sender':
        expiry = a_profile[0][setting]['da_balance'][DA_ID]['expiry']
        previous_amount = a_profile[0][setting]['da_balance'][DA_ID]['value']
    else:
        expiry = get_b_expiry(b_profile, amount, logger)
        previous_amount = b_profile[0][setting]['da_balance'][DA_ID]['value']

    info = "trans_id: %s amount in MB: %s amount in BYTES: %s msisdn: %s" % (
            trans_id,
            str(amount),
            str(byte_amount),
            msisdn)
    logger.info(info)

    try:
        da_res = update_da(msisdn, b_msisdn, byte_amount,
                expiry,
                setting,
                trans_id,
                a_profile,
                logger)
    except Exception, err:
        logger.error(traceback.format_exc())
        raise IncompleteProvisioningException("provision_da_uc",
                trans_id,
                msisdn)
    else:
        if da_res:
            try:
                uc_res = update_threshold(msisdn, previous_amount,
                        byte_amount,
                        setting,
                        trans_id,
                        a_profile,
                        logger)
            except Exception, err:
                logger.error(traceback.format_exc())
                raise IncompleteProvisioningException("provision_da_uc",
                        trans_id,
                        msisdn)
            else:
                if uc_res:
                    if setting != 'sender':
                        info = "trans_id: %s updated  %s 's da and uc with %s bytes" % (
                                str(trans_id),
                                msisdn,
                                str(byte_amount))
                    else:
                        info = "trans_id: %s deducted %s 's da and uc with %s bytes" % (
                                str(trans_id),
                                msisdn,
                                str(byte_amount))
                    logger.info(info)
                    return True
                else:
                    raise IncompleteProvisioningException("provision_da_uc",
                            trans_id,
                            msisdn)
        else:
            raise IncompleteProvisioningException("provision_da_uc",
                    trans_id,
                    msisdn)

def update_b_offers(a_profile, b_profile, amount, logger):
    '''
    determines what offer to provision to the b number
    if neccessary
    @params:
        1) b_profile the recipients profile
        2) amount: the amount being sent
        3) logger: the logger
    @return:
        boolean
    '''
    exp = None
    a_active_offers = a_profile[0]['sender']['active_offers']
    a_expiry = get_highest_expiry(a_active_offers)

    start_date = None
    #offer = get_offer_with_largest_expiry(a_active_offers, a_expiry)

    trans_id = b_profile[1]
    msisdn = b_profile[0]['recipient']['msisdn']
    calc_expiry = get_b_expiry(b_profile, amount, logger)

    if not (has_default_offer(b_profile, logger)):
        start_date = datetime.now()

    exp = calc_expiry
    if int(a_profile[0]['sender']['da']) == PARABOLE_DA:
        offer = PARABOLE_OFFER
    else:
        offer = DEFAULT_OFFER

    return (update_offers(msisdn, offer, trans_id,
            start_date, exp, logger), exp)

def update_parabole_offer(resources, logger):
    '''
    determines what offer to provision to the b number
    if neccessary
    @params:
        1) b_profile the recipients profile
        2) amount: the amount being sent
        3) logger: the logger
    @return:
        boolean
    '''
    exp = None
    a_active_offers = a_profile[0]['sender']['active_offers']
    a_expiry = get_highest_expiry(a_active_offers)

    start_date = None
    #offer = get_offer_with_largest_expiry(a_active_offers, a_expiry)

    trans_id = b_profile[1]
    msisdn = b_profile[0]['recipient']['msisdn']
    calc_expiry = get_b_expiry(b_profile, amount, logger)

    if not (has_default_offer(b_profile, logger)):
        start_date = datetime.now()

    exp = calc_expiry
    if int(a_profile[0]['sender']['da']) == PARABOLE_DA:
        offer = PARABOLE_OFFER
    else:
        offer = DEFAULT_OFFER

    return (update_offers(msisdn, offer, trans_id,
            start_date, exp, logger), exp)

def get_offer_with_largest_expiry(active_offers, largest_expiry):
    '''
    given the dict with active offers
    returns the offer that yielded the largest 
    expiry
    @params:
        1) active_offers: a list of actove offers
        2) largest_expiry: the largest expiry from the active
            offers:
    @return:
        offer_id
    '''
    offer_expiry_dict = {}
    for each in active_offers:
        offer_expiry_dict[each['offer_id']] = each['expiry']

    for key, value in offer_expiry_dict.iteritems():
        if value == largest_expiry:
            offer_id = key
            break

    return offer_id


def has_default_offer(b_profile, logger):
    '''
    Returns True if the sub has the parameter provisioned
    or false if the sub doesnt have it provisioned
    @params
        1) b_profile : the profile for the b number
        2) logger: for logging operations
    @return:
        boolean
    '''
    value = False
    active_offers = b_profile[0]['recipient']['active_offers']
    trans_id = b_profile[0]['recipient']['trans_id']
    msisdn = b_profile[1]

    if len(active_offers) > 0:
        offer_list = []
        for each_offer in active_offers:
            offer = int(each_offer['offer_id'])
            offer_list.append(offer)

        if int(b_profile[0]['recipient']['da']) != PARABOLE_DA:
            if DEFAULT_OFFER in offer_list:
                value = True
                info = "trans_id: %s: msisdn: %s has default offer set: %s" % (
                        str(trans_id),
                        str(msisdn),
                        str(offer_list)
                        )
                logger.debug(info)
        else:
            if PARABOLE_OFFER in offer_list:
                value = True
                info = "trans_id: %s: msisdn: %s has Parabole offer set: %s" % (
                        str(trans_id),
                        str(msisdn),
                        str(offer_list)
                        )
                logger.debug(info)


    return value



def get_highest_expiry(active_offers):
    '''
    gets the offer to provision the recipient with
    default to the offer with the largest expiry
    @params:
        1) active_offers: the list of a subscribers active offers
    @return:
        the offer_id with the largest expiry
    '''
    expiry = None
    if len(active_offers) > 0:

        expiry_list = []
        for each_offer in active_offers:
            curr_exp = each_offer['expiry']
            expiry_list.append(curr_exp)

        new_expiry_list = sort_expiry(expiry_list)
        expiry = new_expiry_list[0]

    return expiry

def get_highest_expiry_offer(active_offers,expiry):
    '''
    gets the offer_id of the longest expiry
    @params:
        1) active_offers: the list of a subscribers active offers
    @return:
        the offer_id with the largest expiry
    '''

    probable_offer_list = []
    for each_offer in active_offers:
        if each_offer['expiry'] == expiry:
            probable_offer_list.append(int(each_offer['offer_id']))
    if PARABOLE_OFFER in probable_offer_list:
        offer = PARABOLE_OFFER
    else:
        offer = probable_offer_list[0]


    return offer

def get_total_usage(usage_list):
    '''
    returns the total usage based on the usage_list
    @params:
        1) usage_list: the uc ut usage_list
    @return:
        total balance
    '''
    total_bal = 0
    if len(usage_list) > 0:
        for each in usage_list:
            for _uc, bal in each.iteritems():
                if int(each['uc_id']) == int(UC_ID):
                    total_bal = each['balance']
    return total_bal


def get_b_expiry(b_profile, amount, logger):
    '''
    generates the expiry as per the 
    business rules
    Rules
    5 MB = 50 Mb : 1 day
    51 MB - 100 mb: 3 days
    101 mb - 500: 7 days
    + 501 Mb : 30 days
    Steps
    1) Get the expiry as per the above rules
    2) Get the current expiry from the b partys profile
    3) compare the two. pick the largest

    @params:
        1) b_profile : the profile of the b number
        2) amount: the amount to be sent in MB
        3) logger: the logger

    @return
        1)expiry: the expiry to provision

    '''
    import calendar
    am_expiry = datetime.now()
    final_expiry = None
    DA_ID = b_profile[0]['recipient']['da']
    p_expiry = b_profile[0]['recipient']['da_balance'][DA_ID]['expiry']
    msisdn = b_profile[0]['recipient']['msisdn']

    trans_id = b_profile[1]
    if int(amount) in range(0, 51):
        am_expiry = (datetime.now()).replace(hour=23, minute=59)
    elif int(amount) in range(51, 101):
        am_expiry = (datetime.now()
                + timedelta(days=2)).replace(hour=23, minute=59)
    elif int(amount) in range(101, 501):
        am_expiry = (datetime.now()
                + timedelta(days=6)).replace(hour=23, minute=59)
    elif int(amount) >= 501:
        am_expiry = (datetime.now()
                + timedelta(days=29)).replace(hour=23, minute=59)

    info = "trans id: %s amount: %s: expiry(based on amount): %s: msisdn: %s" % (
            trans_id, amount, str(am_expiry),
            msisdn)
    logger.info(info)

    final_expiry = am_expiry

    if int(b_profile[0]['recipient']['da']) != PARABOLE_DA:
        if p_expiry:
            if p_expiry.year != 9999:
                if p_expiry > am_expiry:
                    info = "trans_id: %s curr exp: %s is > than calc exp: %s" % (
                            trans_id, str(p_expiry),
                            str(am_expiry))
                    logger.debug(info)
                    final_expiry = p_expiry
                else:
                    info = "trans_id: %s calc exp: %s is > than curr exp: %s" % (
                            trans_id, str(am_expiry), str(p_expiry))
                    logger.debug(info)
                    final_expiry = am_expiry
            else:
                info = "trans_id: %s, %s's expiry is %s:::USING CALC expiry %s" % (trans_id,
                        str(DA_ID),
                        str(p_expiry),
                        str(am_expiry))
                logger.debug(info)
                final_expiry = am_expiry

    else:
        todays_date = datetime.now()
        fin_expiry = (todays_date.replace(day=calendar.monthrange(todays_date.year, todays_date.month)[1]))
        final_expiry = fin_expiry.replace(hour=23, minute=59)

        info = "trans_id: %s, %s's expiry calculated to End of current month as %s" % (trans_id,
                        str(DA_ID),
                        str(final_expiry))
        logger.debug(info)

    return final_expiry


def get_da_id(resources,logger):
    '''
    Determines the DA_ID to use
    '''
    offer_list=[]
    trans_Id = resources['parameters']['transactionId']

    if len(resources['parameters']['active_offers']) > 0:
        offer_list=[]
        for offer in resources['parameters']['active_offers']:
            offer_list.append(int(offer['offer_id']))

        if 1171 in offer_list:
            offer_exp = get_highest_expiry(resources['parameters']['active_offers'])
            offer_id =get_highest_expiry_offer(resources['parameters']['active_offers'],offer_exp)
            if offer_id == PARABOLE_OFFER:
                DA = PARABOLE_DA
            else:
                DA = VOLUME_DA
        else:
            DA = VOLUME_DA
    else:
        DA = VOLUME_DA

    info = "trans_id: %s, DETERMINED DA IS %s" % (str(trans_Id),str(DA))
    logger.debug(info)

    return DA

