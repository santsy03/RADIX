#!/usr/bin/env python
from twisted.application import internet,service
from twisted.web import server,resource
from languageServer import RequestFactory
from twisted.python.log import ILogObserver,FileLogObserver
from twisted.python.logfile import DailyLogFile
from twisted.internet import reactor

HOST_NAME = __import__('socket').gethostname()

ProfilerService = internet.TCPServer(9062,RequestFactory())
ProfilerService.setName('language-server')
application = service.Application('language-server')
ProfilerService.setServiceParent(application)
logfile = DailyLogFile('logs/twistd.log-language-server-{}'.format(HOST_NAME), '.')
application.setComponent(ILogObserver,FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(200)
