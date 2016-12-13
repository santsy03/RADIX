'''
returns a connection pool to the database
in a dict as expected by events
'''

from configs.config import databases
from utilities.secure.core import decrypt
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
            2,50, 1, threaded=True)

    resources = {}
    resources['connections'] = connections
    return resources

