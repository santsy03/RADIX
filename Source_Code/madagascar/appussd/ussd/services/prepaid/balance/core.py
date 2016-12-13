import traceback
from decimal import Decimal

from utilities.ucip.core import get_balance_and_date
from utilities.logging.core import log

from config import da, failureTxt, resp

cents = Decimal('0.01')
def get_all_subscriber_balance(resources):
    """
    Returns various subscriber balances.
    1. MA
    2. Modular
    3. Bonus
    4. Min
    5. Sec
    6. Sms
    7. Data
    """
    transId = resources['parameters']['sessionId']
    resources['parameters']['transactionId'] = transId
    resources['parameters']['externalData1'] = 'balanceCheck'
    resources['parameters']['externalData2'] = 'radixBa'
    try:
        response = get_balance_and_date(resources)
    except Exception, err:
        log(resources, traceback.format_exc(), 'error')

    else:
        return response
   

def segregate_balance(resources):
    """
    Formats balance as above.
    """
    msisdn = resources['parameters']['msisdn']
    language = resources['parameters']['language']
    try:
        response = get_all_subscriber_balance(resources)

    except Exception, e:
        log(resources, traceback.format_exc(), 'error')

    else:
        sms = None
        min = []
        bon = []
        sec = []
        mod = []
        data = []
        if response['responseCode'] == 0:
            MA = str(Decimal(int(response['accountValue1'])/Decimal('100')).quantize(cents))
            if 'dedicatedAccountInformation' in response:
                daInfo = response['dedicatedAccountInformation']
                for info in daInfo:
                    if str(info['dedicatedAccountID']) in da['sms']:
                        sms = info['dedicatedAccountValue1']
                    if str(info['dedicatedAccountID']) in da['mn']:
                        min.append(int(info['dedicatedAccountValue1']))
                    if str(info['dedicatedAccountID']) in da['bonus']:
                        bon.append(Decimal(int(info['dedicatedAccountValue1'])/Decimal('100')).quantize(cents))
                    if str(info['dedicatedAccountID']) in da['sec']:
                        sec.append(int(info['dedicatedAccountValue1'])) 
                    if str(info['dedicatedAccountID']) in da['modular']:
                        mod.append(Decimal(int(info['dedicatedAccountValue1'])/Decimal('100')).quantize(cents))
                    if str(info['dedicatedAccountID']) in da['data']:
                        data.append(Decimal(int(info['dedicatedAccountValue1'])/Decimal('100')).quantize(cents))

                log(resources, "sms:%s"%str(sms), 'debug')
                log(resources, "Min:%s"%str(min), 'debug')
                log(resources, "Bonus:%s"%str(bon), 'debug')
                log(resources, "Seconds:%s"%str(sec), 'debug')
                log(resources, "Modular:%s"%str(mod), 'debug')
                log(resources, "Data:%s"%str(data), 'debug')
                bal =  (MA, sms, sum(min), sum(bon), sum(sec),
                       sum(mod), sum(data))
                balance = format_balance(bal, language)
                return balance

            else:
                bal = (MA, 0, 0, 0, 0, 0, 0)
                balance = format_balance(bal, language)
                return balance
        else:
            debug = "IN Returned responseCode:%s for Msisdn:%s"\
                    %(str(response['responseCode']), str(msisdn))
            log(resources, debug, 'debug')
            return failureTxt


def format_balance(bal, lan):
    """
    Takes a tuple and do string
    Substitution.
    """
    try:
        MA = bal[0]
        sms = bal[1]
        min = bal[2]
        bon = bal[3]
        sec = bal[4]
        mod = bal[5]
        data = bal[6]
        response = resp[str(lan)].substitute(ma=MA,mod=mod,
                   bon=bon,min=min,sec=sec,sms=sms,data=data)

    except Exception, e:
        log(resources, traceback.format_exc(), 'error')

    else:
        return response
       

if __name__ == '__main__':
    resources = {}
    param = {'msisdn':'261330770007', 'language':'txt-3','sessionId':'8373737'}
    resources['parameters'] = param
    print segregate_balance(resources)
   
