import sys
from time import sleep
import logging
from logging.handlers import TimedRotatingFileHandler
from utilities.common.daemon import Daemon
from utilities.logging.core import log
from events.config import GENERATOR
from events.core.core import setup as a_setup
from events.core.core import process_events


HOST_NAME = __import__('socket').gethostname()


def setup():
    resources = {}
    log_directory = GENERATOR['log_directory']
    log_name = GENERATOR['log_name']
    log_level = GENERATOR['log_level']
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)
    ch = TimedRotatingFileHandler('%s/%s' %(log_directory, log_name), 'midnight')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    resources['logger'] = logger
    resources = a_setup(resources)
    return resources

class Events_Generator(Daemon):
    def run(self):
        try:
            resources = setup()
            info = 'event generator started ....'
            log(resources, info)
            while True:
                try:
                    process_events(resources)
                except Exception, err:
                    error = 'operation:Events_Enqueue_Daemon, status:fail, error:%s' %(str(err),)
                    log(resources, error, 'error')
                finally:
                    sleep(30)

        except Exception, err:
            error = 'operation:Events_Enqueue_Daemon, status:fail, error:%s' %(str(err),)
            log(resources, error, 'error')
                

if __name__ == '__main__':

    application_location = GENERATOR['home']
    generator = Events_Generator('%s/daemon-%s.pid' %(application_location, HOST_NAME))
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print ('events generator starting ....')
            generator.start()
        elif 'stop' == sys.argv[1]:
            print ('events generator stopping .....')
            generator.stop()
        elif 'restart' == sys.argv[1]:
            print ('events generator restarting ....')
            generator.restart()
        else:
            print "unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" %sys.argv[0]
        sys.exit(2) 
