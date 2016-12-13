def test_process_request(resources):
    from core import process_request
    process_request(resources)


if __name__ == '__main__':
    from server_modular_requests import setup
    resources = setup('log-test')


    parameters = {'msisdn':'261332789512',
            'package_id':'0',
            'action':'balance',
            #'renew':'False',
            'transaction_id':'1',
            'category':'data',
            'transaction_type':'a',
            #'b_msisdn':'261336173681',
            'channel':'modular_tariffs'}
    '''

    parameters = {'msisdn': '261336173681', 'renew': 'False', 'b_msisdn': 'False', 'package_id': '1', 'action': 'provision', 'transaction_type': 'a', 'channel': 'modular_tariffs','transaction_id':'1'}

    '''

    resources['parameters'] = parameters
    resources['msg'] = str(parameters)

    test_process_request(resources)
