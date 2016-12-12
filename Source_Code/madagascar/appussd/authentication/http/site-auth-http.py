#!/usr/bin/python2.7
from twisted.application import internet, service
from authentication.http.server import RequestFactory
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile
from twisted.internet import reactor
from authentication.configs import (THREADS, PORTS, LOGS)
port = PORTS['http']
threads = THREADS['http']
log = LOGS['http']

ProfilerService = internet.TCPServer(port, RequestFactory())
ProfilerService.setName('authentication-http')
application = service.Application('authentication-http')
ProfilerService.setServiceParent(application)
logfile = DailyLogFile(log, '.')
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(threads)
