#!/usr/bin/env python
from twisted.application import service,internet
from twisted.web import resource, server
from twisted.internet import reactor
from menuServer import MenuService
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile
from mg_data_interface.hxc_proxy.config import PORTS, THREADS

port = PORTS['ussd']['100']
threads = THREADS['ussd']
HOST_NAME = __import__('socket').gethostname()

SiteServer = MenuService()
SiteService = internet.TCPServer(port,server.Site(SiteServer))
SiteService.setName('ussd-voice-menus')
application = service.Application('ussd-voice-menus')
SiteService.setServiceParent(application)
logfile = DailyLogFile("logs/twistd.log_menus-{}".format(HOST_NAME), ".")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(threads)
