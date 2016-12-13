import sys
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from utilities.common.daemon import Daemon
from utilities.logging.core import log
import pika
from pika.adapters import SelectConnection
from events.config import CONSUMER
from events.core.core import setup as a_setup
from events.common.tools import ThreadPool
from events.core.core import handle_event


HOST_NAME = __import__('socket').gethostname()


def setup():
    resources = {}
    log_directory = CONSUMER['log_directory']
    log_name = CONSUMER['log_name']
    log_level = CONSUMER['log_level']
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)
    ch = TimedRotatingFileHandler('%s/%s' %(log_directory, log_name), 'midnight')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    resources['logger'] = logger
    resources = a_setup(resources)
    return resources

class Consumer(object):
    def __init__(self, thread_id,resources, queue_name):
        self.channel = None
        self.response = None
        self.consumerId = 'thread:%d' %(thread_id,)
        self.logger = resources['logger']
        self.queue = queue_name
        self.resources = resources

    def handle_delivery(self,channel,method,header,body):
        try:
            message = str(body).strip()
            self.logger.info(message)
            resources = {}
            resources['connections'] = self.resources['connections']
            resources['logger'] = self.logger
            parameters = {}
            parameters['msg']= message
            resources['parameters'] = parameters
            try:
                handle_event(resources)
            except Exception, err:
                pass
            start = datetime.now()
            duration = datetime.now()- start
        except Exception,e:
            try:
                self.logger.error('operation:handleDelivery,status:failed to processRequest command:%s,error:%s' %( message,str(e),))
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
            self.logger.error(str(e),)

    def on_connected(self,connection):
        connection.channel(self.on_channel_open)

    def consume(self,):
        try:
            self.connection = SelectConnection(pika.ConnectionParameters(host='127.0.0.1'),self.on_connected)
            self.connection.ioloop.start()
        except Exception,e:
            self.connection.close()
            self.connection.ioloop.start()
        else:
            pass

class Events_Consumer(Daemon):
    def __init__(self, pid_file):
        self.resources = None
        self.logger = None
        super(Events_Consumer,self).__init__(pid_file)

    def run(self):
        try:
            self.resources = setup()
            self.logger = self.resources['logger']
            workers = CONSUMER['workers']
            info = 'event consumer started ....'
            log(self.resources, info)
            pool = ThreadPool(workers, self.logger)
            queue_name = CONSUMER['queue_name']
            for i in range(1, workers+1):
                pool.add_task(Consumer(i,self.resources, queue_name).consume)
            try:
                log(self.resources, '... events consumer working')
                pool.wait_completion()
            except Exception, err:
                error = 'died dead %s' %str(err)
                log(self.resources, error, 'error')

        except Exception, err:
            error = 'operation:Events_Consumer_Daemon, status:fail, error:%s' %(str(err),)
            log(self.resources, error, 'error')
                

if __name__ == '__main__':

    application_location = CONSUMER['home']
    consumer = Events_Consumer('%s/daemon-%s.pid' %(application_location, HOST_NAME))
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print ('events consumer starting ....')
            consumer.start()
        elif 'stop' == sys.argv[1]:
            print ('events consumer stopping .....')
            consumer.stop()
        elif 'restart' == sys.argv[1]:
            print ('events consumer restarting ....')
            consumer.restart()
        else:
            print "unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" %sys.argv[0]
        sys.exit(2) 
