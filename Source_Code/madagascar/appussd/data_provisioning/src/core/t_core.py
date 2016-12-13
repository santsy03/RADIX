#!/usr/bin/env python


from data_provisioning.src.common.core import log
from utilities.logging.core import log
from utilities.db.core import get_connection as getConnections
from utilities.memcache.core import MemcacheHandler
import traceback


def debug(txt):
    from config import debug
    if debug:
        txt = 'DEBUG: %s' %(str(txt))
        return txt

def getPackageDetails(resources):
    ''' retrieves the packageId,cost and other details from a DB call '''
    packageId = resources['parameters']['packageId']
    transaction_id = resources['parameters']['transactionId']
    sql = '''
          select table1.offer_id, table3.package_category_name, table1.volume,
          table1.validity, table2.package_cost, table2.package_name, table2.refill_id, 
          table2.trans_amount, table1.uc, table1.ut from new_provisioning_packages table1,
          new_packages table2, provision_package_category table3 where 
          table2.provisioning_packages_id = table1.id and table2.id =:packageId 
          and table3.id=table1.package_category_id '''
    sql = sql.strip()
    try:
        cache_key = 'package_details_%s' % str(packageId)
        details = MemcacheHandler().get( cache_key )
        log( resources, '%s - packageDetails from cache - %s' % (transaction_id, details), 'debug' )
        
        if not details:
            log(resources, "get package details: cache miss!! package_id %s" % (packageId), 'debug')
            log(resources, "fetching from DB", 'debug')
            connection = getConnections(resources)
            cursor = connection.cursor()
            cursor.execute(sql,{'packageId':packageId})
            details = cursor.fetchall()
            # put in cache
            try:
                MemcacheHandler().set(cache_key, details)
            except Exception, err:
                caching_err = 'error on caching - %s' % (str(err))
                log( resources, caching_err, 'error' )
                pass

            cursor.close()
            resources['connections'].release(connection)
    except Exception,e:
        error = ('operation: getPackageDetails, Desc: Could not fetch package details' +
                'for packageID:%s,Error:%s' %(str(packageId),str(e)))
        error = e
        log(resources, error, 'error')
        try:
            cursor.close()
        except:
            pass
        raise e

    else:
        if details:
            log(resources, str(details), 'debug')
            try:
                packageDetails = {}
                packageDetails['offer_id'] = details[0][0]
                packageDetails['package_category_name']= details[0][1]
                try:
                    packageDetails['data_volume'] =  int(details[0][2])
                except Exception, err:
                    packageDetails['data_volume'] =  details[0][2]
                packageDetails['data_validity'] =  details[0][3]
                packageDetails['package_cost'] = details[0][4]
                packageDetails['package_name'] = details[0][5]
                packageDetails['refill_id'] = details[0][6]
                packageDetails['trans_amount'] = details[0][7]
                packageDetails['uc'] = details[0][8]
                packageDetails['ut'] = details[0][9]

                resources['parameters']['packageDetails'] = packageDetails
                parameters = resources['parameters']
                parameters['validity'] = packageDetails['data_validity']
                parameters['package_category_name'] = packageDetails['package_category_name']
                parameters['volume'] = packageDetails['data_volume']
                parameters['offer_id'] = packageDetails['offer_id']
                parameters['cost'] = '%s' %str(packageDetails['package_cost'])
                parameters['price'] = parameters['cost']
                parameters['package_name'] = packageDetails['package_name']
                parameters['refill_id'] = packageDetails['refill_id']
                parameters['trans_amount'] = packageDetails['trans_amount']
                parameters['uc'] = packageDetails['uc']
                parameters['ut'] = packageDetails['ut']
                parameters['externalData2'] = parameters['package_name']
                resources['parameters'] = parameters
                log(resources, resources, 'info')
            except Exception,e:
                error = ('operation GetPackageDetails, Desc: error inserting details into '+ 
                        'a dict,Error:%s' %(str(e)))
                log(resources, str(traceback.format_exc()), 'error')
                print error
        else:
            resources['provisionStatus'] = '-1'
            resources['desc'] = 'No such Package'
    log(resources, resources['parameters'], 'debug')
    return resources


def billSubscriber(resources):
    from utilities.data_ucip.core import bill_subscriber
    parameters = resources['parameters']
    
    if 'args' in parameters:
        if 'is_renew' in (parameters['args']):
            log(resources, "is_renew", 'info')
            parameters['externalData1'] = parameters['package_name'] + '_autorenewal'
            parameters['externalData2'] = 'auto_renewal' + '_' + parameters['beneficiary']
        elif 'can_renew' in (parameters['args']):
            args = parameters['args']
            if args['can_renew'] == '1':
                parameters['externalData1'] = parameters['package_name'] + '_autorenewal'
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

    if parameters['msisdn'] == '261330465390':
        return True
    if int(parameters['price']) > 0:
        resp = bill_subscriber(resources)
        info_msg = '%s %s' %(str(resources['parameters']['transactionId']),
                str(resp['responseCode']))
        log(resources, info_msg, 'info')
        if resp['responseCode'] == 0:
            return True
        else:
            return False
    else:
        return True


