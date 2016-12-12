#!/usr/bin/env python
from twisted.application import service,internet
from twisted.web import resource, server
from twisted.internet import reactor
from menuServer import MenuService
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile
from me2u.src.config import PORTS, THREADS, HOME
logfile = '%s/ussd/logs/twistd.log_me2u_ussd' % HOME
port = PORTS['ussd']
threads = THREADS['ussd']

SiteServer = MenuService()
SiteService = internet.TCPServer(int(port),server.Site(SiteServer))
SiteService.setName('me2u-ussd')
application = service.Application('me2u-ussd')
SiteService.setServiceParent(application)
logfile = DailyLogFile(logfile, ".")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(int(threads))
