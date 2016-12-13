import csv
import sys
from cx_Oracle import IntegrityError


from core import setup


def read_file(whitelist):
    '''
    read .csv file
    '''
    try:
        f = open(whitelist, 'rt')
        reader = csv.reader(f)
    except Exception, e:
        raise e
    else:
        return reader


def push_data(file_name):
    '''
    is the wrapper function
    calls setup to get db conn
    read_file to get csv file object
    create_entry to insert record in db
    '''

    conn = setup()['connections']
    count = 1
    records = read_file(file_name)
    try:
        for record in records:
            cols = len(record)
            if cols == 1:
                msisdn = '261%s' % record[0].strip()[-9:]
                print count, msisdn
                create_entry(conn, msisdn)
                count = count + 1
    except Exception, e:
        error = 'failed to create entry for: %s' % (str(e))
        print error


def create_entry(conn, msisdn):
    '''
    create a whitelist entry in db
    '''

    sql = ('insert into GOODMORNING_WHITELIST(id, msisdn, created_at) '
           'values(GMM_WL_PK.nextval, :msisdn, systimestamp)')
    params = {'msisdn': msisdn}
    try:
        connection = conn.connection()
        cursor = connection.cursor()
        cursor.execute(sql, params)
        cursor.connection.commit()
    except IntegrityError, err:
        error = '%s is already whitelisted' % (msisdn)
        print error
        pass
    except Exception, err:
        error = ('operation:create_entry, desc: failed to '
                 'insert, error: %s' % str(err))
        print error
    finally:
        try:
            cursor.close()
        except Exception, err:
            pass

if __name__ == '__main__':
    argument = sys.argv[1]
    push_data(argument)
