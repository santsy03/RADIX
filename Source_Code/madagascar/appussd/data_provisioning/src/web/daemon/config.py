queueName= 'provision_response'
home = '/usr/local/test/data_provisioning/src/web/daemon'
workers = 5

current = 'dev'
env = {}
env['prod'] = {}
env['prod']['home'] = '/usr/local/data_provisioning/src/web/daemon'
env['prod']['queueName'] = 'prod_provision_response'
env['prod']['workers'] = 10


env['dev'] =  {}
env['dev']['home'] = '/usr/local/data_provisioning/src/web/daemon'
env['dev']['queueName'] = 'dev_provision_response'
env['dev']['workers'] = 10
