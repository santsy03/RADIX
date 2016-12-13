#!/usr/bin/env python
from twisted.application import internet,service
from adaptor import RequestFactory
from twisted.python.log import ILogObserver,FileLogObserver
from twisted.python.logfile import DailyLogFile
from twisted.internet import reactor

HOST_NAME = __import__('socket').gethostname()

ProfilerService = internet.TCPServer(4047,RequestFactory())
ProfilerService.setName('bulkprov-proxy-server')
application = service.Application('bulkprov-proxy-server')
ProfilerService.setServiceParent(application)
logfile = DailyLogFile('logs/twistd.log-bulkprov-{}'.format(HOST_NAME), '.')
application.setComponent(ILogObserver,FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(200)
