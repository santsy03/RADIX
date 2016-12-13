from configs.config import databases
from utilities.secure.core import decrypt
import cx_Oracle

def test(msisdn):
    connection = cx_Oracle.connect(decrypt(databases['core']['username']),
            decrypt(databases['core']['password']),
            decrypt(databases['core']['string']),
            threaded=True)
    cursor = connection.cursor()
    sql = '''
    select * from service_events where msisdn = :msisdn 
    and can_execute = 1 and status = 0 and service_id =  2 and event_id = 2
    '''
    params = {'msisdn':msisdn}
    cursor.execute(sql, params)
    results = cursor.fetchall()

    print results


if __name__ == '__main__':
    test('22667088086')

