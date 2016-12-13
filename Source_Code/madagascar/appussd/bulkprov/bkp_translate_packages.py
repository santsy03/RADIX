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

    billed_packageId = package

    try:
        packageId = PACK_TRANSLATION[int(billed_packageId)]

    except KeyError:
        packageId = str(billed_packageId)
        cdr = 'MSISDN: %s PACKAGE_ID: %s Not Translated' % (msisdn, packageId)
        error.log(cdr)

    cdr = 'MSISDN: %s PACKAGE_ID: %s Translated To: %s' % (msisdn,billed_packageId,packageId)
    success.log(cdr)

    return packageId

'''
    if int(billed_packageId) == 1:
        packageId = '259'
    elif int(billed_packageId) == 3:
        packageId = '261'
    elif int(billed_packageId) == 4:
        packageId = '262'
    elif int(billed_packageId) == 5:
        packageId = '263'
    elif int(billed_packageId) == 6:
        packageId = '264'
    elif int(billed_packageId) == 7:
        packageId = '265'
    elif int(billed_packageId) == 8:
        packageId = '266'
    elif int(billed_packageId) == 9:
        packageId = '267'
    elif int(billed_packageId) == 11:
        packageId = '269'
    elif int(billed_packageId) == 12:
        packageId = '270'
    elif int(billed_packageId) == 14:
        packageId = '272'
    elif int(billed_packageId) == 15:
        packageId = '273'
    elif int(billed_packageId) == 16:
        packageId = '274'
    elif int(billed_packageId) == 19:
        packageId = '275'
    elif int(billed_packageId) == 20:
        packageId = '276'
    elif int(billed_packageId) == 21:
        packageId = '277'
    elif int(billed_packageId) == 32:
        packageId = '288'
    elif int(billed_packageId) == 33:
        packageId = '289'
    elif int(billed_packageId) == 35:
        packageId = '291'
    elif int(billed_packageId) == 58:
        packageId = '311'
    elif int(billed_packageId) == 59:
        packageId = '312'
    elif int(billed_packageId) == 119:
        packageId = '313'
    elif int(billed_packageId) == 131:
        packageId = '318'
    elif int(billed_packageId) == 132:
        packageId = '319'
    elif int(billed_packageId) == 133:
        packageId = '320'
    elif int(billed_packageId) == 179:
        packageId = '323'
    elif int(billed_packageId) == 180:
        packageId = '324'
    elif int(billed_packageId) == 181:
        packageId = '325'
    elif int(billed_packageId) == 182:
        packageId = '326'
    elif int(billed_packageId) == 189:
        packageId = '327'
    elif int(billed_packageId) == 191:
        packageId = '328'
    elif int(billed_packageId) == 193:
        packageId = '329'
    elif int(billed_packageId) == 194:
        packageId = '329'
    elif int(billed_packageId) == 195:
        packageId = '330'
    elif int(billed_packageId) == 197:
        packageId = '331'
    elif int(billed_packageId) == 199:
        packageId = '332'
    elif int(billed_packageId) == 201:
        packageId = '333'
    elif int(billed_packageId) == 203:
        packageId = '334'
    elif int(billed_packageId) == 205:
        packageId = '335'
    elif int(billed_packageId) == 207:
        packageId = '336'
    elif int(billed_packageId) == 209:
        packageId = '337'
    elif int(billed_packageId) == 211:
        packageId = '338'
    elif int(billed_packageId) == 213:
        packageId = '339'
    elif int(billed_packageId) == 215:
        packageId = '340'
    elif int(billed_packageId) == 217:
        packageId = '341'
    elif int(billed_packageId) == 218:
        packageId = '342'
    elif int(billed_packageId) == 219:
        packageId = '343'
    elif int(billed_packageId) == 220:
        packageId = '344'
    elif int(billed_packageId) == 221:
        packageId = '345'
    elif int(billed_packageId) == 222:
        packageId = '346'

    elif int(billed_packageId) == 223:
        packageId = '347'
    elif int(billed_packageId) == 224:
        packageId = '348'
    elif int(billed_packageId) == 225:
        packageId = '349'
    elif int(billed_packageId) == 226:
        packageId = '350'
    elif int(billed_packageId) == 227:
        packageId = '351'
    elif int(billed_packageId) == 228:
        packageId = '352'
    elif int(billed_packageId) == 229:
        packageId = '353'
    elif int(billed_packageId) == 230:
        packageId = '354'
    elif int(billed_packageId) == 231:
        packageId = '355'
    elif int(billed_packageId) == 232:
        packageId = '356'
    elif int(billed_packageId) == 233:
        packageId = '357'
    elif int(billed_packageId) == 234:
        packageId = '358'
    elif int(billed_packageId) == 235:
        packageId = '359'
    elif int(billed_packageId) == 236:
        packageId = '360'

    elif int(billed_packageId) == 240:
        packageId = '361'
    elif int(billed_packageId) == 242:
        packageId = '362'
    elif int(billed_packageId) == 244:
        packageId = '363'

    elif int(billed_packageId) == 250:
        packageId = '367'
    elif int(billed_packageId) == 251:
        packageId = '368'
    elif int(billed_packageId) == 252:
        packageId = '369'
    elif int(billed_packageId) == 253:
        packageId = '370'
    elif int(billed_packageId) == 254:
        packageId = '371'
    elif int(billed_packageId) == 255:
        packageId = '372'
    elif int(billed_packageId) == 256:
        packageId = '373'
    elif int(billed_packageId) == 257:
        packageId = '374'
    elif int(billed_packageId) == 258:
        packageId = '375'

    elif int(billed_packageId) == 376:
        packageId = '385'
    elif int(billed_packageId) == 377:
        packageId = '386'
    elif int(billed_packageId) == 378:
        packageId = '387'

    elif int(billed_packageId) == 379:
        packageId = '388'
    elif int(billed_packageId) == 380:
        packageId = '389'
    elif int(billed_packageId) == 381:
        packageId = '390'

    elif int(billed_packageId) == 382:
        packageId = '391'
    elif int(billed_packageId) == 383:
        packageId = '392'
    elif int(billed_packageId) == 384:
        packageId = '393'
    else:
        packageId = str(billed_packageId)
        cdr = 'MSISDN: %s PACKAGE_ID: %s Not Translated' % (msisdn, packageId)
        error.log(cdr)
    cdr = 'MSISDN: %s PACKAGE_ID: %s Translated To: %s' % (msisdn,billed_packageId,packageId)
    success.log(cdr)

    return packageId
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
