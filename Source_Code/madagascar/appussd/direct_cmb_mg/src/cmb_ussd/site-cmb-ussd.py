#!/usr/bin/env python2.7
from twisted.application import service,internet
from twisted.web import server
from twisted.internet import reactor
from menuServer import MenuService
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile
from direct_cmb_mg.src.config import PORTS, LOGS, THREADS

HOST_NAME = __import__('socket').gethostname()

SiteServer = MenuService()
SiteService = internet.TCPServer(PORTS['cmb_ussd'], server.Site(SiteServer))
SiteService.setName('direct-cmb-ussd')
application = service.Application('direct-cmb-ussd')
SiteService.setServiceParent(application)
logfile = DailyLogFile("twistd.log-direct-cmb-ussd-{}".format(HOST_NAME),
                       LOGS['ussd'])
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(THREADS['ussd'])
