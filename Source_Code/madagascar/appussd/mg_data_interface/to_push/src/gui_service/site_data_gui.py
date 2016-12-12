#!/usr/bin/env python
from twisted.application import internet, service
from twisted.web import server,resource
from twisted.internet import reactor
from adaptor import Factory
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile


Service = Factory()
factory = server.Site(Service)
#factory.sessionFactory = SessionFactory # add session
GuiService = internet.TCPServer(8787, factory)
application = service.Application('guiservice')
GuiService.setName('guiservice')
GuiService.setServiceParent(application)
#logging
logfile = DailyLogFile('twistd.log', './logs/')
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(200)
