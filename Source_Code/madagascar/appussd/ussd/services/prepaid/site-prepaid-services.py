#!/usr/bin/env python
from twisted.application import internet,service
from twisted.web import server,resource
from prepaidServicesServer import RequestFactory
from twisted.python.log import ILogObserver,FileLogObserver
from twisted.python.logfile import DailyLogFile
from twisted.internet import reactor

HOST_NAME = __import__('socket').gethostname()

ProfilerService = internet.TCPServer(9097,RequestFactory())
ProfilerService.setName('prepaid-services-server')
application = service.Application('prepaid-services-server')
ProfilerService.setServiceParent(application)
logfile = DailyLogFile('logs/twistd.log-prepaid-services-server-{}'.format(HOST_NAME), '.')
application.setComponent(ILogObserver,FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(200)
