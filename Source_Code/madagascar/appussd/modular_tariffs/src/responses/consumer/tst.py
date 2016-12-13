def test_process_provision_response(resources):
    from core import process_provision_response
    process_provision_response(resources)


if __name__ == '__main__':
    from server_modular_responses import setup
    import datetime
    resources = setup('log-test')
    resources['connections'] = resources['db_connection']


    #balance_info = {'volume': 638, 'units': 'MB', 'da_id': '8', 'package_name': 'MyMeg 10Test', 'expiry': datetime.datetime(2013, 12, 19, 14, 28, 2, 967827)}

    #balance_info = {'8': {'volume': '638.4828125', 'units': 'MB', 'da_id': '8', 'expiry': datetime.datetime(2013, 12, 19, 12, 0)}, '2': {'volume': '0.0', 'units': 'MB', 'da_id': '2', 'expiry': datetime.datetime(9999, 12, 31, 0, 0)}}

    '''
    parameters = {'msisdn': '261336173681',
            'status': '5',
            'b_msisdn': '261336173681',
            'packageId': '4',
            'transactionId' : '2',
            'transaction_type': 'a',
            'args':'/5|108|True|8|modular_tariffs',
            'name':'MyMeg 10Test',
            'balance' : balance_info}
	    '''

    #parameters = {'status': '7', 'msisdn': '261336173681', 'args': '/5|108|True|8|modular_tariffs', 'expiry': '2014-01-08T12:20:56.900643', 'volume': '160', 'callBack': 'http://127.0.0.1:1102/process/5|108|True|8|modular_tariffs', 'modular_id': '108', 'packageId': '5', 'b_msisdn': '261336173681', 'response': '5||2014-01-08T12:20:56.900643||160||MyMeg 20||128', 'da_id': '8', 'name': 'MyMeg 20', 'transaction_type': 'a', 'renew': 'True', 'package_requested': '5', 'transactionId': '128', 'balance': {'volume': 160, 'units': 'MB', 'da_id': '8', 'package_name': 'MyMeg 20', 'expiry': '2014-01-08T12:20:56.900643'}, 'channel': 'modular_tariffs'}

    parameters = {"status": "5", "args": "/0|192|False|False|modular_tariffs", "name": "balance", "packageId": "0", "msisdn": "261261336173681", "balance": {"8": {"volume": "1475.0", "units": "MB", "da_id": "8", "expiry": "2014-01-16T12:00:00"}, "2": {"volume": "False", "units": "MB", "da_id": "2", "expiry": "False"}, "14": {"volume": "False", "units": "MB", "da_id": "16", "expiry": "False"}}, "transactionId": "211", "transaction_type": "a", "b_msisdn": "261336173681","response":"5||2014-01-16T12:00:00||1475.0||||211"}

    parameters['package_requested'], \
            parameters['modular_id'], \
            parameters['renew'], \
            parameters['da_id'], \
            parameters['channel'] = \
            parameters['args'].split('|')

    parameters['package_requested'] = str(parameters['package_requested']).replace('/','')
    resources['parameters'] = parameters
    
    print resources
    test_process_provision_response(resources)
