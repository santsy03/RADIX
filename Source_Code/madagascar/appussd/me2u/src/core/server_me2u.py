#!/usr/bin/env python
import pika
from threading import Thread
from pika.adapters import SelectConnection
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from me2u.src.common import verify_params
from me2u.src.common import log
from utilities.metrics.core import send_metric
from me2u.src.config import METRICS

from datetime import datetime as dt
import datetime
from me2u.src.core.core import process_request

class Consumer(object):
    def __init__(self,id,resources):
        from me2u.src.config import QUEUES
        queue_name = QUEUES['core']
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
            message = eval(body)
            verify_params(message, ['msisdn', 'recipient', 'amount'])
            resources = {}
            resources['logger'] = self.logger
            resources['db_connection'] = self.db_connection
            resources['parameters'] = message
            start = dt.now()
            resp = process_request(resources)
            mtrcs = {'name_space':METRICS['core_resp_time'],
                    'start_time':start}
            send_metric(mtrcs, 'timer')
            del(mtrcs)
            duration ='Duration: %s' % str(dt.now() - start)
            response = 'Processed: %s -- %s -- %s' % (str(body), str(resp), str(duration))
            log(resources, response)
        except Exception,e:
            try:
            	self.logger.error('operation:handle_delivery,status:failed to processRequest,command:%s,error:%s' % ( 
                    message,str(e),))
            except Exception:
                pass
            raise e

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
    from utilities.secure.core import decrypt
    from cx_Oracle import SessionPool
    from me2u.src.config import HOME as cwd
    from me2u.src.config import DATABASES as db
    try:
        resources = {}
        logger = logging.getLogger(log)
        logger.setLevel(logging.DEBUG)
        ch = TimedRotatingFileHandler('%s/core/logs/%s.log' %(cwd,log,),'midnight')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        db_user = decrypt(db['username'])
        db_password = decrypt(db['password'])
        db_string = db['string']
        db_connection = SessionPool(db_user, db_password, db_string, 10, 200, 5, threaded=True)
        resources['logger'] = logger
        resources['db_connection'] = db_connection
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
        from me2u.src.config import THREADS
        workers = THREADS['core']
        self.resources = setup('log-me2u-core')
        self.logger = self.resources['logger']
        self.db_connection = self.resources['db_connection']
        pool = ThreadPool(workers,self.logger)
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
    from me2u.src.config import HOME as home
    daemon = Dequeue('%s/core/me2u_core.pid' %(home))
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

