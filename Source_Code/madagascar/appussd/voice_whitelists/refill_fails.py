import csv
class Error(object):
    def __init__(self):
        from datetime import datetime
        now = datetime.now()
        today = str(now).replace(' ','_').split('.')[0]
        self.file_name = '/appussd/voice_whitelists/logs/refill_search_errors.txt'
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
        self.file_name = '/appussd/voice_whitelists/logs/refill_fails.csv'
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
    return whitelist_list[0:]

def yield_list(whitelist_list):
    for i in whitelist_list:
        yield i


def search_refills(rec,con, error, success):
    created_at, msisdn = rec.split(',')
    #package_id = int(package)
    sql = "select a.msisdn,b.package_name,CASE a.status WHEN 3 then 'REFILL TIMEOUT' END as STATUS,a.created_at from requests a, new_packages b where a.package_id = b.PROVISIONING_PACKAGES_ID and a.MSISDN = :msisdn and to_char(a.CREATED_AT,'yyyy-mm-dd HH24') = :created_at and status =3 and ROWNUM <= 1"
    #sql = "insert into VOICE_BUNDLES_WHITELIST(MSISDN,PACKAGE_ID) values (:msisdn, :package_id)"
    params = {'msisdn':str(msisdn),'created_at':str(created_at)}
    try:
        cursor = con.connection().cursor()
        cursor.execute(sql, params)
        #cursor.connection.commit()
        res = cursor.fetchall()
        cursor.close()
        #cdr = res
        #cdr = 'MSISDN: %s PACKAGE_ID: %s added' % (msisdn, str(package_id))
        #success.log(res)
        return res
    except Exception, err:
        cdr = 'MSISDN: %s failed: %s' % (msisdn, str(err))
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
    result = [] 
    for i in gen_white_list:
        res = search_refills(i, con, error, success)
        result.append(res)
        print res
    #print result
    try:
        file = open('refills.csv', 'w')
        #print "***********************************"    
        file.write("MSISDN,BUNDLE,STATUS,CREATED_AT\n")
        for package in result:
            file.write("%s\n" %(','.join(i.__str__() for i in package[0:])))
    except:
        print "Error: cannot write report file\n"
        sys.exit(1)
    file.close()



    error.close()
    #success.close()

if __name__ == '__main__':
    run()
