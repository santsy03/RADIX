HOST_NAME = __import__('socket').gethostname()

current = 'prod'
service_name = 'authentication'

DEBUG = {}
DEBUG['prod'] = False
DEBUG['test'] = True

debug = DEBUG[current]

ENV = {}

ENV['prod'] = {}
ENV['test'] = {}

ENV['prod']['HOME'] = '/appussd/authentication'
ENV['test']['HOME'] = '/appussd/test/authentication'

HOME = ENV[current]['HOME']

ENV['prod']['PORTS'] = {}
ENV['prod']['PORTS']['http'] = 8005

ENV['test']['PORTS'] = {}
ENV['test']['PORTS']['http'] = 8006

ENV['prod']['DB'] = {}
ENV['prod']['DB']['pool'] = (5, 200, 5), {'threaded': True}

ENV['test']['DB'] = {}
ENV['test']['DB']['pool'] = (3, 30, 3), {'threaded': True}

ENV['prod']['THREADS'] = {}
ENV['prod']['THREADS']['http'] = 200

ENV['test']['THREADS'] = {}
ENV['test']['THREADS']['http'] = 20

ENV['prod']['LOGS'] = {}
ENV['prod']['LOGS']['http'] = '%s/logs/twistd-authentication-http-%s' % (HOME, HOST_NAME)
ENV['prod']['LOGS']['cdr'] = '%s/logs/cdr/cdr-authentication-%s' % (HOME, HOST_NAME)

ENV['test']['LOGS'] = {}
ENV['test']['LOGS']['http'] = '%s/logs/twistd-test-authentication-http' % HOME
ENV['test']['LOGS']['cdr'] = '%s/logs/cdr/cdr-authentication' % HOME


PORTS = {}
PORTS['http'] = ENV[current]['PORTS']['http']

THREADS = {}
THREADS['http'] = ENV[current]['THREADS']['http']

LOGS = {}
LOGS['http'] = ENV[current]['LOGS']['http']
LOGS['cdr'] = ENV[current]['LOGS']['cdr']
LOGS['when'] = dict(when = 'MIDNIGHT')  # log rollover interval
LOGS['cdr_format'] = '%(name)s | %(asctime)s | %(msecs)d | %(thread)d | %(message)s'

DB_POOL = ENV[current]['DB']['pool']

SQL = {}
SQL['table'] = 'USERS'
SQL['procedure'] = 'update_users'
SQL['fetch_password'] = '''SELECT PASSWORD FROM %s WHERE USERNAME = :username''' % SQL['table']
SQL['fetch_salt'] = 'SELECT SALT FROM %s WHERE USERNAME = :username' % SQL['table']
SQL['authenticate'] = 'SELECT ATTEMPTS, SALT, PASSWORD FROM %s WHERE USERNAME = :username' % SQL['table']
SQL['update_attempts'] = 'UPDATE %s SET ATTEMPTS = :attempts WHERE USERNAME = :username' % SQL['table']
SQL['reset_password'] = 'UPDATE %s SET ATTEMPTS = :attempts , PASSWORD = :default_password , SALT = :salt WHERE USERNAME = :username' % SQL['table']
SQL['unlock'] = 'UPDATE %s SET ATTEMPTS = :attempts WHERE USERNAME = :username' % SQL['table']

HTTP = {}
# API request and response parameters
HTTP['responses'] = {}
HTTP['responses']['success'] = '5'
HTTP['responses']['failure'] = '3'

HTTP['args'] = {}
# list of mandatory args for each http request type
HTTP['args']['authenticate'] = ['username', 'password', 'channel']
HTTP['args']['change_password'] = ['username', 'current_password', 'new_password', 'channel']
HTTP['args']['unlock'] = ['username', 'channel']
HTTP['args']['reset'] = ['username', 'channel']
HTTP['args']['create_user'] = ['username', 'channel']

HTTP['pages'] = {}
# servlet:function mapping
# format:
# HTTP['pages'][{servlet}] = function
HTTP['pages']['authenticate'] = 'process_authentication'
HTTP['pages']['change_password'] = 'process_change_password'
HTTP['pages']['unlock'] = 'process_unlock'
HTTP['pages']['reset'] = 'process_reset'
HTTP['pages']['create_user'] = 'process_create_user'

STATUS = {}
# Status code : definition mapping
STATUS['no_user'] = '1'
STATUS['auth_success'] = '0'
STATUS['auth_fail'] = '2'
STATUS['error'] = '3'
STATUS['user_created'] = '4'
STATUS['user_create_fail'] = '6'
STATUS['password_change_success'] = '7'
STATUS['password_change_fail'] = {}
STATUS['password_change_fail']['auth_fail'] = '8'
STATUS['password_change_fail']['create_user_fail'] = '9'
STATUS['account_locked'] = '10'
STATUS['password_reset_success'] = '11'
STATUS['password_reset_fail'] = '12'
STATUS['unlock_success'] = '13'
STATUS['unlock_fail'] = '14'
STATUS[''] = ''


ALLOWED_ATTEMPTS = 3    # Number of auth attempts before account locks

DEFAULT_PASSWORD = '1234'
