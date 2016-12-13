#!/usr/bin/python2.4
from twisted.application import internet,service
from twisted.web import server,resource
from modularResponsesServer import RequestFactory
from twisted.python.log import ILogObserver,FileLogObserver
from twisted.python.logfile import DailyLogFile
from twisted.internet import reactor
from modular_tariffs.src.configs import THREADS, PORTS
port = PORTS['responses']
threads = THREADS['responses']['listener']

ProfilerService = internet.TCPServer(port, RequestFactory())
ProfilerService.setName('modular-responses-server')
application = service.Application('modular-responses-server')
ProfilerService.setServiceParent(application)
logfile = DailyLogFile('logs/twistd.log-modular-responses-server','.')
application.setComponent(ILogObserver,FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(threads)
