#!/usr/bin/env python
from twisted.application import internet, service
from twisted.web import server,resource
from webservicesServer import Factory
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile
from twisted.internet import reactor
from data_provisioning.src.configs.core import web_services_port

HOST_NAME = __import__('socket').gethostname()

api_service = Factory()
factory = server.Site(api_service)
http_web_service = internet.TCPServer(web_services_port, factory)
application = service.Application('data-webservices-server')
http_web_service.setName('data-webservices')
http_web_service.setServiceParent(application)

logfile = DailyLogFile('logs/twistd.log-webservices-{}'.format(HOST_NAME), '.')
application.setComponent(ILogObserver,FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(600)
