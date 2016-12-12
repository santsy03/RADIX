
"""
module that defines custom loggers
logging for dameons and for twistd services
 
"""
from logging.handlers import TimedRotatingFileHandler
from mg_auto_renewal.src.configs.config import DEBUG as debug
import logging

def twistd_logger(level, info):
    '''
    twistd  makes logging easy it logs all print statements
    this wraps around print to introduce
    logging levels
    '''
    if debug:
        print level+"::"+" "+info
    else:
        if level == 'INFO' or level == 'ERROR' or level == 'CRITICAL':
            print level+"::"+" "+info

def daemon_logger(cwd, folder, log_name):
    '''
    creates a daemon to be used in a logger
    '''
    try:
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)
        handler = TimedRotatingFileHandler('%s/%s/%s.log' %(cwd, folder, log_name,),'midnight')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    except Exception, err:
        raise err
    else:
        return logger


