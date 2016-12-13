import csv
class Error(object):
    def __init__(self):
        from datetime import datetime
        now = datetime.now()
        today = str(now).replace(' ','_').split('.')[0]
        self.file_name = '/appussd/voice_whitelists/logs/refill_whitelist_errors_%s.txt' % (today)
        self._open_()

    def _open_(self):
        self.file_ =  open(self.file_name, 'a')
        self.file_.write('>>>>>error logging started>>>>>\n')

    def log(self, message):
        self.file_.write(message)
        self.file_.write('\n\n')

    def close(self):
        self.file_.write('>>>>>error logging completed>>>>>\n')
        self.file_.close()

class Success(object):
    def __init__(self):
        from datetime import datetime
        now = datetime.now()
        today = str(now).replace(' ','_').split('.')[0]
        self.file_name = '/appussd/voice_whitelists/logs/refill_whitelist_successes_%s.txt' % (today)
        self._open_()

    def _open_(self):
        self.file_ =  open(self.file_name, 'a')
        self.file_.write('>>>>>success logging started>>>>>\n')

    def log(self, message):
        self.file_.write(message)
        self.file_.write('\n\n')

    def close(self):
        self.file_.write('>>>>>success logging completed>>>>>\n')
        self.file_.close()

def read_csv(file_):
    whitelist_list = []
    with open(file_, 'rb') as _csv_file:
        reader = csv.reader(_csv_file)
        for row in reader:
            created_at = row[0]
            msisdn = row[1]
            rec = str(created_at)+','+str(msisdn)
            whitelist_list.append(rec)
    #Return without the header row
    return whitelist_list[1:]

def yield_list(whitelist_list):
    for i in whitelist_list:
        yield i


def add_whitelist(rec,con, error, success):
    created_at, msisdn = rec.split(',')
    #package_id = int(package)
    sql = "insert into REFILL_FAILS(created_at,msisdn) values (:created_at, :msisdn)"
    params = {'created_at':str(created_at),'msisdn':str(msisdn)}
    try:
        cursor = con.connection().cursor()
        cursor.execute(sql, params)
        cursor.connection.commit()
        cursor.close()
        cdr = 'CREATED_AT: %s MSISDN: %s added' % (created_at, msisdn)
        success.log(cdr)
    except Exception, err:
        cdr = 'MSISDN: %s CREATED_AT: %s failed: %s' % (msisdn, created_at, str(err))
        error.log(cdr)
        try:
            cursor.close()
        except:
            pass

def setup():
    import cx_Oracle
    from DBUtils.PooledDB import PooledDB
    from utilities.secure.core import decrypt
    from configs.config import databases
    core = databases['core']
    pooled = PooledDB(cx_Oracle, mincached = 10,
        maxcached = 300,
        user = decrypt(core['username']),
        password = decrypt(core['password']),
        dsn = core['string'],
        threaded = True)
    return pooled

def run():
    import sys
    filename = sys.argv[1]
    success = Success()
    error = Error()
    con = setup()
    whitelist = read_csv(filename)
    gen_white_list = yield_list(whitelist)
    
    for i in gen_white_list:
        add_whitelist(i, con, error, success)
    error.close()
    success.close()

if __name__ == '__main__':
    run()
