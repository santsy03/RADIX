#!/usr/bin/env python2.7
#from twisted.internet import epollreactor
#epollreactor.install()
from twisted.application import service,internet
from twisted.web import resource, server
from twisted.internet import reactor
from twisted.python.logfile import DailyLogFile
from twisted.python.log import ILogObserver,FileLogObserver
from mg_aapcn_me2u.hxc_proxy.config import PORTS, THREADS
from server import MenuService

port = PORTS['hxc_proxy']['177']
threads = THREADS['hxc_proxy']

hxcServer = MenuService()
hxcProxyService = internet.TCPServer(port, server.Site(hxcServer))
hxcProxyService.setName('hxc_proxy_177')
application = service.Application('hxc_proxy_177')
logfile = DailyLogFile("logs/twistd.log-177-hxcproxy",".")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
hxcProxyService.setServiceParent(application)
reactor.suggestThreadPoolSize(threads)
