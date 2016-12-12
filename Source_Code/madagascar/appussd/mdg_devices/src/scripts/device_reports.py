from datetime import datetime, timedelta, date

STATES = {}
STATES[0] = 'IMEI SUCCESSFULLY PROVISIONED'
STATES[1] = 'IMEI USED'
STATES[2] = 'IMEI NOT WHITELISTED'
STATES[3] = 'ERROR DURING PROCESSING'
STATES[5] = 'QUEUED FOR PROVISIONING'
STATES[6] = 'IMEI NOT FOUND'
STATES[7] = 'IMEI DEACTIVATED'
STATES[8] = 'RETAILER NOT WHITELISTED'
STATES[9] = 'CLAIMED TRANSACTION ID'
STATES[10] = 'SUCCESSFUL CLAIM OF TRANSACTION ID'

LOCATION = '/tmp'

DST = '/appussd/monitor/device_reports'

date_today = datetime.now()

yesterday = date_today - timedelta(days = 1)

split_date = str(date_today).split(' ')[0]

split_date_yesterday = str(yesterday).split(' ')[0]

file_name = '%s_device_reports.csv' % split_date

_file_string = '%s/%s' % (LOCATION,
            file_name)

zipfilename = '%s/%s_device_reports.zip' % (DST, split_date)

def setup():
    import cx_Oracle
    from DBUtils.PooledDB import PooledDB
    from utilities.secure.core import decrypt
    from configs.config import databases
    core = databases['core']
    pooled = PooledDB(cx_Oracle, 
        maxcached = 5,
        maxconnections = 10,
        user = decrypt(core['username']),
        password = decrypt(core['password']),
        dsn = core['string'],
        threaded = True)
    _file = open_file()
    return pooled, _file

def get_data_list():
    mon =  date_today.strftime("%B")[:3]
    days_list = ''
    for i in range(1, date_today.day):
        if not days_list == '':
            days_list = days_list+','
        day = "'%s-%s-%s'" % (str(i), mon, date_today.year)
        days_list = days_list + day
    return days_list

def open_file():
    return open(_file_string, 'w')

def close_file(_file):
    _file.close()

def write_to_file(_file, item):
    _file.write(item)

def get_whitelist_details(pool, _file):
    """
    total = get_total_imei(pool)
    write_to_file(_file,total)
    used = get_used_imei(pool)
    write_to_file(_file,used)
    available = get_available_imei(pool)
    write_to_file(_file,available)
    total_claimed = get_total_claimed(pool)
    write_to_file(_file,total_claimed)
    total_unclaimed = get_total_unclaimed(pool)
    write_to_file(_file,total_unclaimed)
    write_to_file(_file,'\n\n')
    overal_breakdown = get_transaction_break_down_overally(pool)
    write_to_file(_file,overal_breakdown+'\n')
    total_requests = get_total_requests(pool)
    write_to_file(_file,'\t'+total_requests+'\n\n')
    periodic_breakdown = get_transaction_break_down_periodic(pool)
    periodic_breakdown = loop_through_breakdown(periodic_breakdown,
            '\nTRANSACTION BREAKDOWN FOR %s' % split_date_yesterday)
    write_to_file(_file,periodic_breakdown+'\n')
    total_request_periodic = get_total_requests_periodic(pool)
    write_to_file(_file,'\t'+total_request_periodic+'\n\n')
    """
    day_list = get_data_list()
    breakdown = get_hits_per_day(pool, day_list)
    rec = loop_through_breakdown(breakdown, day_list)
    write_to_file(_file, rec)
    close_file(_file)

def get_hits_per_day(pool, day_list):
    sql = ("select * from (SELECT status as "
            "Status,COUNT(*) AS hits,trunc(created_at) "
            "as day FROM device_requests where created_at > "
            "to_date('2015-04-01','yyyy-mm-dd') "
            "group by status,trunc(created_at)) "
            "pivot (sum(hits) for day "
            "in(%s)) "
            "order by Status")
    sql = sql % day_list
    breakdown = run_query(pool, sql)
    if not breakdown:
        breakdown = 'COULD NOT BE RETRIEVED'
    return breakdown


def get_used_imei(pool):
    sql = ('select count(*) from whitelist_imei where status = 1')
    count = 'COULD NOT BE RETRIEVED'
    used = run_query(pool, sql)
    if used:
        count = used[0][0]
    cdr = ("\n TOTAL IMEIS PROVISIONED : %s" % str(count))
    return cdr

