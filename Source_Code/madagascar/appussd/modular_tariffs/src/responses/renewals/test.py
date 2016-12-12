def test_process_provision_response(resources):
    from modular_tariffs.src.responses.consumer.core import process_provision_response
    process_provision_response(resources)


if __name__ == '__main__':
    from server_modular_renewal_responses import setup
    import datetime
    resources = setup('log-test')
    resources['connections'] = resources['db_connection']

    parameters = {'status': '5', 'msisdn': '261336173681', 'args': '/5|142|True|8|renewals|0|0', 'expiry': '2014-01-10T12:00:00', 'volume': '800', 'callBack': 'http://127.0.0.1:1102/process/5|142|True|8|renewals', 'modular_id': '142', 'packageId': '5', 'b_msisdn': '261336173681', 'response': '5||2014-01-10T12:00:00||800||MyMeg 20||160', 'da_id': '8', 'name': 'MyMeg 20', 'transaction_type': 'a', 'renew': 'True', 'package_requested': '5', 'transactionId': '160', 'balance': {'volume': 800, 'units': 'MB', 'da_id': '8', 'package_name': 'MyMeg 20', 'expiry': '2014-01-10T12:00:00'}, 'channel': 'renewals'}


    package_requested, \
            parameters['modular_id'], \
            parameters['renew'], \
            parameters['da_id'], \
            parameters['channel'], \
            parameters['frequency'], \
            parameters['renewal_days'] = \
            parameters['args'].split('|')

    parameters['package_requested'] = str(package_requested).replace('/','')
    resources['parameters'] = parameters

    test_process_provision_response(resources)
