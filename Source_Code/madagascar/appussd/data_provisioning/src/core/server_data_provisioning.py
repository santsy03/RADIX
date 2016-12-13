#!/usr/bin/env python
import pika
from threading import Thread
from pika.adapters import SelectConnection
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from daemon import Daemon
from utilities.logging.core import log
from kombu.pools import producers
from kombu import Connection

HOST_NAME = __import__('socket').gethostname()

class Consumer(object):
    def __init__(self,id,resources):
        from data_provisioning.src.configs.core import queues, exchange
        self.channel = None
        self.response = None
        self.consumerId = 'thread:%d' %(id,)
        self.logger = resources['logger']
        self.queue = queues['core']
        self.resources = resources
        self.exchange = exchange

    def send_delivery(self, resources, routing_key, msg):
        producer = resources['producers'].acquire( block=True)
        producer.publish(msg,
                exchange = self.exchange,
                serializer = 'json',
                routing_key = routing_key)
        resources['producers'].release(producer)


    def handle_delivery(self,channel,method,header,body):
        from data_provisioning.src.core.core import processRequest
        from data_provisioning.src.configs.core import status
        import ast
        import traceback
        from json import dumps
        self.logger.debug(str(body.strip()))
        try:
            from datetime import datetime
            message = str(body).strip()
            message = ast.literal_eval(message)
            self.logger.info(str(message))
            message['args'] = ast.literal_eval(message['args'])

            routing_key = (message['args'])['routing_key']
            
            resources = {}
            resources['connections'] = self.resources['connections']
            resources['logger'] = self.logger
            resources['producers'] = self.resources['producers']
            parameters = {}
            parameters['msisdn']= message['msisdn']
            parameters['packageId'] = message['package_id']
            parameters['transactionId'] = message['transaction_id']
            parameters['args'] = message['args']
            parameters['b_msisdn'] = message['b_msisdn']
            parameters['transaction_type'] = message['transaction_type']
            if 'external_Data1' in message:
                parameters['external_Data1'] = message['external_Data1']
            if 'external_Data2' in message:
                parameters['external_Data2'] = message['external_Data2']

            response = {}
            response['msisdn'] = message['msisdn']
            response['name'] = "False"
            response['status'] = status['error']
            response['packageId'] = message['package_id']
            response['package_id'] = message['package_id']
            response['transaction_type'] = message['transaction_type']
            response['transactionId'] = message['transaction_id']
            response['balance'] = {}

            resources['parameters'] = parameters

            response = processRequest(resources)
            log(resources, str(response), 'info')
            start = datetime.now()
            duration = datetime.now()- start

        except Exception, err:
            error2 = traceback.format_exc()
            self.logger.error(error2)
            try:
                response = dumps(response)
                self.send_delivery(resources, routing_key, response)
                info = "sent response %s || key %s" % (str(response), str(routing_key))
                self.logger.info(info)
            except Exception, err:
                self.logger.error(traceback.format_exc())
                self.logger.error(str(err))
        else:
            try:
                self.send_delivery(resources, routing_key, response)
                info = "sent response %s || key %s" % (str(response), str(routing_key))
                self.logger.info(info)
            except Exception, err:
                self.logger.error(traceback.format_exc())
                self.logger.error(str(err))
        finally:
                channel.basic_ack(method.delivery_tag)


    def on_queue_declared(self,frame):
        self.logger.debug('... declaring queue')
        self.channel.basic_qos(prefetch_count =1)
        try:
            self.channel.basic_consume(self.handle_delivery,queue=self.queue)
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
    from DBUtils.PooledDB import PooledDB
    try:
        from utilities.secure.core import decrypt
        from configs.config import databases
        from data_provisioning.src.configs.core import home
        import cx_Oracle
        resources = {}

        pool = PooledDB(
                cx_Oracle,
                maxcached = 5,
                maxconnections = 300,
                user = decrypt(databases['core']['username']),
                password = decrypt(databases['core']['password']),
                dsn = databases['core']['string'],
                threaded = True
                )
        pool.timeout = 300
        resources['connections'] = pool
        cwd = '%s/core/' % home
        logger = logging.getLogger(log)
        logger.setLevel(logging.DEBUG)
        ch = TimedRotatingFileHandler('%s/logs/%s-%s.log' %(cwd, log, HOST_NAME),
                                      'midnight')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        resources['logger'] = logger
    except Exception,e:
        logger.error(str(e))
        sys.exit(2)
    else:
        return resources



class Dequeue(Daemon):
    def __init__(self,pidfile):
        self.resources = None
        self.logger = None
        self.producers = self.get_connections() 
        super(Dequeue,self).__init__(pidfile)

   
    def get_connections(self):
        connection = Connection('amqp://rabbitmg:mgrabbituser@localhost:5672/data')
        producer_pool = producers[connection]
        return producer_pool

    def run(self):
        from data_provisioning.src.core.tools import ThreadPool
        from data_provisioning.src.configs.core import workers

        self.resources = setup('log-data-provisioning')
        #self.resources = res #setup('log-data-provisioning')
        self.logger = self.resources['logger']
        print "logger done"
        self.resources['producers'] = self.producers
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
    from data_provisioning.src.configs.core import home
    daemon = Dequeue('%s/core/dequeue-%s.pid' %(home, HOST_NAME))
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

