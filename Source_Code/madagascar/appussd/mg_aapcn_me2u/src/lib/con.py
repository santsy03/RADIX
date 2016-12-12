from configs.config import databases
from utilities.secure.core import decrypt
import cx_Oracle
from DBUtils.PooledDB import PooledDB



def generate_connection():
    '''
    returns connection as expected by 
    events

    '''
    connections = PooledDB(
                cx_Oracle,
                maxcached = 5,
                maxconnections = 50,
                user = decrypt(databases['core']['username']),
                password = decrypt(databases['core']['password']),
                dsn = databases['core']['string']
                )
 

    resources = {}
    resources['connections'] = connections
    return resources

