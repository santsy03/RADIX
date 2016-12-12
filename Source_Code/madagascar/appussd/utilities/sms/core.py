#-*- coding: utf-8 -*-
'''
utility methods for sending sms
'''
from utilities.secure.core import decrypt
from configs.config import kannel

def send_message(msisdn, message, logger = None):
    from urllib import urlopen,urlencode
    message = str(message)
    user_name = decrypt(str(kannel['username']))
    password = decrypt(str(kannel['password']))
    args = urlencode({'username':user_name,'password':password,'to':str(msisdn),'from':'AIRTEL','text':message,})#'charset':'utf-8','coding':'2'})
    try:
        url = 'http://127.0.0.1:14020/cgi-bin/sendsms?%s' %  str(args)
        print "MESSAGE:: "+message
        resp = urlopen(url)
    except Exception,e:
        print "could not send message: %s for this sub %s" %  (str(e), str(msisdn))
        if logger:
            logger.info("could not send message: %s for this sub %s" %  (str(e), str(msisdn)))
    else:
        info = "message: %s, msisdn: %s, successfully sent" % (message, msisdn)
        print info
        if logger:
            logger.info(info)
        return True

if  __name__ == '__main__':
    send_message("261330998255","Chere client, votre forfait Internet de My Meg 50 a ete renouvele avec succes pour 1. Pour arreter le renouvellemnt automatique Tapez *114*0*2#")

