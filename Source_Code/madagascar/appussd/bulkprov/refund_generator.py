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
        self.reportdir = '/appussd/bulkprov/bulkfiles/'
        self.report = 'MG_Failed_Refills_' + (date.today()).strftime('%Y-%m-%d')+'_'+(datetime.now()).strftime('%H')+'00HRS'+'.csv'
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

        curs = Connection.cursor(conns)
        sql = """select b_msisdn,package_id,status,created_at from requests where status=15 and created_at > sysdate- interval '30' Minute order by created_at asc"""
        #sql = """select msisdn,package_id,status,created_at from requests where status=15 and created_at > sysdate- interval '2' Hour order by created_at asc"""
        #sql = """select msisdn,package_id,status,created_at from requests where status=15 and msisdn ='261330465390' order by created_at asc"""
        #sql = """select msisdn,package_id,status,created_at from requests where status=15 and trunc(created_at) = trunc(sysdate) order by created_at asc"""
        curs.execute(sql)
        res = curs.fetchall()
        curs.close()
        return res

    def write(self, res):
        try:
            file = open(self.reportdir + self.report, 'w')
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
