'''
module to be loaded by data provisioning for fun /RAITRA bundles 
1) get_balance: Returns the subscriber's current bundle balance
2) provision_bundle: Provisions the actual bundle
3) check_conflicting_bundles: checks if sub has any other conflicting bundle,
   that blocks him/her from purchasing the requested bundle
4) is barred that prevents a sub from getting something cos he is barred
'''

from datetime import datetime, timedelta
from utilities.logging.core import log
from data_provisioning.src.configs.core import status
from aapcn.src.common.core import get_dedicated_account_values, get_dedicated_account_ids
from aapcn.src.common.core import IncompleteProvisioningException 
from aapcn.src.common.core import provision_dedicated_accounts

import time
import random


package_category = 'fun'
package_category_id = 4
action = 'dedicatedAccountValueNew'
renw_prefix = '_autorenewal'

def getBalance(resources):
    '''
    retuns the balance information for the subscriber
    '''
    parameters = resources['parameters']
    package_name = parameters['package_name']
    da_list = get_dedicated_account_ids(resources, package_category_id)
    bundle_balance = get_dedicated_account_values(resources, da_list)
    parameters['da_details'] = {}
    parameters['da_details'][package_category] = bundle_balance['accounts']
    parameters['da_details'][package_category] = bundle_balance['accounts']
    resources['parameters'] = parameters
    return resources


def provisionBundle(resources):
    '''
    provisions the package for the given packageId
    '''

    resources['parameters']['action'] = action
    parameters = resources['parameters']
    validity = parameters['validity']

    validity = validity.split('-')
    validity = int(validity[0])

    if 'args' in parameters:
        if 'is_renew' in (parameters['args']):
            log(resources, "is_renew", 'info')
            parameters['externalData1'] = parameters['package_name'] + renw_prefix
            parameters['externalData2'] = 'auto_renewal' + '_' + parameters['beneficiary']
        elif 'can_renew' in (parameters['args']):
            args = parameters['args']
            if args['can_renew'] == '1':
                parameters['externalData1'] = parameters['package_name'] + renw_prefix
                parameters['externalData2'] = 'auto_renewal' + '_' + parameters['beneficiary']
            else:
                parameters['externalData1'] = parameters['package_name']
                parameters['externalData2'] = 'oneoff' + '_' + parameters['beneficiary']

        elif parameters['transaction_type'] == 'B':
            parameters['externalData1'] = parameters['package_name']
            parameters['externalData2'] = 'oneoff'+ '_'+  parameters['beneficiary']

        else:
            parameters['externalData1'] = parameters['package_name']
            parameters['externalData2'] = 'oneoff' + '_' + parameters['beneficiary']

    log(resources, str(parameters['externalData1']), 'info')
    log(resources, str(parameters['externalData2']), 'info')


    provisioning_expiry = datetime.now().replace(hour=0, minute=0, second =0, microsecond=0)
    provisioning_expiry = provisioning_expiry + timedelta(days = int(validity))

    volume_data = generate_da_volume_data(resources)
    da_details = parameters['da_details']

    log(resources, 'da details: %s MSISDN: %s' % (str(da_details), str(parameters['msisdn'])), 'debug')
    dedicated_accounts = parameters['da_details'][package_category]

    to_provision_das = {}
    balance = {}
    parameters['balance'] = balance
    log(resources, "vol data: %s" % (str(volume_data)), 'debug')
    for da_id, value in volume_data.iteritems():
        if dedicated_accounts.has_key(da_id):
            to_provision_das[da_id] = {}
            to_provision_das[da_id]['value'] = dedicated_accounts[da_id]['value'] + int(volume_data[da_id])
            to_provision_das[da_id]['expiry'] = provisioning_expiry
        else:
            to_provision_das[da_id] = {}
            to_provision_das[da_id]['value'] = int(volume_data[da_id])
            to_provision_das[da_id]['expiry'] = provisioning_expiry

    log(resources, str(to_provision_das), 'debug')
    try:
        resp = provision_dedicated_accounts(resources, to_provision_das, provisioning_expiry)
    except Exception, err:
        log(resources,str(err),'error')
        (resources['parameters'])['status'] = status['error']
    else:
        log(resources, str(resp), 'debug')
        fail = False
        for i in resp:
            if i != 0:
                fail = True
                break
        if fail:
            (resources['parameters'])['status'] = status['error']
            log(resources, "wrong response codes: %s" % str(resp), 'debug')
            raise IncompleteProvisioningException(str(resp))

        else:
            (resources['parameters'])['status'] = status['successfullyProvisioned']
            balance = {}
            balance['expiry'] = provisioning_expiry
            balance['package_name'] = parameters['package_name']
            balance['accounts'] = to_provision_das
            parameters['balance'] = balance 
            parameters['balanceInfo'] = {}
            parameters['balanceInfo'][package_category] = balance
            parameters['expiry'] = provisioning_expiry

    parameters['balance'] = balance
    resources['parameters'] = parameters
    return resources


def checkConflictingBundles(resources):
    ''' 
    checks whether sub is allowed to purchase the requested bundle
    '''

    response = False
    resources['parameters']['conflictingBundles'] = response
    return response


def is_barred(resources):
    '''
    checks whether a subscriber is barred
    '''
    return False

def generate_da_volume_data(resources):
    '''
    generates  a dict eith the da id as key
    and the volume to provision as the value
    '''
    parameters = resources['parameters']
    da_s = str(parameters['offer_id']).strip()
    da_ids = da_s.split('-')
    volume = parameters['volume']
    all_volumes = volume.split('-')

    final_dict = dict(zip(da_ids, all_volumes))
    info = "pack configuration for %s: %s: msisdn %s" %(str(parameters['packageId']),
            str(final_dict),
            str(parameters['msisdn']))
    log(resources, info, 'debug')
    return final_dict




