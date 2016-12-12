#!/usr/bin/env python
from twisted.application import service,internet
from twisted.web import resource, server
from twisted.internet import reactor
from menuServer import MenuService
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile
from mg_data_interface.hxc_proxy.config import PORTS, THREADS

port = PORTS['ussd']['114']
threads = THREADS['ussd']

SiteServer = MenuService()
SiteService = internet.TCPServer(port,server.Site(SiteServer))
SiteService.setName('ussd-prepaid-menus')
application = service.Application('ussd-prepaid-menus')
SiteService.setServiceParent(application)
logfile = DailyLogFile("logs/twistd.log_menus", ".")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(threads)
reactor.suggestThreadPoolSize(200)
