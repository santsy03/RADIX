#!/usr/bin/env python2.7
from twisted.application import service,internet
from twisted.web import resource, server
from twisted.internet import reactor
from modular_tariffs.src.ussd_menus.menuServer import MenuService
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile
from modular_tariffs.src.configs import PORTS, THREADS
port = PORTS['ussd']['101']
threads = THREADS['ussd']

SiteServer = MenuService()
SiteService = internet.TCPServer(port, server.Site(SiteServer))
SiteService.setName('modular101-ussd')
application = service.Application('modular101-ussd')
SiteService.setServiceParent(application)
logfile = DailyLogFile("logs/twistd.log-modular101-ussd", ".")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(threads)
