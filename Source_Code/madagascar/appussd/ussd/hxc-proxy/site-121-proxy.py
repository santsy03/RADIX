#!/usr/bin/env python2.7
#from twisted.internet import epollreactor
#epollreactor.install()
from twisted.application import service,internet
from twisted.web import resource, server
from twisted.internet import reactor
from twisted.python.logfile import DailyLogFile
from twisted.python.log import ILogObserver,FileLogObserver

HOST_NAME = __import__('socket').gethostname()

from menuserver import MenuService
hxcServer = MenuService()
hxcProxyService = internet.TCPServer(9001,server.Site(hxcServer))
hxcProxyService.setName('hxcProxy')
application = service.Application('hxcProxy')
logfile = DailyLogFile("logs/twistd.log-hxcProxy-{}".format(HOST_NAME), ".")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
hxcProxyService.setServiceParent(application)
reactor.suggestThreadPoolSize(200)
