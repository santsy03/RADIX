#!/usr/bin/env python
from twisted.application import internet,service
from twisted.web import server,resource
from languageServer import RequestFactory
from twisted.python.log import ILogObserver,FileLogObserver
from twisted.python.logfile import DailyLogFile
from twisted.internet import reactor

ProfilerService = internet.TCPServer(9062,RequestFactory())
ProfilerService.setName('450-sms-server')
application = service.Application('450-sms-server')
ProfilerService.setServiceParent(application)
logfile = DailyLogFile('twistd.log-450-sms-server','.')
application.setComponent(ILogObserver,FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(1)
