from data_provisioning.src.configs.core import web_services_port
#from data_provisioning.src.configs.core import web_services_port

HOST_NAME = __import__('socket').gethostname()

CURRENT = 'prod'

###### twistd conf
twisted = {}

prod = {}
prod['PORT'] = 7867
prod['THREADS'] = 100
prod['LOGS'] = 'logs'
prod['LOG_NAME'] = 'device_services-{}.log'.format(HOST_NAME)

dev = {}
dev['PORT'] = 7867
dev['THREADS'] = 100
dev['LOGS'] = 'logs'
dev['LOG_NAME'] = 'device_services-{}.log'.format(HOST_NAME)

twisted['prod'] = prod
twisted['dev'] = dev
#############


#### Queues and exchange config

queues = {}

dev = {}
dev['routing_key'] ='device.route'
dev['exchange'] = 'prod_data_exchange'
dev['queue'] = 'mdg_device'
dev['workers'] = 3

prod = {}
prod['routing_key'] ='device.route'
prod['exchange'] = 'prod_data_exchange'
prod['queue'] = 'mdg_device'
prod['workers'] = 20

queues['prod'] = prod
queues['dev'] = dev
########################################

### daemon config
daemon = {}

dev = {}
dev['home'] = '/appussd/mdg_devices/src/daemon'
dev['log_directory'] = dev['home']+'/logs'
dev['log_name'] = 'log_mdg_devices_daemon-{}.log'.format(HOST_NAME)

prod = {}
prod['home'] = '/appussd/mdg_devices/src/daemon'
prod['log_directory'] = prod['home'] + '/logs'
prod['log_name'] = 'log_mdg_devices_daemon-{}.log'.format(HOST_NAME)

daemon['dev'] = dev
daemon['prod'] = prod
###########################################

DAEMON = daemon[CURRENT]
QUEUES = queues[CURRENT]
TWISTED = twisted[CURRENT]

PROVISION_URL = "http://127.0.0.1:%s/submitProvision?" % str(web_services_port)
AUTH_KEY = 'mdg_devices'
ACCOUNT_ID = 'mdg_devices'

RANGE = {}
RANGE['MID'] = {'package_id':238,'validity':'7'}
RANGE['ENTRY'] = {'package_id':237,'validity':'7'}
RANGE['HIGH'] = {'package_id':239,'validity':'15'}

IMEI_SOURCE = 'EMA'
