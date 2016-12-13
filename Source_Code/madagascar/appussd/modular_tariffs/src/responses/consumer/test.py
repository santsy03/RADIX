def test_process_provision_response(resources):
    from core import process_provision_response
    process_provision_response(resources)


if __name__ == '__main__':
    from server_modular_responses import setup
    import datetime
    resources = setup('log-test')
    resources['connections'] = resources['db_connection']


    balance_info = {'volume': 638, 'units': 'MB', 'da_id': '8', 'package_name': 'MyMeg 10Test', 'expiry': datetime.datetime(2013, 12, 19, 14, 28, 2, 967827)}

    #balance_info = {'8': {'volume': '638.4828125', 'units': 'MB', 'da_id': '8', 'expiry': datetime.datetime(2013, 12, 19, 12, 0)}, '2': {'volume': '0.0', 'units': 'MB', 'da_id': '2', 'expiry': datetime.datetime(9999, 12, 31, 0, 0)}}

    parameters = {'msisdn': '261336173681',
            'status': '5',
            'b_msisdn': '261336173681',
            'packageId': '4',
            'transactionId' : '2',
            'transaction_type': 'a',
            'args':'/4|14.0|False|8|modular_tariffs',
            'name':'MyMeg 10Test',
            'balance' : balance_info}

    parameters['package_requested'], \
            parameters['modular_id'], \
            parameters['renew'], \
            parameters['da_id'], \
            parameters['channel'] = \
            parameters['args'].split('|')

    parameters['package_requested'] = str(parameters['package_requested']).replace('/','')
    resources['parameters'] = parameters

    test_process_provision_response(resources)
