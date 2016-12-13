#!/usr/bin/python2.7
from twisted.application import internet,service
from twisted.web import server,resource
from modularRequestsServer import RequestFactory
from twisted.python.log import ILogObserver,FileLogObserver
from twisted.python.logfile import DailyLogFile
from twisted.internet import reactor
from modular_tariffs.src.configs import THREADS, PORTS
port = PORTS['requests_http']
threads = THREADS['requests_http']

ProfilerService = internet.TCPServer(port, RequestFactory())
ProfilerService.setName('modular-requests-http')
application = service.Application('modular-requests-http')
ProfilerService.setServiceParent(application)
logfile = DailyLogFile('logs/twistd.log-modular-requests-http','.')
application.setComponent(ILogObserver,FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(threads)
