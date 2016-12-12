#!/usr/bin/python2.7
#author: SIMON
#Date: 2015-1-24
#Reports refill fails

import sys
import zipfile
from cx_Oracle import Cursor,Connection
from datetime import datetime, timedelta, date
sys.path.append('/appussd/')
from configs.config import databases as database
from utilities.secure.core import decrypt
from operator import *

class Report:
    def __init__(self):
        self.reportdir = '/appussd/bulkprov/bulk_reports/'
        self.report = 'MG_Reprovisioning_Report_' + (date.today()).strftime('%Y-%m-%d')+'_'+(datetime.now()).strftime('%H')+'00HRS'+'.csv'
        self.user = decrypt(database['core']['username'])
        self.passwd = decrypt(database['core']['password'])
        self.conn = database['core']['string']
    
    def trudiv(self, num, denom):
        if denom == 0:
            return 0
        else:
            return num/denom

    def query(self):
        try:
            conns = Connection(user=self.user, password=self.passwd, dsn=self.conn)
        except:
            print "Could not connect to databases\n"
            sys.exit(1)
        #interval '1' Hour 
        curs = Connection.cursor(conns)
    
        sql = """select a.msisdn,CASE a.status WHEN 0 THEN 'QUEUED' WHEN 3 THEN 'ERROR' WHEN 5 THEN 'SUCCESS' WHEN 15 THEN 'REFILL FAILED' END as State, b.package_name,a.created_at from requests_test a, new_packages b where a.package_id in (259,261,262,263,264,265,266,267,269,270,272,273,274,275,276,277.288,289,291,311,312,313,318,319,320,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,367,368,369,370,371,372,373,374,375,385,386,387,388,389,390,391,392,393) and a.package_id = b.id and a.created_at > sysdate- interval '10' Minute order by a.created_at asc"""

        curs.execute(sql)
        res = curs.fetchall()
        curs.close()
        return res

    def write(self, res):
        try:
            file = open(self.reportdir + self.report, 'w')
            file.write("MSISDN,STATUS,BUNDLE,CREATED_AT\n")
            for result in res:
                file.write("%s\n" %(','.join(i.__str__() for i in result[0:])))
        except:
            print "Error: cannot write report file\n"
            sys.exit(1)
        file.close()
    

r = Report()
res = r.query()
#print res
r.write(res)