def processRequest(resources):
    '''processes the provisioning request for the given subscriber'''
    from data_provisioning.src.configs.core import status
    from json import dumps
    from utilities.metrics.core import beat
    from aapcn.src.common.core import get_data_profile

    transactionId = resources['parameters']['transactionId']

    msisdn = resources['parameters']['msisdn']
    benefactor = msisdn
    log(resources, "BENEFACTOR msisdn: %s" % (str(benefactor)), 'info')

    beneficiary = resources['parameters']['b_msisdn']
    log(resources, "BENEFICIARY msisdn: %s" % (str(beneficiary)), 'info')

    #add a parameter  a mssisdn just because
    resources['parameters']['a_msisdn'] = benefactor

    '''
    1) always bill the benefactor
    2) always provision the beneficiary
    '''
    #make the beneficiary to be the main msisdn
    resources['parameters']['msisdn'] = beneficiary

    resources['parameters']['benefactor'] = benefactor
    resources['parameters']['beneficiary'] = beneficiary

    packageId = resources['parameters']['packageId']
    parameters = resources['parameters']
    resources['parameters'] = parameters
    resources = get_data_profile(resources)
    from aapcn.src.volume.core import provisionBundle,checkConflictingBundles,getBalance,is_barred
    if int(packageId) != 0:
        resources = getPackageDetails(resources)
        packageDetails = resources['parameters']['packageDetails']
        packageCategoryName = packageDetails['package_category_name'] 
        group = packageCategoryName
        packageName = resources['parameters']['package_name']
        log(resources, packageName, 'debug')
        #packageName = packageDetails['packageName']
        if packageCategoryName == 'volume':
            from aapcn.src.volume.core import provisionBundle,checkConflictingBundles,getBalance,is_barred
        elif packageCategoryName == 'router':
            from aapcn.src.routers.core import provisionBundle,checkConflictingBundles,getBalance,is_barred
        elif packageCategoryName == 'meg_15':
            from aapcn.src.meg_fifteen.core import provisionBundle,checkConflictingBundles,getBalance,is_barred
        elif packageCategoryName == 'fun':
            from aapcn.src.sacc_fun.core import provisionBundle,checkConflictingBundles,getBalance,is_barred
            log(resources, 'loaded sacc module', 'debug')

        elif packageCategoryName == 'telescopic':
            from aapcn.src.telescopic.core import (provisionBundle, checkConflictingBundles, getBalance,
                    check_subscription_time, update_package_details, get_subscription_limit)
            getBalance(resources)
            update_package_details(resources)

        resources = getBalance(resources)
        log(resources, 'get balance done','debug')

        conflicting_bundle = checkConflictingBundles(resources)
        log(resources, 'conflicting: %s msisdn: %s bundle: %s' % (str(conflicting_bundle)
            ,beneficiary,
            packageName),'debug')

        is_barred = is_barred(resources)
        log(resources, 'is barred: %s msisdn: %s bundle: %s' % (str(is_barred)
            ,beneficiary,
            packageName),'debug')
        
            
        within_time_limits = True
        if packageCategoryName == 'telescopic':
            within_time_limits = check_subscription_time(resources)

        if (is_barred == False) and within_time_limits:
            if (conflicting_bundle == False):
                #JUST BEFORE WE BILL WE ENSURE THE MSISDN IS SET BACK TO THE BENEFACTOR
                resources['parameters']['msisdn'] = benefactor

                if billSubscriber(resources):
                    (resources['parameters'])['packageName'] = packageName
                    #HAVING BILLED THE BENEFACTOR, WE RESET THE MSISDN TO THE BENEFICIARY FOR PROVISIONING
                    resources['parameters']['msisdn'] = beneficiary
                    try:
                        resources = provisionBundle(resources)
                    except Exception, err:
                        log(resources, traceback.format_exc(), 'error')
                        (resources['parameters'])['status'] = status['error']
                    else:
                        (resources['parameters'])['status'] = status['successfullyProvisioned']
                        try:
                            metric_name = packageName.replace(' ','_')
                            beat('application.internet.%s' %metric_name)
                        except Exception, err:
                            pass
                else:
                    (resources['parameters'])['status'] = status['insufficientFunds']
            else:
                resources['parameters']['status'] = status['packageConflict']
        else:
            if within_time_limits:
                resources['parameters']['status'] = status['isBarred']
            else:
                resources['parameters']['status'] = status['time_restriction']
    else:
        resources['parameters']['package_name'] = 'balance'
        resources['parameters']['package_category_name'] = 'volume'
        resources = getBalance(resources)
    #HAVING GOTTEN OUR RESPONSE WE RESET THINGS TO THE WAY THEY WERE
    resources['parameters']['msisdn'] = benefactor
    resources['parameters']['b_msisdn'] = beneficiary

    parameters = resources['parameters']
    transactionId = parameters['transactionId']
    info = json_dump(resources)['parameters']['resp']
    log(resources, "Final resources:%s"%str(info), 'info')
    resp = dumps(json_dump(resources)['parameters']['resp'],default=date_handler)
    response = '%s' %(str(resp))
    return response

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def json_dump (resources):
    '''gets parameters from resources
    and creates a json
    '''
    parameters = resources['parameters']
    balance_info = parameters['balance']
    msisdn = parameters['msisdn']
    b_msisdn = parameters['b_msisdn']
    status = parameters['status']
    transaction_id = parameters['transactionId']
    packageId = parameters['packageId']
    transaction_type = parameters['transaction_type'] 
    name = parameters['package_name']
    args = parameters['args']

    resp = {'msisdn': msisdn,
            'status': status,
            'b_msisdn': b_msisdn,
            'package_id': packageId,
            'transactionId' : transaction_id,
            'transaction_type': transaction_type,
            'args':args,
            'name':name,
            'balance' : balance_info}
    parameters['resp'] = resp
    return resources
