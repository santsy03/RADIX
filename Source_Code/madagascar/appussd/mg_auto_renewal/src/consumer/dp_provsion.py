#!/usr/bin/env python
'''
consumer for the provisioning renewal service

'''
from mg_auto_renewal.src.configs.config import QUEUES as queues
from mg_auto_renewal.src.lib.custom_loggers import daemon_logger
from mg_auto_renewal.src.configs.config import CWD
from mg_auto_renewal.src.configs.config import LOG_NAME
from mg_auto_renewal.src.configs.config import LOG_FOLDER
from mg_auto_renewal.src.lib.core import process_provision_request 
from mg_auto_renewal.src.configs.config import PID_FILE
from mg_auto_renewal.src.configs.config import DEBUG
from mg_auto_renewal.src.consumer.daemon import Daemon
import pika
import ast
import traceback


class Consumer(object):
    def __init__(self, _id, _lg):
        self.channel = None
        self.response = None
        self.consumer_id = 'thread:%d' % (_id)
        self.logger = _lg
        if DEBUG:
            self.queue = queues['internal']['test']
        else:
            self.queue = queues['internal']['prod']

    def handle_delivery(self, channel, method, header, body):

        try:
            parameters = ast.literal_eval(body)
            self.logger.info(parameters)
            try:
                response = process_provision_request(parameters, \
                        self.logger)
            except Exception, err:
                self.logger.error(str(err))
            else:
                self.logger.info(response)
        except Exception, err:
            self.logger.error(str(err))
            self.logger.error(traceback.format_exc())

    def on_queue_declared(self, frame):
        self.logger.debug('... declaring queue')
        self.channel.basic_qos(prefetch_count = 1)
        try:
            self.channel.basic_consume(self.handle_delivery, \
                    queue = self.queue,no_ack=True)
        except Exception, err:
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
            self.connection = SelectConnection(pika.ConnectionParameters\
                    (host='127.0.0.1'), 
                    self.on_connected)
            self.connection.ioloop.start()
        except Exception, err:
            self.connection.close()
            self.connection.ioloop.start()
        else:
            pass


class Dequeue(Daemon):
    def __init__(self, pidfile):
        self.logger = daemon_logger(CWD, LOG_FOLDER, LOG_NAME)
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
    print type(PID_FILE)
    PID_FILE = str(PID_FILE)
    daemon = Dequeue(PID_FILE)
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

