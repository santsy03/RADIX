import sys
import time
from common.config import offers
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

def ServerError(msg):
    return render_to_response('500.html', {'msg': msg})

def PageNotFound(msg):
    return render_to_response('404.html')

def get_subtype(msisdn):
    sys.path.append('/appussd')
    from utilities.data_ucip.core import get_balance_and_date
    resources, subdetails = {}, 'Prepaid,0'
    try:
        print "GetSubscriberType: AIRHandler.getBalanceAndDate: %s" %(msisdn)
        resources['parameters'] = {}
        resources['parameters']['msisdn'] = msisdn
        resources['parameters']['transactionId'] = '40400'
        resources['parameters']['externalData1'] = 'CustomerCareGUI'
        resources['parameters']['externalData2'] = 'GUIPromotions'
        response = get_balance_and_date(resources)
        balance = check_balance(resources, response)
        data_balance = process_balance(balance)
        sub_type, ma_balance = 'Postpaid', 0
        if response['responseCode'] == 0:
            sub_type = 'Prepaid'
            ma_balance = str((float(response['accountValue1'])/100))
        subdetails = {'ma_balance': ma_balance, 'sub_type': sub_type,
                      'data_balance': data_balance}
    except Exception, e:
        print 'Failed to get subscriber details for %s: %s' %(msisdn, str(e))
        raise e
    else:
        return subdetails

def process_balance(balances):
    my_offers = balances['offers']
    my_das = balances['balance']
    category = {}
    category[1011] = 'Volume'
    category[1013] = 'Night'
    category[1018] = 'Facebook'
    category[1019] = 'Twitter'
    category[1020] = 'Whatsapp'
    balance = {}
    for offer in my_offers:
        if offer in offers:
            offer_details = offers[offer]
            offer_info = my_offers[offer]
            print offer_details
            da_id = int(offer_details['data'])
            name = offer_details['name']
            price = offer_details['price']
            uc_ut = int(offer_details['uc_ut'])
            volume = my_das[da_id]['value']
            start_date = offer_info['offerStart']
            end_date = offer_info['offerEnd']
            balance[category[uc_ut]] = {'amount': volume,
                                        'name': name,
                                        'price': price,
                                        'expiry': str(end_date),
                                        'purchase_date': str(start_date)}
    return balance

def check_balance(resources, ac_detail):
    '''
    Method to get subscriber balances offer ids then DA values
    '''
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    try:
        balances, category = False, 0
        offer_list = [1011, 1014, 1016, 1018, 1019, 1021, 1022, 1024, 1025,
                      1026, 1030, 1032, 1034, 1035, 1037, 1038, 1040, 1041,
                      1042, 1044, 1045, 1047, 1073, 1074, 1080, 1081, 1082,
                      1083, 1084]
        #range(1011, 1043)
        #offer_list.extend(settings['OFFER_DA'])
        da_list = [1011, 1013, 1014, 1018, 1019, 1020, 1021]
        # To change this
        balances = {'offers': {}, 'balance': {}}
        if ac_detail['responseCode'] == 0:
            sc = ac_detail['serviceClassCurrent']
            balances['sc'] = sc
            if offer_list:
                offers = get_offer_details(resources, ac_detail, offer_list)
                balances['offers'] = offers
            if da_list:
                da_balance = get_da_values(resources, ac_detail, da_list)
                balances['balance'] = da_balance
        else:
            balances['sc'] = 0
    except Exception, e:
        error = '%s:Error balance check - %s' % (msisdn, str(e))
        print error
        raise e
    else:
        return balances


def get_offer_details(resources, acc_info, offer_ids=None):
    '''
    retrieves the subscribers profile using Offer IDs
    '''
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    try:
        cur_offer = {}
        if 'offerInformationList' in acc_info:
            offers = acc_info['offerInformationList']
            for offer in offers:
                if int(offer['offerID']) in offer_ids:
                    if offer['offerType'] == 2:
                        offer_start = convert_time(offer['startDateTime'])
                        offer_end = convert_time(offer['expiryDateTime'])
                    else:
                        offer_start = convert_time(offer['startDate'], 0)
                        offer_end = convert_time(offer['expiryDate'], 0)
                    cur_offer[offer['offerID']] = {'offerStart': offer_start,
                                                   'offerEnd': offer_end,
                                                   'offerID': offer['offerID']}
    except Exception, e:
        error = '%s : Failed getting offer ids - %s' % (msisdn, str(e))
        print error
        raise e
    else:
        return cur_offer


def get_da_values(resources, acc_info, da_list):
    '''
    Get dedicated account values existing in list
    '''
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    try:
        da_balance = {}
        if 'dedicatedAccountInformation' in acc_info:
            dainfo = acc_info['dedicatedAccountInformation']
            i = 0
            for dedicatedAccount in dainfo:
                da_id = dedicatedAccount['dedicatedAccountID']
                if da_id in da_list:
                    da_value = dainfo[i]['dedicatedAccountValue1']
                    da_expiry = dainfo[i]['expiryDate']
                    da_type = dainfo[i]['dedicatedAccountUnitType']
                    da_balance[da_id] = {'value': da_value,
                                         'expiry': da_expiry,
                                         'unit': da_type}
                i += 1
    except Exception, e:
        error = '%s : Failed get DA values - %s' % (msisdn, str(e))
        print error
        raise e
    else:
        return da_balance


def convert_time(air_time, dtype=2):
    '''
    converts air time to datetime object for better comparison
    '''
    try:
        if dtype == 0:
            fmt = '%Y%m%dT%H:%M:%S+0000'
        else:
            fmt = '%Y%m%dT%H:%M:%S+0300'
        time_air = time.mktime(time.strptime(str(air_time), fmt))
        new_time = datetime.fromtimestamp(time_air)
        if dtype == 0:
            new_time = new_time.replace(hour=23, minute=59)
    except Exception, e:
        raise e
    else:
        return new_time
