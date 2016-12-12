#!/usr/bin/env python
from twisted.application import service,internet
from twisted.web import resource, server
from twisted.internet import reactor
from menuServer import MenuService
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile

HOST_NAME = __import__('socket').gethostname()

SiteServer = MenuService()
SiteService = internet.TCPServer(7190,server.Site(SiteServer))
SiteService.setName('ussd')
application = service.Application('ussd')
SiteService.setServiceParent(application)
logfile = DailyLogFile("logs/twistd.log-prepaid-ussd-{}".format(HOST_NAME), ".")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(200)
