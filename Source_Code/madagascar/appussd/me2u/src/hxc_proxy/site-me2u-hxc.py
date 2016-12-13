#!/usr/bin/env python2.7
#from twisted.internet import epollreactor
#epollreactor.install()
from twisted.application import service,internet
from twisted.web import resource, server
from twisted.internet import reactor
from twisted.python.logfile import DailyLogFile
from twisted.python.log import ILogObserver,FileLogObserver
from me2u.src.config import PORTS, THREADS
from server import MenuService

port = int(PORTS['flares'])
threads = int(THREADS['flares'])

hxcServer = MenuService()
hxcProxyService = internet.TCPServer(port, server.Site(hxcServer))
hxcProxyService.setName('me2u_hxc_proxy')
application = service.Application('me2u_hxc_proxy')
logfile = DailyLogFile("logs/twistd.log-me2u-hxcproxy",".")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
hxcProxyService.setServiceParent(application)
reactor.suggestThreadPoolSize(threads)
