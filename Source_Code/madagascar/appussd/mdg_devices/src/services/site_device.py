#!/usr/bin/env python
from twisted.application import service, internet
from twisted.web import server
from twisted.internet import reactor
from twisted.python.logfile import DailyLogFile
from twisted.python.log import ILogObserver, FileLogObserver
from mdg_devices.src.configs.general import TWISTED

PORT = TWISTED['PORT']
THREADS = TWISTED['THREADS']
LOGS = TWISTED['LOGS']
LOG_NAME = TWISTED['LOG_NAME']


from adaptor import ServiceFactory
flaresProxyService = internet.TCPServer(PORT, server.Site(ServiceFactory()))
flaresProxyService.setName('channel-service-server')
application = service.Application('channel-service-server')
logfile = DailyLogFile('%s/%s' % (str(LOGS), str(LOG_NAME)), '.')
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
flaresProxyService.setServiceParent(application)
reactor.suggestThreadPoolSize(THREADS)
