from configs.config import databases
from utilities.secure.core import decrypt
from utilities.ucip.core import get_balance_and_date
from utilities.metrics.core import beat
from utilities.sms.core import send_message
from cx_Oracle import SessionPool


def generate_connection():
    '''
    returns connection as expected by 
    events

    '''
    connections = SessionPool(\
            decrypt(databases['core']['username']), \
            decrypt(databases['core']['password']), \
            databases['core']['string'],\
            2,500, 2, threaded=True)

    resources = {}
    resources['connections'] = connections
    return resources

