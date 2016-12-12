#!/usr/bin/env python
from twisted.application import service,internet
from twisted.web import server
from twisted.internet import reactor
from menuServer import MenuService
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile
#from mg_aapcn_me2u.hxc_proxy.config import PORTS, THREADS

#port = PORTS['ussd']['me2u']
#threads = THREADS['ussd']

HOST_NAME = __import__('socket').gethostname()

SiteServer = MenuService()
#SiteService = internet.TCPServer(port,server.Site(SiteServer))
SiteService = internet.TCPServer(9343,server.Site(SiteServer))
SiteService.setName('me2u-prepaid-menus')
application = service.Application('me2u-prepaid-menus')
SiteService.setServiceParent(application)
logfile = DailyLogFile("logs/twistd.log_me2u_menus-{}".format(HOST_NAME), ".")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
#reactor.suggestThreadPoolSize(threads)
reactor.suggestThreadPoolSize(200)
