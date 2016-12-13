#!/usr/bin/env python
from twisted.application import internet,service
from postpaidServicesServer import RequestFactory
from twisted.python.log import ILogObserver,FileLogObserver
from twisted.python.logfile import DailyLogFile
from twisted.internet import reactor

HOST_NAME = __import__('socket').gethostname()

ProfilerService = internet.TCPServer(9098,RequestFactory())
ProfilerService.setName('postpaid-services-server')
application = service.Application('postpaid-services-server')
ProfilerService.setServiceParent(application)
logfile = DailyLogFile('logs/twistd.log-postpaid-services-server-{}'.format(HOST_NAME), '.')
application.setComponent(ILogObserver,FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(200)
