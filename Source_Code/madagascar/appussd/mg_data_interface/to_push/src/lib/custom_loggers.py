
"""
module that defines custom loggers
logging for dameons and for twistd services
 
"""
from logging.handlers import TimedRotatingFileHandler
from mg_data_interface.src.configs.config import DEBUG as debug
import logging, os, sys

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

def daemon_logger(cwd, log_name):
    try:
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)
        handler = TimedRotatingFileHandler('%s/logs/%s.log' %(cwd,log_name,),'midnight')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    except Exception, err:
        raise err
    else:
        return logger