def get_total_imei(pool):
    sql = ('select count(*) from whitelist_imei')
    count = 'COULD NOT BE RETRIEVED'
    used = run_query(pool, sql)
    if used:
        count = used[0][0]
    cdr = ("\n TOTAL IMEIS WHITELISTED : %s" % str(count))
    return cdr

def loop_through_breakdown(ret, day_list):
    headers = 'STATES'
    rec = headers+','+day_list
    for item in ret:
        item = list(item)
        status = STATES.get(item[0])
        item.pop(0)
        i = 0
        cdr = ''
        for state in item:
            if state == None:
                state = '0'
            cdr = cdr + ("%s,"
                    % (state))
        cdr = status+','+ cdr

        rec = rec +'\n'+ cdr
    return rec

def get_available_imei(pool):
    sql = ('select count(*) from whitelist_imei where status = 0')
    count = 'COULD NOT BE RETRIEVED'
    used = run_query(pool, sql)
    if used:
        count = used[0][0]
    cdr = ("\n TOTAL IMEIS STILL AVAILABLE : %s" % str(count))
    return cdr

def get_total_requests(pool):
    sql = ("select count(*) from device_requests "
           " where created_at > to_date('2015-04-01 12:00:00 AM', "
           "'yyyy-mm-dd HH:MI:SS AM')")
    count = 'COULD NOT BE RETRIEVED'
    used = run_query(pool, sql)
    if used:
        count = used[0][0]
    cdr = ("\n TOTAL REQUESTS HANDLED : %s" % (str(count)))
    return cdr

def get_total_requests_periodic(pool):
    sql = ("select count(*) from device_requests "
            "where created_at BETWEEN to_date('%s 12:00:00 AM', "
            "'yyyy-mm-dd HH:MI:SS AM') AND to_date('%s 12:00:00 AM', "
            "'yyyy-mm-dd HH:MI:SS PM')")
    sql = sql % (split_date_yesterday, split_date)
    count = 'COULD NOT BE RETRIEVED'
    used = run_query(pool, sql)
    if used:
        count = used[0][0]
    cdr = ("\n REQUESTS HANDLED FOR %s : %s" % (split_date_yesterday, str(count)))
    return cdr

def get_total_claimed(pool):
    sql = ("select count(*) from whitelist_imei "
            "where claim_status = 1 ")
    count = 'COULD NOT BE RETRIEVED'
    used = run_query(pool, sql)
    if used:
        count = used[0][0]
    cdr = ("\n TOTAL TRANSACTION IDS CLAIMED : %s" % str(count))
    return cdr

def get_total_unclaimed(pool):
    sql = ("select count(*) from whitelist_imei "
            "where claim_status = 0 ")
    count = 'COULD NOT BE RETRIEVED'
    used = run_query(pool, sql)
    if used:
        count = used[0][0]
    cdr = ("\n TOTAL TRANSACTION IDS NOT YET CLAIMED : %s" % str(count))
    return cdr

def get_transaction_break_down_overally(pool):
    sql = ("SELECT status, COUNT(*) AS hits FROM device_requests "
            "where created_at > to_date('2015-04-01 12:00:00 AM',"
            " 'yyyy-mm-dd HH:MI:SS AM') GROUP BY status")
    count = 'COULD NOT BE RETRIEVED'
    breakdown = run_query(pool, sql)
    return breakdown

def get_transaction_break_down_periodic(pool):
    sql = ("SELECT status, COUNT(*) AS hits FROM device_requests "
            "where created_at BETWEEN to_date('%s 12:00:00 AM', "
            "'yyyy-mm-dd HH:MI:SS AM') AND to_date('%s 12:00:00 AM', "
            "'yyyy-mm-dd HH:MI:SS PM') GROUP BY status")
    sql = sql % (split_date_yesterday, split_date)
    count = 'COULD NOT BE RETRIEVED'
    breakdown = run_query(pool, sql)
    return breakdown

def run_query(pool, query):
    try:
        con = pool.connection()
        cur = con.cursor()
        cur.execute(query)
        ret = cur.fetchall()
        cur.close()
        con.close()
        return ret
    except Exception, err:
        print err
        try:
            cur.close()
            con.close()
        except:
            pass

def zip_file(_file):
    import zipfile
    zf = zipfile.ZipFile(zipfilename, "w", zipfile.ZIP_DEFLATED)
    zf.write(_file)

if __name__ == '__main__':
    pool, _file = setup()
    get_whitelist_details(pool, _file)
    zip_file(_file_string)
