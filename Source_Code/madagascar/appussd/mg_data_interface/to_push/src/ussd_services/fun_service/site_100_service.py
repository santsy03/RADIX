#!/usr/bin/env python
from twisted.application import internet,service
from twisted.web import server,resource
from data_server import RequestFactory
from twisted.python.log import ILogObserver,FileLogObserver
from twisted.python.logfile import DailyLogFile
from twisted.internet import reactor

ProfilerService = internet.TCPServer(7992,RequestFactory())
ProfilerService.setName('data_server')
application = service.Application('data_server')
ProfilerService.setServiceParent(application)
logfile = DailyLogFile('logs/twistd.log-data-100-server','.')
application.setComponent(ILogObserver,FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(200)
