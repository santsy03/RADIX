def test_process_request(resources):
    from core import process_renewal_request
    process_renewal_request(resources)


if __name__ == '__main__':
    from server_modular_renewals import setup
    from modular_tariffs.src.configs import WEB_SERVICES
    resources = setup('log-test')

    parameters = {'msisdn': '261336173681', 'event_id': '1', 'package_id': '5', 'args': '2,5,MyMeg 20,0,0', 'package_name': 'MyMeg 20'}
    parameters['b_msisdn'] = parameters['msisdn']
    parameters['action'] = 'provision'
    parameters['renew'] = 'True'
    parameters['channel'] = WEB_SERVICES['renewal_channel']
    parameters['transaction_type'] = 'a'

    resources['parameters'] = parameters
    resources['msg'] = str(parameters)

    test_process_request(resources)
