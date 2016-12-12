#!/usr/bin/env python
import pika
from threading import Thread
from pika.adapters import SelectConnection
import os
import logging
from logging.handlers import TimedRotatingFileHandler

class Consumer(object):
    def __init__(self,id,resources):
        
        from modular_tariffs.src.configs import QUEUES
        queue_name = QUEUES['modular_requests']
        self.connection = None
        self.channel = None
        self.response = None
        self.consumerId = 'thread:%d' %(id,)
        self.logger = resources['logger']
        self.db_connection = resources['db_connection']
        self.resources = resources
        self.queue = queue_name

    def handle_delivery(self,channel,method,header,body):
        try:
            from modular_tariffs.src.requests.core import process_request
            from modular_tariffs.src.common import InvalidActionException
            from utilities.logging.core import log
            from datetime import datetime as dt
            import datetime
            msg = str(body).strip()
            start = dt.now()
            resources = self.resources
            resources['msg'] = msg
            resources['logger'] = self.logger
            resources['db_connection'] = self.db_connection
            resources['parameters'] = eval(msg)
            process_request(resources)


        except Exception,e:
            try:
                log( {'logger':self.logger}, 
                        'op:handleDelivery - process_request failed - command: %s - %s' % (
                            message, str(e),), 'error')
            except Exception:
                pass

    def on_queue_declared(self,frame):
        self.logger.debug('... declaring queue')
        self.channel.basic_qos(prefetch_count =1)
        try:
            self.channel.basic_consume(self.handle_delivery,queue=self.queue,no_ack=True)
        except Exception,e:
            self.logger.error('crashing')

    def on_channel_open(self,channel):
        self.channel = channel
        try:
            self.channel.queue_declare(queue=self.queue,exclusive=False,durable=True,auto_delete=False,callback=self.on_queue_declared)
        except Exception,e:
            logger.error(str(e),)

    def on_connected(self,connection):
        connection.channel(self.on_channel_open)

    def consume(self,):
        try:
            from pika.adapters import SelectConnection
            self.connection = SelectConnection(pika.ConnectionParameters(host='127.0.0.1'),self.on_connected)
            self.connection.ioloop.start()
        except Exception,e:
            self.connection.close()
            self.connection.ioloop.start()
        else:
            pass


def setup(log):
    import logging,os,sys
    from logging.handlers import TimedRotatingFileHandler
    from cx_Oracle import SessionPool
    from configs.config import databases
    from utilities.secure.core import decrypt
    from modular_tariffs.src.configs import HOME
    db = databases['core']
    db_user = decrypt(db['username'])
    db_password = decrypt(db['password'])
    db_string = db['string']
    try:
        cwd = '%s/src/requests' % HOME
        resources = {}
        logger = logging.getLogger(log)
        logger.setLevel(logging.DEBUG)
        ch = TimedRotatingFileHandler('%s/logs/%s.log' %(cwd,log,),'midnight')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        resources['logger'] = logger
        resources['db_connection'] = SessionPool(db_user, db_password, db_string, 5, 100, 2, threaded=True)
    except Exception,e:
        logger.error(str(e))
        sys.exit(2)
    else:
        return resources

from daemon import Daemon

class Dequeue(Daemon):
    def __init__(self,pidfile):
        self.resources = None
        self.logger = None
        super(Dequeue,self).__init__(pidfile)

    def run(self):
        from tools import ThreadPool
        from modular_tariffs.src.configs import THREADS
        workers = THREADS['requests']
        self.resources = setup('log-modular-requests')
        self.logger = self.resources['logger']
        self.db_connection = self.resources['db_connection']
        pool = ThreadPool(workers, self.logger)
        self.logger.info('adding workers to pool')
        for i in range(1,(workers+1)):
            pool.add_task(Consumer(i,self.resources).consume)
        try:
            self.logger.info('added threads to pool')
            pool.wait_completion()
        except Exception,e:
            self.logger.error('died')

if __name__ == '__main__':
    import sys
    from modular_tariffs.src.configs import HOME
    cwd = '%s/src/requests' % HOME
    daemon = Dequeue('%s/requests_consumer.pid' %(cwd))
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print 'dequeue daemon starting ....'
            daemon.start()
        elif 'stop' == sys.argv[1]:
            print 'dequeue daemon stopping .....'
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            print 'dequeue daemon restarting ....'
            daemon.restart()
        else:
            print "unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" %sys.argv[0]
        sys.exit(2)

