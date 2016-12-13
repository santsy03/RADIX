#!/usr/bin/env python

def queue_response(resources):
    ''' publishes the response parameters received
    into a queue

    @params: dict with response parameters
    '''
    from modular_tariffs.src.common import verify_params
    from utilities.logging.core import log
    from modular_tariffs.src.responses.consumer.client import ModularResponsesClient
    parameters = resources['parameters']
    verify_params(parameters, 
            ['transactionId','msisdn','statusCode','request_details','renew'])
    try:
        '''queue response'''
        ModularResponsesClient(str(parameters))
    except Exception, err:
        q_error = 'operation: queue_response failed. %s' % (
                str(err))
        log(resources, q_error, error=True)


if __name__ == '__main__':
    pass
