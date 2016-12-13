#!/usr/bin/env python2.7
#from twisted.internet import epollreactor
#epollreactor.install()
from twisted.application import service,internet
from twisted.web import resource, server
from twisted.internet import reactor
from twisted.python.logfile import DailyLogFile
from twisted.python.log import ILogObserver,FileLogObserver
from mg_data_interface.hxc_proxy.config import PORTS, THREADS
from server import MenuService

port = PORTS['hxc_proxy']['100']
threads = THREADS['hxc_proxy']
HOST_NAME = __import__('socket').gethostname()

hxcServer = MenuService()
hxcProxyService = internet.TCPServer(port, server.Site(hxcServer))
hxcProxyService.setName('hxc_proxy_100')
application = service.Application('hxc_proxy_100')
logfile = DailyLogFile("logs/twistd.log-100-hxcproxy-{}".format(HOST_NAME), ".")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
hxcProxyService.setServiceParent(application)
reactor.suggestThreadPoolSize(threads)
