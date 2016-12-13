#!/usr/bin/env python
from twisted.application import internet,service
from twisted.web import server,resource
from data_sms_server import RequestFactory
from twisted.python.log import ILogObserver,FileLogObserver
from twisted.python.logfile import DailyLogFile
from twisted.internet import reactor

ProfilerService = internet.TCPServer(4050,RequestFactory())
ProfilerService.setName('data_sms_server')
application = service.Application('data_sms_server')
ProfilerService.setServiceParent(application)
logfile = DailyLogFile('logs/twistd.log-datamix-server','.')
application.setComponent(ILogObserver,FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(200)
