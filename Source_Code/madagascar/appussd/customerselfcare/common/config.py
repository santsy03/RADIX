#Opco settings
opco = {}
#Country code
opco['code'] = '261'
#MSISDN length without country code
opco['mlen'] = 9

#middleware application
application = {}
application['provision'] = {'ip': '127.0.0.1',
                            'port': '8787'}
application['balance'] = {'ip': '127.0.0.1',
                          'port': '8787'}
application['stop'] = {'ip': '127.0.0.1',
                       'port': '8787'}
#Data provision responses
responses = {}
responses[0] = 'Request queued for processing'
responses[1] = 'Unknown'
responses[2] = 'Missing parameters'
responses[3] = 'Error'
responses[4] = 'Invalid Package'
responses[5] = 'Request completed successfully'
responses[6] = 'Package Conflict'
responses[7] = 'Insufficient Funds'
responses[8] = 'Invalid transaction-id'
responses[9] = 'Time not allowed'
responses[10] = 'Auto-renewal stopped successfully'
responses[11] = 'Not on auto-renewal'
#me2u response codes
ME2U_CODES = {}
ME2U_CODES['0'] = 'error'
ME2U_CODES['1'] = 'insufficient_data_balance'
ME2U_CODES['2'] = 'amount_max'
ME2U_CODES['3'] = 'amount_min'
ME2U_CODES['4'] = 'no_bundle'
ME2U_CODES['5'] = 'success'
ME2U_CODES['7'] = 'insufficient_funds'
ME2U_CODES['8'] = 'volume_not_allowed'
ME2U_CODES['9'] = 'exhausted_daily_tries'
ME2U_CODES['10'] = 'expired_bundle'
ME2U_CODES['11'] = 'sender_expiry_limit'
ME2U_CODES['12'] = 'disallowed_category'
#For balance check
offers = {}
offers[1011] = {'price': '100','data': '1011', 'name':'my meg 15', 'uc_ut': '1011'}
offers[1014] = {'price': '1000','data': '1011', 'name':'my meg 50', 'uc_ut': '1011'}
offers[1016] = {'price': '3000','data': '1011', 'name':'my meg 100', 'uc_ut': '1011'}
offers[1018] = {'price': '13500','data': '1011', 'name':'my meg 250', 'uc_ut': '1011'}
offers[1019] = {'price': '25500','data': '1011', 'name':'my meg 500', 'uc_ut': '1011'}
offers[1021] = {'price': '45000','data': '1011', 'name':'my gig 1', 'uc_ut': '1011'}
offers[1022] = {'price': '67500','data': '1011', 'name':'my gig 2', 'uc_ut': '1011'}
offers[1024] = {'price': '90000','data': '1011', 'name':'my gig 5', 'uc_ut': '1011'}
offers[1025] = {'price': '135000','data': '1011', 'name':'my gig 10', 'uc_ut': '1011'}
offers[1026] = {'price': '180000','data': '1011', 'name':'my gig 30', 'uc_ut': '1011'}
offers[1030] = {'price': '1000','data': '1011', 'name':'my meg 50 gift', 'uc_ut': '1011'}
offers[1032] = {'price': '3000','data': '1011', 'name':'my meg 100 gift', 'uc_ut': '1011'}
offers[1034] = {'price': '13500','data': '1011', 'name':'my meg 250 gift', 'uc_ut': '1011'}
offers[1035] = {'price': '25500','data': '1011', 'name':'my meg 500 gift', 'uc_ut': '1011'}
offers[1037] = {'price': '45000','data': '1011', 'name':'my gig 1 gift', 'uc_ut': '1011'}
offers[1038] = {'price': '67500','data': '1011', 'name':'my meg 2 gift', 'uc_ut': '1011'}
offers[1040] = {'price': '90000','data': '1011', 'name':'my gig 5 gift', 'uc_ut': '1011'}
offers[1041] = {'price': '135000','data': '1011', 'name':'my gig 10 gift', 'uc_ut': '1011'}
offers[1042] = {'price': '180000','data': '1011', 'name':'my gig 30 gift', 'uc_ut': '1011'}
offers[1044] = {'price': '600','data': '1013', 'name':'my meg 20 night', 'uc_ut': '1013'}
offers[1045] = {'price': '900','data': '1013', 'name':'my meg 50 night', 'uc_ut': '1013'}
offers[1047] = {'price': '2600','data': '1013', 'name':'my meg 100 night', 'uc_ut': '1013'}
offers[1073] = {'price': '750','data': '1011', 'name':'Kozy Kozy', 'uc_ut': '1011'}
offers[1074] = {'price': '13500','data': '1011', 'name':'Rta Mobile', 'uc_ut': '1011'}
offers[1080] = {'price': '1500','data': '1011', 'name':'RTA bundle mix', 'uc_ut': '1011'}
offers[1081] = {'price': '0','data': '1011', 'name':'bundle universite', 'uc_ut': '1011'}
offers[1082] = {'price': '75','data': '1018', 'name':'Facebook', 'uc_ut': '1018'}
offers[1083] = {'price': '75','data': '1019', 'name':'Twitter', 'uc_ut': '1019'}
offers[1084] = {'price': '75','data': '1020', 'name':'Whatsapp', 'uc_ut': '1020'}
#Authentication api details
AUTH_API = {}
AUTH_API['ip'] = '127.0.0.1'
AUTH_API['port'] = '8005'
#Authentication response codes
STATUS = {}
STATUS[0] = 'Auth success'
STATUS[1] = 'No user'
STATUS[2] = 'Auth fail'
STATUS[3] = 'Error'
STATUS[4] = 'User created'
STATUS[6] = 'User create fail'
STATUS[7] = 'PIN change success'
STATUS[8] = 'PIN change fail - auth fail'
STATUS[9] = 'PIN change fail - create user fail'
STATUS[10] = 'Account locked'
STATUS[11] = 'PIN reset success'
STATUS[12] = 'PIN reset fail'
STATUS[13] = 'Unlock success'
STATUS[14] = 'Unlock fail'
STATUS[15] = 'Update list successful'
STATUS[16] = 'Incorrect parameters'
STATUS[17] = 'Update list fail'
