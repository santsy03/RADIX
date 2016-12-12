debug = True
eng = 'txt-1'
mal = 'txt-2'
default_language = mal
airtel_prefix = '033'


SQL = {}
MIX = {}
HTTP = {}
PORTS = {}
QUEUES = {}
STATUS = {}
EVENTS = {}
THREADS = {}
TIMEOUTS = {}
RESPONSES = {}
WHITELIST = {}
EXCEPTIONS = {}
STOP_RENEWAL = {}
WEB_SERVICES = {}
APPLICATIONS = {}
USSD_RESPONSES = {}
BALANCE_CATEGORY= {}
PACK_TIME_MAPPING = {}
DEGRESSIVE_PACKAGES = {}

WHITELIST['toggle'] = 'off'
WHITELIST['msisdns'] = ['261330891190','261331611457','261332287989','261330798574','261331001028','261331005571','261331004862','261331004864','261338001184']

PORTS['hxc_proxy'] = {}
PORTS['hxc_proxy']['114'] = 8343          # 1100
PORTS['hxc_proxy']['103'] = 8345
PORTS['hxc_proxy']['100'] = 8344
PORTS['hxc_proxy']['177'] = 6329

PORTS['ussd'] = {}
PORTS['ussd']['100'] = 7346
PORTS['ussd']['103'] = 7344
PORTS['ussd']['114'] = 7345
PORTS['ussd']['177'] = 7345


PORTS['sms'] = 1103
PORTS['responses'] = 1102
PORTS['requests_http'] = 1106

THREADS['hxc_proxy'] = 400
THREADS['ussd'] = 400
THREADS['sms'] = 200
THREADS['requests'] = 10
THREADS['requests_http'] = 10
THREADS['renewals'] = 10
THREADS['responses'] = {}
THREADS['responses']['listener'] = 200
THREADS['responses']['consumer'] = 10
THREADS['responses']['renewals'] = 10

HTTP['queued'] = {}
HTTP['queued']['code'] = '0'
HTTP['queued']['desc'] = 'queued'

HTTP['missing_parameter'] = {}
HTTP['missing_parameter']['code'] = '1'
HTTP['missing_parameter']['desc'] = 'mandatory parameter missing'

HTTP['auth_failed'] = {}
HTTP['auth_failed']['code'] = '2'
HTTP['auth_failed']['desc'] = 'failed authentication'

HTTP['invalid_transaction_type'] = {}
HTTP['invalid_transaction_type']['code'] = '4'
HTTP['invalid_transaction_type']['desc'] = 'invalid transaction type'

HTTP['error'] = {}
HTTP['error']['code'] = '3'
HTTP['error']['desc'] = 'other error'

HTTP['invalid_transaction_id'] = {}
HTTP['invalid_transaction_id']['code'] = '11'
HTTP['invalid_transaction_id']['desc'] = 'invalid transaction id'

HTTP[''] = {}
HTTP['']['code'] = ''
HTTP['']['desc'] = ''

provision_actions = ['provision', 'provisioning']
balance_actions = ['balance', 'balance_check']
stop_actions = ['stop', 'stop_renewal']
response_actions = ['response']

STOP_RENEWAL['pass'] = '51'  # successfully stopped
STOP_RENEWAL['fail'] = '31'  # stop renewal failed

STATUS['51'] = 'stopped'
STATUS['31'] = 'no renewals'


APPLICATIONS['100'] = {}
APPLICATIONS['100']['prepaid'] = 'http://127.0.0.1:%s' % PORTS['ussd']['100']
APPLICATIONS['100']['postpaid'] = ''

APPLICATIONS['103'] = {}
APPLICATIONS['103']['prepaid'] = 'http://127.0.0.1:%s' % PORTS['ussd']['103']
APPLICATIONS['103']['postpaid'] = ''

APPLICATIONS['114'] = {}
APPLICATIONS['114']['prepaid'] = 'http://127.0.0.1:%s' % PORTS['ussd']['114']
APPLICATIONS['114']['postpaid'] = ''


APPLICATIONS['177'] = {}
APPLICATIONS['177']['prepaid'] = 'http://127.0.0.1:%s' % PORTS['ussd']['114']
APPLICATIONS['177']['postpaid'] = ''

APPLICATIONS['requests'] = {}
for action in provision_actions:
    APPLICATIONS['requests'][action] = 'http://127.0.0.1:%s/provision?' % PORTS['requests_http']
for action in balance_actions:
    APPLICATIONS['requests'][action] = 'http://127.0.0.1:%s/balance?' % PORTS['requests_http']
for action in stop_actions:
    APPLICATIONS['requests'][action] = 'http://127.0.0.1:%s/stop?' % PORTS['requests_http']

WEB_SERVICES = {}
WEB_SERVICES['port'] = '9002'
WEB_SERVICES['accountId'] = 'modular'
WEB_SERVICES['authKey'] = 'modularP4ss'
WEB_SERVICES['channel'] = 'modular_tariffs'
WEB_SERVICES['renewal_channel'] = 'renewals'
WEB_SERVICES['requests_callback'] = 'http://127.0.0.1:%s/process' % PORTS['responses']

QUEUES['modular_requests'] = 'modular_requests'
QUEUES['modular_responses'] = '%s_responses' % WEB_SERVICES['channel']
QUEUES['renewal_responses'] = '%s_responses' % WEB_SERVICES['renewal_channel']
QUEUES['renewals'] = 'renewals_req'
QUEUES[''] = ''

