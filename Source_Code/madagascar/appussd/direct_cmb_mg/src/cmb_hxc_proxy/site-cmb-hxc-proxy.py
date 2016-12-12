#!/usr/bin/env python2.7
#from twisted.internet import epollreactor
#epollreactor.install()
from twisted.application import service,internet
from twisted.web import server
from twisted.internet import reactor
from twisted.python.logfile import DailyLogFile
from twisted.python.log import ILogObserver,FileLogObserver
from menuserver import MenuService
from direct_cmb_mg.src.config import THREADS, PORTS, LOGS

HOST_NAME = __import__('socket').gethostname()

hxcServer = MenuService()
hxcProxyService = internet.TCPServer(PORTS['cmb_flares'], server.Site(hxcServer))
hxcProxyService.setName('cmb_hxc_proxy')
application = service.Application('cmb_hxc_proxy')
logfile = DailyLogFile("twistd.cmb-hxc-proxy-{}.log".format(HOST_NAME),
                       LOGS['flares'])
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
hxcProxyService.setServiceParent(application)
reactor.suggestThreadPoolSize(THREADS['flares'])
