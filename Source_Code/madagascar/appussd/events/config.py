'''
Configuration file for events manager
'''
import logging
from configs.config import databases

HOST_NAME = __import__('socket').gethostname()

prod_username = databases['core']['username']
prod_password = databases['core']['password']
prod_string = databases['core']['string']

CURRENT = 'prod'

status = {}
status['queued'] = 2
status['scheduled'] = 0
status['processed'] = 1
status['disabled'] = 3
status['error'] = 4

ENV = {}

ENV['dev'] = {}
ENV['dev']['home'] = '/appussd/test'
ENV['dev']['database'] = {}
ENV['dev']['database']['user'] = prod_username
ENV['dev']['database']['password'] = prod_password
ENV['dev']['database']['connection_string'] = prod_string

ENV['dev']['generator'] = {}
ENV['dev']['generator']['home'] = '%s/events/daemons/generator' %ENV['dev']['home'] 
ENV['dev']['generator']['log_directory'] = '%s/logs' %ENV['dev']['generator']['home']
ENV['dev']['generator']['log_name'] = 'log-generator-{}.txt'.format(HOST_NAME)
ENV['dev']['generator']['log_level'] = logging.DEBUG

ENV['dev']['consumer'] = {}
ENV['dev']['consumer']['home'] = '%s/events/daemons/consumer' %ENV['dev']['home']
ENV['dev']['consumer']['log_directory'] = '%s/logs' %ENV['dev']['consumer']['home']
ENV['dev']['consumer']['log_name'] = 'log-consumer-{}.txt'.format(HOST_NAME)
ENV['dev']['consumer']['log_level'] = logging.DEBUG
ENV['dev']['consumer']['queue_name'] = 'events_queue_dev'
ENV['dev']['consumer']['workers'] = 4


ENV['prod'] = {}
ENV['prod']['home'] = '/appussd'
ENV['prod']['database'] = {}
ENV['prod']['database']['user'] = prod_username 
ENV['prod']['database']['password'] = prod_password
ENV['prod']['database']['connection_string'] = prod_string

ENV['prod']['generator'] = {}
ENV['prod']['generator']['home'] = '%s/events/daemons/generator' %ENV['prod']['home'] 
ENV['prod']['generator']['log_directory'] = '%s/logs' %ENV['prod']['generator']['home']
ENV['prod']['generator']['log_name'] = 'log-generator-{}.txt'.format(HOST_NAME)
ENV['prod']['generator']['log_level'] = logging.DEBUG

ENV['prod']['consumer'] = {}
ENV['prod']['consumer']['home'] = '%s/events/daemons/consumer' %ENV['prod']['home'] 
ENV['prod']['consumer']['log_directory'] = '%s/logs' %ENV['prod']['consumer']['home']
ENV['prod']['consumer']['log_name'] = 'log-consumer-{}.txt'.format(HOST_NAME)
ENV['prod']['consumer']['log_level'] = logging.DEBUG
ENV['prod']['consumer']['queue_name'] = 'events_queue_pro'
ENV['prod']['consumer']['workers'] = 4

DATABASE = ENV[CURRENT]['database']
GENERATOR = ENV[CURRENT]['generator']
CONSUMER = ENV[CURRENT]['consumer']