TIMEOUTS = {}
TIMEOUTS['web_services'] = 4
TIMEOUTS['requests'] = 4

TIMEOUT = TIMEOUTS

USSD_RESPONSES['invalid_command'] = {}
USSD_RESPONSES['invalid_command'][eng] = 'You have entered an invalid command'
USSD_RESPONSES['invalid_command'][mal] = 'You have entered an invalid command'

USSD_RESPONSES['postpaid'] = {}
USSD_RESPONSES['postpaid'][eng] = 'This service is not available for postpaid subscribers'
USSD_RESPONSES['postpaid'][mal] = 'This service is not available for postpaid subscribers'

#Whitelist
MSISDNS = ['2617272618']
error_ussd = 'There was an error in handling the request. Please try again later'

accepted_ussd_shortcuts = ['1','2','3','4','5','7','12','13','14','15','16']


RESPONSES['success'] = {}
RESPONSES['success'][eng] = 'Your request has been received. Wait for a response'
RESPONSES['success'][mal] = 'Voaray ny fangatahanao. Miandrasa kely azafady. Misaotra tompoko'

RESPONSES['failure'] = {}
RESPONSES['failure'][eng] = 'There was a problem processing your request. Try again later'
RESPONSES['failure'][mal] = 'Tsy tontosa ny fangatahanao. Azafady, avereno afaka fotoana fohy. Misaotra tompoko'

RESPONSES['invalid_code'] = {}
RESPONSES['invalid_code'][eng] = 'Invalid USSD shortcut'
RESPONSES['invalid_code'][mal] = 'Invalid USSD shortcut'

EXCEPTIONS['data_provisioning'] = {}
EXCEPTIONS['data_provisioning']['request'] = 'Data Provisioning Responded With : %s'
EXCEPTIONS['data_provisioning']['response'] = 'Data Provisioning Returned Response: %s'

EXCEPTIONS['invalid_action'] = 'Unknown Action Requested: %s'
EXCEPTIONS['invalid_hour'] = '%s || Package %s -- %s is not available at this time. '

EXCEPTIONS['missingParameter'] = ' Missing parameter '

''' Packages
1   ClubSms
2   FUN Mini
3   PAY
4   LIBERTE 5
5   No frontier
6   Neighbors
7   Fun Cool
8   Fun Relax
9   Fun Extra
10  Fun Ultra
11  Fun Maxi
12  Fun15
'''

SQL['stored_function'] = 'generate_modular_id'
SQL['package_details'] = 'select PACKAGE_NAME, START_TIME, STOP_TIME, DA_ID from PACKAGES where id = :package'
SQL['update_request'] = 'update MODULAR_REQUEST set RESPONSE = :status, COMPLETED_AT = systimestamp where ID = :modular_id'
SQL['stop_status'] = 'select response from modular_request where id = :modular_id'
SQL['fetch_response'] = 'select response from MODULAR_REQUEST where id = :modular_id'
SQL['request_type'] = 'select action, msisdn from MODULAR_REQUEST where id = :modular_id'
SQL['degressive_frequency'] = 'select count(*) from requests where msisdn = :msisdn and package_id = :package_id and status = :status and to_char(created_at, \'dd-MON-RR\') = :today'

DA_DATA = ['8','14']
DA_VOICE = ['4','6','7','11','12','1', '26']
DA_SMS = ['2']
DA_FUNP = ['20']

BALANCE_CATEGORY['data'] = DA_DATA
BALANCE_CATEGORY['sms'] = DA_SMS
BALANCE_CATEGORY['voice'] = DA_VOICE

EVENTS['notify'] = '1'
EVENTS['provision'] = '2'
EVENTS['notify_two'] = '3'
EVENTS['service_id'] = {}
EVENTS['service_id']['modular'] = '1'
EVENTS['service_id'][''] = ''
EVENTS['renewal_spacing'] = '3' # If renewal fails, try again after ~ hours
EVENTS['renewal_tries_in_a_day'] = '3'  #  Try ~ times per day
EVENTS['renewal_days'] = '3'    # Try renewing for ~ days then stop trying
EVENTS['notification'] = '2880'   # Send pre-renewal notification ~ minutes before renewal happens
EVENTS['notification_two'] = '1440'   # Send pre-renewal notification ~ minutes before renewal happens

DEGRESSIVE_PACKAGES['list'] = []

#  format:
#  DEGRESSIVE_PACKAGES[package_id][frequency] = new_package_id

DEGRESSIVE_PACKAGES['x'] = {}
DEGRESSIVE_PACKAGES['x'][0] = ''
DEGRESSIVE_PACKAGES['x'][1] = ''
DEGRESSIVE_PACKAGES['x'][2] = ''
DEGRESSIVE_PACKAGES['x'][3] = ''

DEGRESSIVE_PACKAGES['y'] = {}
DEGRESSIVE_PACKAGES['y'][0] = ''
DEGRESSIVE_PACKAGES['y'][1] = ''
DEGRESSIVE_PACKAGES['y'][2] = ''

DEGRESSIVE_PACKAGES['z'] = {}
DEGRESSIVE_PACKAGES['z'][0] = ''
DEGRESSIVE_PACKAGES['z'][1] = ''
DEGRESSIVE_PACKAGES['z'][2] = ''

# format:
# MIX[ new_package_id ] = [ P_ID1, P_ID2, P_ID3... ]
MIX['40'] = [1,2,3]
MIX[''] = []
MIX[''] = []

