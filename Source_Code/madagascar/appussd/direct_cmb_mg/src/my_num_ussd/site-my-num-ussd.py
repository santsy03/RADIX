#!/usr/bin/env python2.7
from twisted.application import service,internet
from twisted.web import server
from twisted.internet import reactor
from menuServer import MenuService
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile
from direct_cmb_mg.src.config import PORTS, THREADS

HOST_NAME = __import__('socket').gethostname()

SiteServer = MenuService()
SiteService = internet.TCPServer(PORTS['my_num_ussd'], server.Site(SiteServer))
SiteService.setName('my-number-ussd')
application = service.Application('my-number-ussd')
SiteService.setServiceParent(application)
logfile = DailyLogFile("logs/twistd.log-my-number-ussd-{}".format(HOST_NAME), ".")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(THREADS['ussd'])
