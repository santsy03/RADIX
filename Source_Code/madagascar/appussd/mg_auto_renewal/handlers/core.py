from utilities.logging.core import log
from mg_auto_renewal.src.client.client import EventsClient

def event_handler(resources):
    '''
    this will handle the various events sent to
    the autorenewal by the event handlers
    '''
    log(resources, str(resources), 'info')
    parameters = resources['parameters']
    args = str(parameters['args']).strip()

    packageId, frequency, renewal_days = args.split(',')
    parameters['packageId'] = packageId
    parameters['frequency'] = frequency
    parameters['renewal_days'] = renewal_days

    del parameters['args']
    try:
        EventsClient(parameters)
    except Exception, err:
        error = 'operation: autorenewal.event_handler, desc:\
                failed to enque renewal request, error: %s' % str(err)
        log(resources, error, 'error')
        #raise err

if __name__ == '__main__':
    resources = {}
    parameters = {}
    parameters['msisdn'] = '243999964900'
    parameters['service_id'] = '22'
    parameters['event_id'] = '2'
    parameters['args'] = '1,aoc,0,0'
    resources['parameters'] = parameters
    event_handler(resources)


