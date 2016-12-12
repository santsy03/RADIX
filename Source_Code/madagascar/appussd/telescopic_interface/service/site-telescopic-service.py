#!/usr/bin/env python
from twisted.application import internet,service
from adaptor import RequestFactory
from twisted.python.log import ILogObserver,FileLogObserver
from twisted.python.logfile import DailyLogFile
from twisted.internet import reactor

HOST_NAME = __import__('socket').gethostname()

ProfilerService = internet.TCPServer(4045,RequestFactory())
ProfilerService.setName('telescopic-proxy-server')
application = service.Application('telescopic-proxy-server')
ProfilerService.setServiceParent(application)
logfile = DailyLogFile('logs/twistd.log-telescopic-{}'.format(HOST_NAME), '.')
application.setComponent(ILogObserver,FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(200)
