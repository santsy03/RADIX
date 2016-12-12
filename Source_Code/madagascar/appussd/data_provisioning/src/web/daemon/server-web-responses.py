#!/usr/bin/env python
import pika
from threading import Thread
from pika.adapters import SelectConnection
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from data_provisioning.src.configs.core import da_factor
#import pdb
import ast
import json

HOST_NAME = __import__('socket').gethostname()

class Consumer(object):
    def __init__(self,id,resources):
        from data_provisioning.src.configs.core import queues, exchange
        self.connection = None
        self.channel = None
        self.response = None
        self.consumerId = 'thread:%d' %(id,)
        self.logger = resources['logger']
        self.resources = resources
        self.queue = queues['web']
        self.exchange = exchange
        self.key = '#'

    def handle_delivery(self,channel,method,header,body):
        try:
            import traceback
            from datetime import datetime
            from data_provisioning.src.web.daemon.core import processRequest
            message = str(body).strip()
            message = ast.literal_eval(message)
            self.logger.info(message)
            message = json.loads(message)

            volume = ""
            expiry = ""
            status = str(message['status'])
            if 'volume' in message['balance']:
                volume = str(message['balance']['volume']['amount'])
                expiry = str(message ['balance']['volume']['expiry'])
                expiry = expiry.split('T')[0]

            elif 'meg_15' in message['balance']:
                volume = str(message['balance']['meg_15']['amount'])
                expiry = str(message ['balance']['meg_15']['expiry'])
                expiry = expiry.split('T')[0]

            elif 'telescopic' in message['balance']:
                volume = str(message['balance']['telescopic']['amount'])
                expiry = str(message ['balance']['telescopic']['expiry'])
                expiry = expiry.split('T')[0]

            elif 'regional' in message['balance']:
                volume = str(message['balance']['regional']['amount'])
                expiry = str(message ['balance']['regional']['expiry'])
                expiry = expiry.split('T')[0]

            elif 'unlimited' in message['balance']:
                volume = str(message['balance']['unlimited']['amount'])
                expiry = str(message ['balance']['unlimited']['expiry'])
                expiry = expiry.split('T')[0]

            elif 'router' in message['balance']:
                volume = str(message['balance']['router']['amount'])
                expiry = str(message ['balance']['router']['expiry'])
                expiry = expiry.split('T')[0]

            else:
                volume = str(0)
                expiry = "False"

            name = message['name']
            trans_id = str(message['transactionId'])

            resources = {}
            resources['connections'] = self.resources['connections']
            resources['logger'] = self.resources['logger']
            parameters = {}
            parameters['transactionId'],parameters['status'],\
                    parameters['volume'],parameters['expiry'],parameters['name'] = trans_id,status,volume, expiry, name

            resp = [status,expiry,volume, name, trans_id]
            resp = "||".join(resp)
            self.logger.info(resp)

            parameters['response'] = resp
            parameters['balance_response'] = str(message['balance'])

            resources['parameters'] = parameters
            results = processRequest(resources)
            start = datetime.now()
            duration = datetime.now()- start
        except Exception, e:
            self.logger.error('operation:handleDelivery,status:failed to processRequest,command:%s,error:%s' %(message,str(e),))
            self.logger.error(traceback.format_exc())
        else:
            self.logger.info("process request completed for %s" % (str(message)))

        finally:
             channel.basic_ack(delivery_tag = method.delivery_tag)

    def on_queue_declared(self, frame):
        self.channel.queue_bind(callback = self.on_queue_bound,
                queue = self.queue,
                exchange = self.exchange,
                routing_key = self.key)

    def on_queue_bound(self,frame):
        self.logger.debug('... declaring queue')
        self.channel.basic_qos(prefetch_count =1)
        try:
            self.channel.basic_consume(self.handle_delivery,queue=self.queue)
        except Exception,e:
            self.logger.error('crashing')

    def on_channel_open(self,channel):
        self.channel = channel
        try:
            self.channel.queue_declare(queue=self.queue,
                    exclusive=False,
                    durable=True,
                    auto_delete=False,
                    callback=self.on_queue_declared)
        except Exception,e:
            logger.error(str(e),)

    def on_connected(self,connection):
        connection.channel(self.on_channel_open)

    def consume(self,):
        try:
            from pika.adapters import SelectConnection
            from pika import PlainCredentials
            vhost = 'data'
            credentials = PlainCredentials('rabbitmg', 'mgrabbituser')
            self.connection = SelectConnection(
                    pika.ConnectionParameters(host='127.0.0.1', 
                virtual_host = vhost,
                credentials = credentials) 
                    ,self.on_connected)
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
    import cx_Oracle
    from DBUtils.PooledDB import PooledDB
    try:
        from configs.config import databases
        from data_provisioning.src.configs.core import home
        from utilities.secure.core import decrypt
        cwd = '%s/web/daemon' % home
        logger = logging.getLogger(log)
        logger.setLevel(logging.DEBUG)
        ch = TimedRotatingFileHandler('%s/logs/%s-%s.log' % (cwd, log, HOST_NAME),
                                      'midnight')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        resources = {}
        resources['logger'] = logger
        core = databases['core']
        resources['connections'] =PooledDB(
                cx_Oracle,
                maxcached = 5,
                maxconnections = 300,
                user = decrypt(databases['core']['username']),
                password = decrypt(databases['core']['password']),
                dsn = databases['core']['string'],
                threaded = True
                )
        resources['connections'].timeout = 300
    except Exception,e:
        print str(e)
    else:
        return resources

from data_provisioning.src.web.daemon.daemon import Daemon

class Dequeue(Daemon):
    def __init__(self,pidfile):
        self.resources = None
        self.logger = None
        super(Dequeue,self).__init__(pidfile)

    def run(self):
        try:
            from data_provisioning.src.web.daemon.tools import ThreadPool
            from data_provisioning.src.configs.core import workers
            self.resources = setup('log-web-responses')
            self.logger = self.resources['logger']
            self.logger.info('adding %s workers to pool' %str(workers))
            pool = ThreadPool(workers,self.logger)
            for i in range(1,(workers+1)):
                pool.add_task(Consumer(i,self.resources).consume)
            try:
                self.logger.info('added threads to pool')
                pool.wait_completion()
            except Exception,e:
                self.logger.error('died')
        except Exception, err:
            raise err

if __name__ == '__main__':
    import sys
    from data_provisioning.src.configs.core import home
    daemon = Dequeue('%s/web/daemon/dequeue-%s.pid' %(home, HOST_NAME))
    print "init"
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

