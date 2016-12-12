#!/usr/bin/env python
from twisted.application import internet,service
from twisted.web import server,resource
from smsServer import RequestFactory
from twisted.python.log import ILogObserver,FileLogObserver
from twisted.python.logfile import DailyLogFile
from twisted.internet import reactor
from modular_tariffs.src.configs import PORTS, THREADS
port = PORTS['sms']
threads = THREADS['sms']

ProfilerService = internet.TCPServer(port, RequestFactory())
ProfilerService.setName('modular-sms-server')
application = service.Application('modular-sms-server')
ProfilerService.setServiceParent(application)
logfile = DailyLogFile('logs/twistd-modular-sms-server.log','.')
application.setComponent(ILogObserver,FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(threads)
