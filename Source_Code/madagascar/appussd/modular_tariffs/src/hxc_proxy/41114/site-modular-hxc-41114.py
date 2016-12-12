#!/usr/bin/env python2.7
#from twisted.internet import epollreactor
#epollreactor.install()
from twisted.application import service,internet
from twisted.web import resource, server
from twisted.internet import reactor
from twisted.python.logfile import DailyLogFile
from twisted.python.log import ILogObserver,FileLogObserver
from modular_tariffs.src.configs import PORTS, THREADS
from server import MenuService

port = PORTS['hxc_proxy']['41114']
threads = THREADS['hxc_proxy']

hxcServer = MenuService()
hxcProxyService = internet.TCPServer(port, server.Site(hxcServer))
hxcProxyService.setName('modular_hxc_proxy_41114')
application = service.Application('modular_hxc_proxy_41114')
logfile = DailyLogFile("logs/twistd.log-modular-hxcproxy41114",".")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
hxcProxyService.setServiceParent(application)
reactor.suggestThreadPoolSize(threads)
