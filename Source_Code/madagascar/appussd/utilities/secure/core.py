#!/usr/bin/env python
from sha import sha as sha1
from binascii import hexlify, unhexlify
from random import randint
from random import choice
import string

keys = 'm49s4'
hashed = 128

def encrypt(msg):
    global keys
    global hashed
    if isinstance(keys,unicode):
        keys = keys.encode('utf8')
    key = sha1(keys).hexdigest()
    encrypted = []
    for i, c in enumerate(msg):
        key_c = ord(key[i % len(key)])
        msg_c = ord(c)
        encrypted.append(chr((msg_c + key_c) % hashed))
    return hexlify(''.join(encrypted))

def decrypt(pwd):
    global keys
    global hashed
    if isinstance(keys,unicode):
        keys = keys.encode('utf8')
    key = sha1(keys).hexdigest()
    msg = []
    encrypted = unhexlify(pwd)
    for i, c in enumerate(encrypted):
        key_c = ord(key[i % len(key)])
        enc_c = ord(c)
        msg.append(chr((enc_c - key_c) % hashed))
    return ''.join(msg)


def make_salt( **kwargs ):
    '''
    generates a random 4 digit 
    word to be used for salting the pin
    '''
    params = {}
    for name, value in kwargs:
        params[name] = value

    if 'length' in params:
        salt_length = params['length']
    else:
        salt_length = 4

    salt = ''.join( choice( string.lowercase )  for i in range(salt_length))
    return salt

def salt(password):
    '''
    generate salt
    salt password
    encrypt salted password
    return [ salt, encrypted_salted_password ]
    '''
    try:
        salt = make_salt()
        salted = '{0}{1}'.format( salt, password )
        return [ salt, encrypt(salted) ]
    except Exception, err:
        print 'utilities.secure.core.salt() failed - %r' % err
        raise err

def un_salt( salt, salted, **kwargs ):
    '''
    removes salt
    returns [ salt, unsalted_password ]
    '''
    try:
        params = {}
        for name, value in kwargs:
            params[name] = value
        
        if 'length' in params:
            salt_length = params['length']
        else:
            salt_length = 4

        salt = salted[ :int(salt_length) ]
        return [ salt, unsalted_password ]
    except Exception, err:
        print 'utilities.secure.core.un_salt() failed - %r' % err
        raise err



if __name__ == '__main__':
    import sys
    action_ok, password_ok = True, True
    try:
        action = sys.argv[1]
    except Exception:
        print 'Usage: python2.7 /appussd/utilities/secure/core.py encrypt <plaintextpass>'
        print 'Usage: python2.7 /appussd/utilities/secure/core.py decrypt <encryptedpass>'
        action_ok = False
    try:
        password = sys.argv[2]
    except Exception:
        print 'Usage: python2.7 /appussd/utilities/secure/core.py encrypt <plaintextpass>'
        print 'Usage: python2.7 /appussd/utilities/secure/core.py decrypt <encryptedpass>'
        password_ok = False

    if action_ok and password_ok:
        print 'Key:', repr(keys)
        if action == 'encrypt':
            print 'PlainTextPassword:', password
            encrypted = encrypt(password)
            decrypted = decrypt(encrypted)
            print 'Encrypted:', repr(encrypted)
            print 'Decrypted:', repr(decrypted)
        elif action == 'decrypt':
            print 'EncryptedPassword:', password
            decrypted = decrypt(password)
            encrypted = encrypt(decrypted)
            print 'Decrypted:', repr(decrypted)
            print 'Encrypted:', repr(encrypted)
        else:
            print 'Invalid action'
