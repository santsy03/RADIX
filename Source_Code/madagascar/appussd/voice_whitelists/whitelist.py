import csv
class Error(object):
    def __init__(self):
        from datetime import datetime
        now = datetime.now()
        today = str(now).replace(' ','_').split('.')[0]
        self.file_name = '/appussd/voice_whitelists/logs/voice_whitelist_errors_%s.txt' % (today)
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
        self.file_name = '/appussd/voice_whitelists/logs/voice_whitelist_successes_%s.txt' % (today)
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
            msisdn = row[0]
            package_id = row[1]
            rec = str(msisdn)+','+str(package_id)
            whitelist_list.append(rec)
    #Return without the header row
    return whitelist_list[1:]

def yield_list(whitelist_list):
    for i in whitelist_list:
        yield i


def add_whitelist(rec,con, error, success):
    msisdn, package = rec.split(',')
    package_id = int(package)
    sql = "insert into VOICE_BUNDLES_WHITELIST(MSISDN,PACKAGE_ID) values (:msisdn, :package_id)"
    params = {'msisdn':str(msisdn),'package_id':package_id}
    try:
        cursor = con.connection().cursor()
        cursor.execute(sql, params)
        cursor.connection.commit()
        cursor.close()
        cdr = 'MSISDN: %s PACKAGE_ID: %s added' % (msisdn, str(package_id))
        success.log(cdr)
    except Exception, err:
        cdr = 'MSISDN: %s PACKAGE_ID: %s failed: %s' % (msisdn, str(package_id), str(err))
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
