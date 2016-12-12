from me2u.src.config import AIR
from core import get_params
from server_me2u import setup

def test_get_sub_balance(resources, party):
    pass

def test_process_request():
    from core import process_request
    resources = setup('test')
    parameters = {}
    parameters['msisdn'] = '261330465390'
    parameters['recipient'] = '261331005578'
    parameters['amount'] = '10'
    resources['parameters'] = parameters
    resources = get_params(resources)
    print process_request(resources)

def test_get_sub_balance():
    from core import get_sub_balance
    resources = {}
    parameters = {}
    parameters['msisdn'] = '261330465390'
    parameters['recipient'] = '261331005578'
    parameters['amount'] = '10'
    resources['parameters'] = parameters
    resources = get_params(resources)
    print get_sub_balance(resources, 'msisdn')
    print get_sub_balance(resources, 'recipient')

def test_get_balance_and_date():
    from utilities.ucip.core import get_balance_and_date
    resources = {}
    parameters = {}
    parameters['msisdn'] = '261336173681'
    parameters['recipient'] = '261336173681'
    resources['parameters'] = parameters
    resources = get_params(resources)
    print get_balance_and_date(resources)


def test_process_sender():
    from core import process_sender
    from core import validate_request
    resources = {}
    parameters = {}
    parameters['msisdn'] = '261336173681'
    parameters['recipient'] = '261336173681'
    parameters['amount'] = '6'
    resources['parameters'] = parameters
    resources = get_params(resources)
    validate_request(resources)
    print process_sender(resources)

def test_update_dedicated_account():
    from utilities.ucip.core import update_dedicated_account
    from core import validate_request
    resources = {}
    parameters = {}
    parameters['msisdn'] = '261336173681'
    parameters['recipient'] = '261336173681'
    parameters['amount'] = '6'
    parameters['action'] = AIR['action']
    parameters['transactionId'] = '10'
    parameters['externalData1'] = AIR['externalData1']
    parameters['externalData2'] = 'test'
    resources['parameters'] = parameters
    validate_request(resources)
    da_id = AIR['dedicated_account']
    da_amount = parameters['amount']
    expiry_date = parameters['sender_profile']['expiry_date']
    print update_dedicated_account(resources, int(da_id), int(da_amount), expiry_date)




if __name__ == '__main__':
    test_process_request()
    #test_get_sub_balance()
    #test_get_balance_and_date()
    #test_process_sender()
    #test_update_dedicated_account()
