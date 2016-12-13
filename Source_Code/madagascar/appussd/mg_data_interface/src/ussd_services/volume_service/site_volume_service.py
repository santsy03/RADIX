#!/usr/bin/env python
from twisted.application import internet,service
from data_server import RequestFactory
from twisted.python.log import ILogObserver,FileLogObserver
from twisted.python.logfile import DailyLogFile
from twisted.internet import reactor

HOST_NAME = __import__('socket').gethostname()

ProfilerService = internet.TCPServer(7990,RequestFactory())
ProfilerService.setName('data_server')
application = service.Application('data_server')
ProfilerService.setServiceParent(application)
logfile = DailyLogFile('logs/twistd.log-data-server-{}'.format(HOST_NAME), '.')
application.setComponent(ILogObserver,FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(200)
