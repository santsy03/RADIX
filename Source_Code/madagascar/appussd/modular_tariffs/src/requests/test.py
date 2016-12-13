def test_process_request(resources):
    from core import process_request
    process_request(resources)


if __name__ == '__main__':
    from server_modular_requests import setup
    resources = setup('log-test')

    parameters = {'msisdn':'261336173681',
            'package_id':'4',
            'action':'provision',
            'renew':'False',
            'transaction_type':'a',
            'b_msisdn':'261336173681',
            'channel':'modular_tariffs'}

    resources['parameters'] = parameters
    resources['msg'] = str(parameters)

    test_process_request(resources)
