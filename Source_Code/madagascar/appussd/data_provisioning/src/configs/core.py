current = 'prod'
country_code = '261'

da_factor = 100
#length of msisdn without country code
msisdn_length = 9

debug = True
units = {}
units['kb']='KB'
units['mb']='MB'
units['gb']='GB'

#start - response codes
status = {}
status['queued'] = '0'
status['missingParameters'] = '1'
status['authenticationFailed'] = '2'
status['error'] = '3'
status['invalidPackageId'] = '4'
status['successfullyProvisioned'] = '5'
status['packageConflict'] = '6'
status['insufficientFunds'] = '7'
status['invalidTransactionId'] = '8'
status['isBarred'] = '9'
status['time_restriction'] = '10'
status['exceed_sub_limit'] = '11'
status['isBarred_MyMeg5'] = '12'
status['not_whitelisted'] = '13'
status['voice_time_restriction'] = '14'
status['Undefined_refill_error'] = '15'
status['IN_defined_refill_error'] = '16'

#end - response codes

#start - status messages
statusMsgs = {}
statusMsgs['0'] = 'queued'
statusMsgs['1'] = 'missing parameters'
statusMsgs['2'] = 'authentication failed'
statusMsgs['3'] = 'error'
statusMsgs['4'] = 'invalid package id'
statusMsgs['5'] = 'success'
statusMsgs['6'] = 'package conflict'
statusMsgs['7'] = 'insufficient funds'
statusMsgs['8'] = 'invalid transactionId'
statusMsgs['9'] = 'is barred'
statusMsgs['10'] = 'time restriction violated'
statusMsgs['11'] = 'exceeded subscription limit'
statusMsgs['12'] = 'is barred MyMeg5'
statusMsgs['13'] = 'not whitelisted'
statusMsgs['14'] = 'beyond subscription time'
statusMsgs['15'] = 'Undefined refill failure'
statusMsgs['16'] = 'Defined refill failure'

#end - status messages

# start - environment settings

#production environment
from configs.config import databases

env = {}
env['prod'] = {}
env['prod']['home'] = '/appussd/data_provisioning/src'
env['prod']['queues'] = {}
env['prod']['queues']['web'] = 'prod_provision_response'
env['prod']['queues']['core'] = 'prod_core_provisioning'
env['prod']['queueName'] = 'prod_provision_response'
env['prod']['workers'] = 60
env['prod']['databases'] = {}
env['prod']['databases']['core'] = {}
env['prod']['databases']['core']['username'] = databases['core']['username'] 
env['prod']['databases']['core']['password'] = databases['core']['password'] 
env['prod']['databases']['core']['string'] = databases['core']['string'] 
env['prod']['ports'] = {}
env['prod']['ports']['webServices'] = 9002
env['prod']['exchange'] = 'prod_data_exchange'

#development environment
env['dev'] =  {}
env['dev']['home'] = '/appussd/test/data_provisioning/src'
env['dev']['queues'] = {}
env['dev']['queues']['web'] = 'dev_provision_response'
env['dev']['queues']['core'] = 'dev_core_provisioning'
env['dev']['workers'] = 10
env['dev']['databases'] = {}
env['dev']['databases']['core'] = {}
env['dev']['databases']['core']['username'] = databases['core']['username']
env['dev']['databases']['core']['password'] = databases['core']['password']
env['dev']['databases']['core']['string'] = databases['core']['string']
env['dev']['ports'] = {}
env['dev']['ports']['webServices'] = 19002
env['dev']['exchange'] = 'test_data_exchange'


#end - environment settings

#start - database configurations
databases = {}
databases['core'] = env[current]['databases']['core']
#end - database configurations

#start - application location configuration
home = env[current]['home']
#end - application location configuration

#start - queues configuration
queues = {}
queues['web'] = env[current]['queues']['web']
queues['core'] = env[current]['queues']['core']
# end queues configuration

#start - workers configuration
workers = env[current]['workers']
#end - workers configuration

#start - web services port
web_services_port = env[current]['ports']['webServices']
#end web services port

#start - exchange
exchange = env[current]['exchange']



SPECIAL_PRICE_BUNDLES = {}
SPECIAL_PRICE_BUNDLES['16'] = 164700

