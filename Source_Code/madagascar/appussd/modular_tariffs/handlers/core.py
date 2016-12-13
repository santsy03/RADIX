from utilities.logging.core import log

from modular_tariffs.src.configs import QUEUES
from modular_tariffs.src.requests.renewals.client import ModularRenewalClient

def event_handler(resources):
    '''
    this will handle the various events sent to
    the modular tariffs middleware by the event handlers
    '''
    parameters = resources['parameters']
    event_id = parameters['event_id']
    msisdn = parameters['msisdn']
    cdr = 'event_id %s request for %s' % (str(event_id), msisdn)
    log(resources, cdr, 'info')
    try:
        #args = '%s,%s,%s,%s,%s' % (str(event_id), str(package_id), str(package_name), str(frequency), str(renewal_days) )
        args = parameters['args'].split(',')

        
        msg = {}
        msg['msisdn'] = msisdn
        msg['args'] = parameters['args'] 
        msg['event_id'] = parameters['event_id']
        msg['execute_at'] = parameters['execute_at']
        msg['package_id'] = args[1]
        msg['package_name'] = args[2]
        msg['frequency'] = args[3]
        msg['renewal_days'] = args[4]

        #msg = {'msisdn':msisdn,'package_requested':'1','transactionId':'2013','statusCode':'5','packageName':'clubsms','expiry':'','transaction_id':'123','transaction_type':'a','b_msisdn':'261336173681'}
        ModularRenewalClient(msg)

        log(resources, 'op:mt.handlers.core.event_handler. Queued %s'%msg, 'debug')

    except Exception, err:
        error = ('operation: modular_tariffs.handlers.core, ') + \
                ('desc: failed to queue for provisioning, error:%s') %str(err)
        log(resources, error, 'error')

if __name__ == '__main__':
    '''main fxn'''
    #package_type, package_id, frequency, renewal_days
    resources = {}
    resources['parameters'] = {}
    resources['parameters']['msisdn'] = '261336173681'
    resources['parameters']['event_id'] = '1'
    resources['parameters']['args'] = '2,5,MyMeg 20,0,0,x'
    event_handler(resources)
