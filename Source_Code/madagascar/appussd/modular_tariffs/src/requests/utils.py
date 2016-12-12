#!/usr/bin/env python
__author__ = 'andrew_kamau'
__desc__ =   '''handles extra utility operations on bundle requests
                1. manages logic for degressive bundles.
                   - identifies degressive package IDs
                   - keeps track of subscription count for each sub
                   - returns package ID to requests daemon for provisioning

                   * get_package_id() implemented as a decorator - 
                     for purposes of re-usability
                '''

LOC = 'op:modular.requests.utils'

from datetime import datetime
from utilities.logging.core import log
from utilities.db.core import execute_query

from modular_tariffs.src.configs import SQL
from modular_tariffs.src.configs import DEGRESSIVE_PACKAGES
from modular_tariffs.src.common import MissingParameterException

def get_package_id(func):
    '''
    wrapper function - a decorator that adds a key to resources dict

    @params: expects dict with 'package_id' key

    yields dict with 'new_package_id' key
    '''
    def __inner(resources):
        try:
            assert 'package_id' in resources['parameters']
            
            parameters = resources['parameters']
            msisdn = parameters['msisdn']
            package = parameters['package_id']
            if str(package) not in DEGRESSIVE_PACKAGES['list']:
                # package not in list on config
                no_degress = '%r - package %r not in degressive lst' % (
                        msisdn, package)
                log( resources, no_degress, 'debug' )
                resources['parameters']['new_package_id'] = str(package)
                func(resources)
            else:
                frequency = get_frequency(resources)
                cdr = '%r - %r- package %r - freq %r' % (LOC, 
                        msisdn, package, frequency)
                log( resources, cdr, 'info' )
                
                new_package = DEGRESSIVE_PACKAGES[package][int(frequency)]
                resources['parameters']['new_package_id'] = new_package
                func(resources)

        except AssertionError:
            assert_err = '%s - package_id not in params - %s' % (
                    LOC, resources['parameters'] )
            log( resources, assert_err, 'error' )
            raise MissingParameterException('package_id')
        except Exception, err:
            error = '%r - %r - %r - %r' % ( LOC, msisdn, package, err )
            log( resources, error, 'error' )
            raise err

    return __inner


def get_frequency(resources):
    '''
    checks how many times the msisdn has subscribed to supplied package_id
    '''
    try:
        parameters = resources['parameters']
        package_id = parameters['package_id']
        msisdn = parameters['msisdn']
        today_date = datetime.now()
        today = ( today_date.strftime('%d-%b-%y') ).upper()
        args = {'package_id':package_id, 'msisdn':msisdn,
                'status':'5', 'today':today }
        execute_query( resources, SQL['degressive_frequency'], 
                args, db_name='db_connection' )
        count = resources['parameters']['cursor'].fetchall()
        resources['parameters']['cursor'].close()
        log( resources, '%r - %r count from DB - %r' % (
            msisdn, package_id, count), 'debug' )
        return count[0][0]

    except Exception, err:
        fetch_err = '%r - %r.get_frequency - %r' % (msisdn, LOC, err)
        log( resources, fetch_err, 'error' )
        raise err

