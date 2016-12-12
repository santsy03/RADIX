#!/usr/bin/env python
'''
consumer for the provisioning renewal service

'''
from mg_auto_renewal.src.configs.config import QUEUES as queues
from mg_auto_renewal.src.lib.custom_loggers import daemon_logger
from mg_auto_renewal.src.configs.config import RENW_CWD
from mg_auto_renewal.src.configs.config import RENEWAL_LOG_NAME
from mg_auto_renewal.src.configs.config import RENEWAL_LOG_FOLDER
from mg_auto_renewal.src.configs.config import RENEWAL_PID_FILE
from mg_auto_renewal.src.configs.config import ROUTING_KEY
from mg_auto_renewal.src.lib.core import process_renewal_response
from mg_auto_renewal.src.configs.config import DEBUG
from mg_auto_renewal.src.consumer.daemon import Daemon
from data_provisioning.src.configs.core import env
from data_provisioning.src.configs.core import current


import pika
import traceback


class Consumer(object):
    def __init__(self, _id, _lg):
        self.channel = None
        self.response = None
        self.consumer_id = 'thread:%d' % (_id)
        self.logger = _lg
        if current == 'dev':
            self.queue = queues['renewal']['test']
        else:
            self.queue = queues['renewal']['prod']
        self.exchange = env[current]['exchange']
        self.key = ROUTING_KEY


    def handle_delivery(self, channel, method, header, body):
        try:
            import traceback
            process_renewal_response(body, self.logger)
        except Exception, err:
            self.logger.error(str(err))
            self.logger.error(traceback.format_exc())
        else:
            pass
        finally:
            channel.basic_ack(method.delivery_tag)

    def on_queue_declared(self, frame):
        self.channel.queue_bind(callback = self.on_queue_bound, \
                queue = self.queue, \
                exchange = self.exchange, \
                routing_key = self.key)

    def on_queue_bound(self, frame):
        self.logger.debug('... declaring queue')
        self.channel.basic_qos(prefetch_count =1)
        try:
            self.channel.basic_consume(self.handle_delivery,\
                    queue = self.queue)
        except Exception,e:
            self.logger.error('crashing')


    def on_channel_open(self, channel):
        self.channel = channel
        try:
            self.channel.queue_declare(queue = self.queue, \
                    exclusive = False, durable = True, \
                    auto_delete=False, callback = \
                    self.on_queue_declared)
        except Exception, err:
            self.logger.error(str(err))

    def on_connected(self, connection):
        connection.channel(self.on_channel_open)

    def consume(self,):
        try:
            from pika.adapters import SelectConnection
            credentials = pika.PlainCredentials('rabbitmg', 'mgrabbituser')
            v_host = 'data'
            self.connection = SelectConnection(pika.ConnectionParameters(\
                    host='127.0.0.1', \
                    port = 5672, \
                    virtual_host = v_host, \
                    credentials = credentials), \
                    self.on_connected)

            self.connection.ioloop.start()
        except Exception, err:
            self.connection.close()
            self.connection.ioloop.start()
        else:
            pass



class Dequeue(Daemon):
    def __init__(self, pidfile):
        self.logger = daemon_logger(RENW_CWD, RENEWAL_LOG_FOLDER, RENEWAL_LOG_NAME)
        super(Dequeue, self).__init__(pidfile)

    def run(self):
        from mg_auto_renewal.src.consumer.tools import ThreadPool
        from mg_auto_renewal.src.configs.config import WORKERS as workers

        pool = ThreadPool(workers, self.logger)

        self.logger.info('adding workers to pool')

        for i in range(1, (workers + 1)):
            pool.add_task(Consumer(i, self.logger).consume)
        try:
            self.logger.info('added threads to pool')
            pool.wait_completion()
        except Exception, err:
            self.logger.error('died')

if __name__ == '__main__':
    import sys
    RENEWAL_PID_FILE = str(RENEWAL_PID_FILE)
    daemon = Dequeue(RENEWAL_PID_FILE)
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
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

