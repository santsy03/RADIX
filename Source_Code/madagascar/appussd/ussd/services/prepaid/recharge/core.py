import traceback
from datetime import datetime

from utilities.ucip.airHandler import AIRHandler
from utilities.logging.core import log

from config import resp, wrong_voucher, failureTxt, more_digits
   

def refill_subscriber_number(resources):
    """
    Top up a subscriber with airtime.
    @msisdn
    @voucher
    """
    msisdn = resources['parameters']['msisdn']
    language = resources['parameters']['language']
    voucher = resources['parameters']['pin']
    sessionId = resources['parameters']['sessionId']
    try:
        if voucher.isdigit() and len(voucher) > 15:
            return more_digits[str(language)]
        else:
            if voucher.isdigit() and len(voucher) == 15:
                params = {}
                
                params['transactionId'] = str(sessionId)
                params['externalData1'] = 'refill'
                params['externalData2'] = 'r_Radix'
                air = AIRHandler(params)
                start = datetime.now()
                response = air.refill(msisdn, voucher)
                end = datetime.now()
                duration = (end - start).total_seconds()
                info = "Time taken to refill:%s, Msisdn:%s"\
                        %(str(duration), str(msisdn))
                log(resources, info, 'info')
            
                #response = air.refill(msisdn, voucher)
                #response = {'originTransactionID': '18282', 'responseCode': 0, 'refillFraudCount': 4}
                #response['responseCode'] == 0
                #response['transactionAmount'] = '10000'
                if response['responseCode'] == 0:
                    amount = int(response['transactionAmount'])
                    amount = amount/100
                    return resp[str(language)].substitute(amt=str(amount))

                else:
                    debug = "IN Returned responseCode:%s for Msisdn:%s"\
                            %(str(response['responseCode']), str(msisdn))
                    log(resources, debug, 'debug')
                    return failureTxt
            else:
                debug = "Invalid Voucher:%s Msisdn:%s"%(str(voucher), str(msisdn))
                log(resources, debug, 'debug')
                return wrong_voucher[str(language)]

    except Exception, e:
        log(resources, traceback.format_exc(), 'error')




if __name__ == '__main__':
    resources = {}
    params = {'msisdn':'261330465390', 'language':'txt-1', 'pin':'837363636361234', 'sessionId':'451134455635'}
    resources['parameters'] = params
    print refill_subscriber_number(resources)
