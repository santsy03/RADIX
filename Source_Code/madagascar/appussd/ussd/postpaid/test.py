def getBundleBalance(resources):
    logger = resources['logger']
    connection = resources['tabs'].acquire()
    cursor = connection.cursor()
    msisdn = (resources['msisdn'])[-9:]
    try:
        sql = 'select  free_duration - used_duration from crm_pkg_subsequip_airtime where subno = :msisdn'
        params = {'msisdn':msisdn}
        cursor.execute(sql,params)
        results = cursor.fetchall()
        count = cursor.rowcount
    except Exception,e:
        error = 'operation:getBundleBalance,desc:failed retrieving balance for subscriber:error:%s' %(str(e),)
        logger.error(error)
        raise e
    else:
        if count > 0:
            return int((results[0])[0])/1024
        else:
            return 0

def setup(log):
    import logging,os,sys
    from logging.handlers import TimedRotatingFileHandler
    from cx_Oracle import SessionPool
    from postpaid.config import home
    try:
        resources = {}
	#resources['connections'] = SessionPool('pavp','pavp654','10.10.32.97:1521/fnr',20,50,1,threaded=True)
	resources['connections'] = SessionPool('ussdkeadm','admu55dk3','172.23.1.60:1525/ussdke',20,50,1,threaded=True)
        resources['tabs'] = SessionPool('cyn','cynussd','10.10.33.171:1521/PRODTABS',20,50,5,threaded=True)
        cwd = home
        logger = logging.getLogger(log)
        logger.setLevel(logging.DEBUG)
        ch = TimedRotatingFileHandler('%s/%s.log' %(cwd,log,),'midnight')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        resources['logger'] = logger
    except Exception,e:
        sys.exit(2)
    else:
        return resources

if __name__ == '__main__':
    resources = setup('tests-postpaid')
    resources['msisdn'] = '254736103849'
    print getBundleBalance(resources)


