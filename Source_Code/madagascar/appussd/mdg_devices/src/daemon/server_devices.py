#!/usr/bin/python
import sys, pika
import json
import traceback

from ast import literal_eval
from time import time

from mdg_devices.src.configs.general import QUEUES, DAEMON
from mdg_devices.src.common.core import process_requests, setup as db_setup
from mdg_devices.src.daemon.daemon import Daemon
from mdg_devices.src.daemon.tools import ThreadPool

HOST_NAME = __import__('socket').gethostname()

def setup():
    from logging.handlers import TimedRotatingFileHandler
    import logging, os, sys
    resources = {}
    log_level = logging.DEBUG
    logger = logging.getLogger(DAEMON['log_name'])
    logger.setLevel(log_level)
    log_file = '%s/%s' %(DAEMON['log_directory'],
                    DAEMON['log_name'])
    ch = TimedRotatingFileHandler(log_file,'midnight')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    resources['logger'] = logger
    resources['con'] = db_setup()
    return resources

class Consumer(object):
    def __init__(self, thread_id,resources, queue_name):
        self.channel = None
        self.response = None
        self.consumerId = 'thread:%d' %(thread_id,)
        self.logger = resources['logger']
        self.queue = queue_name
        self.resources = resources
        self.key = QUEUES['routing_key']
        self.exchange = QUEUES['exchange']

    def handle_delivery(self,channel,method,header,body):
        start = time()
        message = json.loads(eval(body))
        try:
            cdr = 'NEW REQUEST: %s' % message
            self.logger.info(cdr)
            parameters = {}
            resources = {}
            resources['parameters'] = parameters
            resources['logger'] = self.logger
            resources['parameters']['message'] = message
            resources['parameters']['connection'] = self.resources['con']
            resources = process_requests(resources)
        except Exception, err:
            try:
                self.logger.error("operation : handleDelivery, status:failed "
                        "to processRequest payload: %s, error:%s" %( 
                            message,str(err),))
                self.logger.error(traceback.format_exc())
            except Exception:
                pass
        else:
            channel.basic_ack(method.delivery_tag)
        stop = time()
        diff = stop - start
        cdr = 'REQUEST TOOK %s seconds to handle %s' % (str(diff),
                str(message))
        self.logger.info(cdr)

    def on_queue_declared(self, frame):
        self.channel.queue_bind(callback = self.on_queue_bound, 
                queue = self.queue, 
                exchange = self.exchange, 
                routing_key = self.key)

    def on_queue_bound(self, frame):
        self.logger.debug('... declaring queue')
        self.channel.basic_qos(prefetch_count =1)
        try:
            self.channel.basic_consume(self.handle_delivery,\
                    queue = self.queue)
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
            credentials = pika.PlainCredentials('rabbitmg', 'mgrabbituser')
            #credentials = pika.PlainCredentials('guest', 'guest')
            v_host = 'data'
            self.connection = SelectConnection(pika.ConnectionParameters(\
                    host='127.0.0.1', \
                    port = 5672, \
                    virtual_host = v_host, \
                    credentials = credentials), \
                    self.on_connected)
            self.connection.ioloop.start()
        except Exception,e:
            self.connection.close()
            self.connection.ioloop.start()
        else:
            pass

class Callbacks_Consumer(Daemon):
    def __init__(self, pid_file):
        self.resources = None
        self.logger = None
        super(Callbacks_Consumer,self).__init__(pid_file)

    def run(self):
        try:
            self.resources = setup()
            self.logger = self.resources['logger']
            info = 'callbacks consumer started ....'
            self.logger.info(info)
            workers = QUEUES['workers']
            pool = ThreadPool(workers, self.logger)
            for i in range(1, workers+1):
                pool.add_task(Consumer(i,self.resources, QUEUES['queue']).consume)
            try:
                self.logger.info('... callbacks consumer working')
                pool.wait_completion()
            except Exception, err:
                error = 'died dead %s' %str(err)
                self.logger.debug(error)

        except Exception, err:
            error = 'operation:Callbacks_Consumer_Daemon, status:fail, error:%s' %(str(err),)
            self.logger.debug(error)
                
if __name__ == '__main__':
    application_location = DAEMON['home']
    pid_file = '%s/daemon-%s.pid' % (application_location, HOST_NAME)
    consumer = Callbacks_Consumer(pid_file)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print ('callbacks consumer starting ....')
            consumer.start()
        elif 'stop' == sys.argv[1]:
            print ('callbacks consumer stopping .....')
            consumer.stop()
        elif 'restart' == sys.argv[1]:
            print ('callbacks consumer restarting ....')
            consumer.restart()
        else:
            print "unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" %sys.argv[0]
        sys.exit(2) 
