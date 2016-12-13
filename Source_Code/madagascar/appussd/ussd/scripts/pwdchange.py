#!/usr/bin/python

import sys, fileinput
sys.path.append('/appussd')
from ussd.services.common.secure.secure import encrypt, decrypt
from ussd.configs.core import databases


username = databases['core']['username']
password = databases['core']['password']

if len(sys.argv) == 2:
    username = databases['core']['username']
    password = databases['core']['password']
    print "Username: %s \nCurrent Password: %s\nCurrent Encrypted Password: %s\n" %(decrypt(username), decrypt(password),password)
    newpassword = encrypt(sys.argv[1].strip())
    print "New password: %s\nEncrypted password: %s\n" %(decrypt(newpassword), newpassword)
    sys.exit(0)
