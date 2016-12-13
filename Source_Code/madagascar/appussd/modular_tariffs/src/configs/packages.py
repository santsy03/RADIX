#!/usr/bin/env python
#coding: utf-8

PACKAGES = {}
'''
package mapping based on direct dialing string.

Format: PACKAGE[SHORTCODE][SHORTCUT] = PACKAGE_ID

E.g. 
For package 1 is *114*1#.

∴  PACKAGE['114']['1'] = '1'

'''

PACKAGES['114'] = {}
PACKAGES['114']['1'] = '1'
PACKAGES['114']['2'] = '2'
PACKAGES['114']['3'] = '5'
PACKAGES['114']['4'] = '6'
PACKAGES['114']['5'] = '7'
PACKAGES['114']['6'] = '8'
PACKAGES['114']['7'] = '9'
PACKAGES['114']['8'] = '10'
PACKAGES['114']['9'] = '11'
PACKAGES['114']['10'] = '12'
PACKAGES['114']['11'] = '13'
PACKAGES['114']['12'] = '14'
PACKAGES['114']['13'] = '15'
PACKAGES['114']['14'] = '16'
PACKAGES['114']['15'] = '17'
PACKAGES['114']['24'] = '18'
PACKAGES['114']['31'] = '19'
PACKAGES['114']['32'] = '20'
PACKAGES['114']['33'] = '21'
PACKAGES['114']['34'] = '22'
PACKAGES['114']['35'] = '23'
PACKAGES['114']['100'] = 'stop'
PACKAGES['114']['101'] = '0'
PACKAGES['114']['102'] = '00'
PACKAGES['114']['103'] = '000'

BALANCE_PACKAGES = {}
BALANCE_PACKAGES['0'] = 'data'
BALANCE_PACKAGES['00'] = 'sms'
BALANCE_PACKAGES['000'] = 'voice'

PACKAGES['100'] = {}
PACKAGES['100']['2'] = '24'
PACKAGES['100']['5'] = '35'
PACKAGES['100']['7'] = '29'
PACKAGES['100']['8'] = '30'
PACKAGES['100']['13'] = '34'
PACKAGES['100']['100'] = 'stop'
PACKAGES['100']['101'] = '00'

PACKAGES['177'] = {}
PACKAGES['177']['2'] = '37' # 
PACKAGES['177']['70'] = '41' # 
PACKAGES['177']['8'] = '42'
PACKAGES['177']['5'] = '45'


#PACKAGES['177']['7'] = '29'
#PACKAGES['177']['13'] = '34'
PACKAGES['177']['100'] = 'stop'
PACKAGES['177']['101'] = '00'

#PACKAGES['177']['5'] = '3'   # for testing only - to remove afterwards

PACKAGES['101'] = {}
PACKAGES['101']['3'] = '31'


''' - for data tests
PACKAGES['177'] = {}
PACKAGES['177']['1'] = '1'
PACKAGES['177']['2'] = '2'
PACKAGES['177']['3'] = '5'
PACKAGES['177']['4'] = '6'
PACKAGES['177']['5'] = '7'
PACKAGES['177']['6'] = '8'
PACKAGES['177']['7'] = '9'
PACKAGES['177']['8'] = '10'
PACKAGES['177']['9'] = '11'
PACKAGES['177']['10'] = '12'
PACKAGES['177']['11'] = '13'
PACKAGES['177']['12'] = '14'
PACKAGES['177']['13'] = '15'
PACKAGES['177']['14'] = '16'
PACKAGES['177']['15'] = '17'
PACKAGES['177']['24'] = '18'
PACKAGES['177']['31'] = '19'
PACKAGES['177']['32'] = '20'
PACKAGES['177']['33'] = '21'
PACKAGES['177']['34'] = '22'
PACKAGES['177']['100'] = 'stop'
PACKAGES['177']['101'] = '0'
PACKAGES['114']['102'] = '00'
PACKAGES['114']['103'] = '000'
'''


PACKAGES['41114'] = {}
PACKAGES['41114']['1'] = '25'
PACKAGES['41114']['7'] = '26'
PACKAGES['41114']['8'] = '27'
PACKAGES['41114']['9'] = '28'

PACKAGES[''] = {}
PACKAGES[''][''] = ''
PACKAGES[''][''] = ''
PACKAGES[''][''] = ''
