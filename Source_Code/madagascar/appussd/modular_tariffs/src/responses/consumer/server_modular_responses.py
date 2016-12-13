#!/usr/bin/env python
import pika
from daemon import Daemon
from threading import Thread
from pika.adapters import SelectConnection
from logging.handlers import TimedRotatingFileHandler


import logging,os,sys
from cx_Oracle import SessionPool
from configs.config import databases
from utilities.secure.core import decrypt
from modular_tariffs.src.configs import HOME
from utilities.common.core import verify_params
from logging.handlers import TimedRotatingFileHandler

import datetime
from datetime import datetime as dt
from utilities.logging.core import log
from modular_tariffs.src.configs import QUEUES
from modular_tariffs.src.responses.consumer.core import process_provision_response

class Consumer(object):
    def __init__(self,id,resources):
        queue_name = QUEUES['modular_responses']
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
            resources = self.resources

            msg = str(body).strip()
            resources['logger'] = self.logger
            resources['db_connection'] = self.db_connection
            resources['connections'] = self.db_connection
            resources['parameters'] = eval(msg)
            parameters = resources['parameters']
            verify_params(resources['parameters'],
                    ['msisdn','packageId','status','transactionId','name',
                        'transaction_type','b_msisdn', 'args', 'expiry'], 
                    logger=resources['logger'])
	    
            package_requested, \
                    parameters['modular_id'], \
                    parameters['renew'], \
                    parameters['da_id'], \
                    parameters['channel'], \
                    parameters['category'], \
                    parameters['mix'] = \
                    parameters['args'].split('|')


            parameters['package_requested'] = str(package_requested).replace('/','')

            resources['parameters'] = parameters
            start = dt.now()
            log(resources, resources['parameters'], 'debug')
            process_provision_response(resources)
            duration ='Duration: %s' % str(dt.now() - start)
            response = 'Processed || %s || %s' % (str(message),  str(duration))
            resources['logger'].info(response)
        except Exception,e:
            try:
            	log(resources, 'operation:handleDelivery,status:failed to process_provision_response, msg: %s, error: %s' % ( 
                    message,str(e),), error=True)
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
    '''defines resources
    - adds a logger and a db connection to resources
    '''
    db = databases['core']
    db_user = decrypt(db['username'])
    db_password = decrypt(db['password'])
    db_string = db['string']
    try:
        cwd = '%s/src/responses/consumer' % HOME
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


class Dequeue(Daemon):
    def __init__(self,pidfile):
        self.resources = None
        self.logger = None
        super(Dequeue,self).__init__(pidfile)

    def run(self):
        from tools import ThreadPool
        from modular_tariffs.src.configs import THREADS
        workers = THREADS['responses']['consumer']
        self.resources = setup('log-modular-responses')
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
    from modular_tariffs.src.configs import HOME
    cwd = '%s/src/responses/consumer' % HOME
    daemon = Dequeue('%s/responses_consumer.pid' %(cwd))
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

