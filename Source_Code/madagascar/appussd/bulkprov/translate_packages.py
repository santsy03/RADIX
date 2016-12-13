#!/usr/bin/python2.7

import csv
from datetime import datetime, timedelta, date
import sys

class Error(object):
    def __init__(self):
        from datetime import datetime
        now = datetime.now()
        today = str(now).replace(' ','_').split('.')[0]
        self.file_name = '/appussd/bulkprov/bulkfiles/logs/package_translate_errors_%s.txt' % (today)
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
        self.file_name = '/appussd/bulkprov/bulkfiles/logs/package_translate_successes_%s.txt' % (today)
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
    success = Success()
    error = Error()
    with open(file_, 'rb') as _csv_file:
        reader = csv.reader(_csv_file)
        for row in reader:
            pack = row[1]
            msisdn = row[0]
            package = translate_package(pack,msisdn,error, success)
            rec = str(msisdn)+','+str(package)
            whitelist_list.append(rec)
    #Return without the header row
    error.close()
    success.close()
    return whitelist_list

def yield_list(whitelist_list):
    for i in whitelist_list:
        yield i

def translate_package(package,msisdn,error,success):
    from config import PACK_TRANSLATION

    try:
        packageId = PACK_TRANSLATION[int(package)]

    except KeyError:
        packageId = str(package)
        cdr = 'MSISDN: %s PACKAGE_ID: %s Not Translated' % (msisdn, packageId)
        error.log(cdr)

    cdr = 'MSISDN: %s PACKAGE_ID: %s Translated To: %s' % (msisdn,package,packageId)
    success.log(cdr)

    return packageId

'''
'''
def write(res):
    reportdir = '/appussd/bulkprov/bulkfiles/'
    report = 'MG_Translated_PackageIds_' + (date.today()).strftime('%Y-%m-%d')+'_'+(datetime.now()).strftime('%H')+'00HRS'+'.csv'
    try:
        file = open(reportdir + report, 'w')
        for result in res:
            file.write("%s\n" %(result))
    except:
        print "Error: cannot write report file\n"
        sys.exit(1)
    file.close()

def run():
    filename = '/appussd/bulkprov/bulkfiles/MG_Failed_Refills_%s_%s00HRS.csv'%((date.today()).strftime('%Y-%m-%d'),(datetime.now()).strftime('%H'))
    #filename = '/appussd/bulkprov/bulkfiles/MG_Failed_Refills_2016-09-20_1100HRS.csv'
    
    content = read_csv(filename)
    gen_final_list = yield_list(content)
    
    write(gen_final_list)

if __name__ == '__main__':
    run()
