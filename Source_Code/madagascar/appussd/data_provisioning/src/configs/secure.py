#!/usr/bin/env python
from sha import sha as sha1
from binascii import hexlify, unhexlify

#keys = 's3ch31132'
keys = 'k3ny4'
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

if __name__ == '__main__':
    key = 'r@D1x'
    msg = 'radix'
    #krypt = encrypt()
    encrypted = encrypt(msg)
    decrypted = decrypt(encrypted)

    print 'Message:', msg
    print 'Key:', repr(key)
    print 'Encrypted:', repr(encrypted)
    print 'Decrypted:', repr(decrypted)

