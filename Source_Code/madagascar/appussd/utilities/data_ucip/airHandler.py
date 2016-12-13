import logging
from datetime import tzinfo,timedelta,datetime
from copy import deepcopy
from tools import *

from utilities.secure.core import decrypt
from configs.config import aapcn_air

username = decrypt(aapcn_air['user']) 
password = decrypt (aapcn_air['password'])
#url = "http://fdsuser:fdsuser@172.25.154.86:10010/Air"
class AIRHandler:
    logger = logging.getLogger('AIRHandler')
    originHostName = 'radix'

    def __init__(self, params, host, originHostName = 'radix'):
        self.url="http://%s:%s@%s:10010/Air" % (username,password,host)
        self.basicRequest =  {}
        self.basicRequest[ 'originNodeType' ] = 'ADM'
        if 'originHost' in params:
            originHostName = params['originHost']
        self.basicRequest[ 'originHostName' ] = 'USSD2Data'
        self.basicRequest[ 'originTransactionID' ] = params['transactionId']
        self.basicRequest['externalData1'] = params['externalData1']
        self.basicRequest['externalData2'] = params['externalData2']
        self.USER_AGENT = 'UGw Server/4.3/1.0'
        self.transport = Transporter( Transporter.HTTP, self.USER_AGENT )
        self.airServer = xmlrpclib2.ServerProxy( self.url, self.transport, verbose=True)

    def getBalanceAndDate( self, msisdn ):
        Req = deepcopy( self.basicRequest )
        Req[ 'originTimeStamp' ] = self.now()
        Req[ 'subscriberNumber' ] = msisdn
        Req[ 'subscriberNumberNAI' ] = 1
        self.logger.debug( Req )
        return self.airServer.GetBalanceAndDate( Req )

    def now(self):
        from datetime import datetime
        today = datetime.today()
        return today.replace( tzinfo=GMT330() )

    def getAccumulators(self, msisdn):
        Req = deepcopy( self.basicRequest )
        Req[ 'originTimeStamp' ] = self.now()
        Req[ 'subscriberNumber' ] = msisdn
        Req[ 'subscriberNumberNAI' ] = 1
        self.logger.debug( Req )
        return self.airServer.GetAccumulators( Req )

    def updateBalanceAndDate(self,msisdn,amount):
        updReq = deepcopy( self.basicRequest )
        updReq[ 'originTimeStamp' ] = self.now()
        updReq[ 'subscriberNumber' ] = msisdn
        updReq[ 'transactionCurrency' ] = 'MGA'
        updReq[ 'subscriberNumberNAI' ] = 1
        updReq[ 'adjustmentAmountRelative' ] = str(amount)
        self.logger.debug( updReq )
        return self.airServer.UpdateBalanceAndDate(updReq)
  
    def getAccountDetails(self, msisdn):
        Req = deepcopy( self.basicRequest )
        Req[ 'originTimeStamp' ] = self.now()
        Req[ 'subscriberNumber' ] = msisdn
        Req[ 'subscriberNumberNAI' ] = 1
        self.logger.debug( Req )
        return self.airServer.GetAccountDetails( Req )	

    def getAllowedServiceClasses(self, msisdn):
        """ Optional License (ID:01871) is required """
        Req = deepcopy( self.basicRequest )
        Req[ 'originTimeStamp' ] = self.now()
        Req[ 'subscriberNumber' ] = msisdn
        Req[ 'subscriberNumberNAI' ] = 1
        self.logger.debug( Req )
        return self.airServer.GetAllowedServiceClasses( Req )

    def getFaFList( self, msisdn ):
        Req = deepcopy( self.basicRequest )
        Req[ 'originTimeStamp' ] = self.now()
        Req[ 'subscriberNumber' ] = msisdn
        Req[ 'requestedOwner' ] = 1
        Req[ 'subscriberNumberNAI' ] = 1
        self.logger.debug( Req )
        return self.airServer.GetFaFList( Req )
		
    def refill( self, msisdn, voucher ):
        Req = deepcopy( self.basicRequest )
        Req[ 'originTimeStamp' ] = self.now()
        Req[ 'subscriberNumber' ] = msisdn
        Req[ 'voucherActivationCode' ] = voucher
        Req[ 'subscriberNumberNAI' ] = 1
        self.logger.debug( Req )
        return self.airServer.Refill( Req )

    def updateFaFList( self, msisdn, action, fafNum, fafInd=0, owner='Subscriber' ):
        """ fafAction have to be one of below option
        fafAction: ADD, SET, DELETE
        """
        Req = deepcopy( self.basicRequest )
        Req[ 'originTimeStamp' ] = self.now()
        Req[ 'subscriberNumber' ] = msisdn
        Req[ 'fafAction' ] = action
        Req[ 'subscriberNumberNAI' ] = 1
        Req[ 'fafInformation' ] = { 'fafNumber': fafNum ,'fafIndicator':fafInd, 'owner': owner }
        self.logger.debug( Req )
        return self.airServer.UpdateFaFList( Req )

    def updateSubscriberSegmentation( self, msisdn, serviceOfferingId, serviceOfferingActiveFlag ):
        '''usage example: updateSubscriberSegmentation('254733725373',1,True) '''
        updReq = deepcopy( self.basicRequest )
        updReq[ 'originTimeStamp' ] = self.now()
        updReq[ 'subscriberNumber' ] = msisdn
        updReq[ 'subscriberNumberNAI' ] = 1
        xflag=[(serviceOfferingId,serviceOfferingActiveFlag),]
        so=[]
        solist={ 'serviceOfferingID': xflag[0][0] ,'serviceOfferingActiveFlag':xflag[0][1] }
        so.append(solist)
        #updReq[ 'serviceOfferings' ] = { 'serviceOfferingID': serviceOfferingId ,'serviceOfferingActiveFlag':serviceOfferingActiveFlag }
        updReq[ 'serviceOfferings' ] = so
        self.logger.debug( updReq )
        return self.airServer.UpdateSubscriberSegmentation( updReq )

    def updateDedicatedAccount( self, msisdn, amount, action, account, expiryDate, da_unit, hostName=originHostName):
        '''
        expiryDate should be a datetime object eg, dt=datetime(2010, 7, 23, 5, 4, 1) 
        '''        
        updReq = deepcopy( self.basicRequest )
        updReq[ 'originHostName' ] = hostName
        updReq[ 'originTimeStamp' ] = self.now()
        updReq[ 'subscriberNumber' ] = msisdn
        updReq[ 'transactionCurrency' ] = 'MGA'
        updReq[ 'subscriberNumberNAI' ] = 1        
        dainfo={'dedicatedAccountID':account,action:str(amount)}
        if action=='dedicatedAccountValueNew':
            dainfo['expiryDate']=expiryDate
        elif action=='adjustmentAmountRelative':
            #dainfo['adjustmentDateRelative']=expiryDate
            dainfo['expiryDate']=expiryDate
        dainfo['dedicatedAccountUnitType']= da_unit
        #nairobi = pytz.timezone("Africa/Nairobi")
        updReq[ 'dedicatedAccountUpdateInformation' ] =[ dainfo ]
        self.logger.debug( updReq )
        return self.airServer.UpdateBalanceAndDate(updReq)

    def setServiceClass( self, msisdn, sc ):
        Req = deepcopy( self.basicRequest )
        Req[ 'originTimeStamp' ] = self.now()
        Req[ 'subscriberNumber' ] = msisdn
        Req[ 'serviceClassAction' ] = 'SetOriginal'
        Req[ 'subscriberNumberNAI' ] = 1
        Req[ 'serviceClassNew' ] = sc
        self.logger.debug( Req )
        return self.airServer.UpdateServiceClass( Req )

    def setServiceClassTemporary( self, msisdn, sc, expdt=None ):
        Req = deepcopy( self.basicRequest )
        Req[ 'originTimeStamp' ] = self.now()
        Req[ 'subscriberNumber' ] = msisdn
        Req[ 'serviceClassAction' ] = 'SetTemporary'
        Req[ 'subscriberNumberNAI' ] = 1
        Req[ 'serviceClassTemporaryNew' ] = sc
        if expdt:
            Req[ 'serviceClassTemporaryNewExpiryDate' ] = expdt
        self.logger.debug( Req )
        return self.airServer.UpdateServiceClass( Req )

    def delServiceClassTemporary( self, msisdn, sc ):
        Req = deepcopy( self.basicRequest )
        Req[ 'originTimeStamp' ] = self.now()
        Req[ 'subscriberNumber' ] = msisdn
        Req[ 'subscriberNumberNAI' ] = 1
        Req[ 'serviceClassAction' ] = 'DeleteTemporary'
        Req[ 'serviceClassTemporary' ] = sc
        sellf.logger.debug( Req )
        return self.airServer.UpdateServiceClass( Req )

    def updateOffer( self,msisdn,offerId,expiryDate=None,startDate=None):
        Req = deepcopy( self.basicRequest )
        Req[ 'originTimeStamp' ] = self.now()
        Req[ 'subscriberNumber' ] = msisdn[-9:]
        Req[ 'subscriberNumberNAI' ] = 2
        Req[ 'offerID' ] = offerId
        Req[ 'originTimeStamp' ] = self.now()
        Req[ 'offerType' ] = 2
        if startDate != None:
            Req['startDateTime'] = startDate
        if expiryDate != None:
            Req['expiryDateTime'] = expiryDate
        return self.airServer.UpdateOffer(Req)

    def updateValueOffer( self,msisdn,offerId,expiryDate=None,startDate=None):
        Req = deepcopy( self.basicRequest )
        Req[ 'originTimeStamp' ] = self.now()
        Req[ 'subscriberNumber' ] = msisdn[-9:]
        Req[ 'subscriberNumberNAI' ] = 2
        Req[ 'offerID' ] = offerId
        Req[ 'originTimeStamp' ] = self.now()
        if startDate != None:
            Req['startDate'] = startDate
        if expiryDate != None:
            Req['expiryDate'] = expiryDate
        return self.airServer.UpdateOffer(Req)

    def deleteOffer( self,msisdn,offerId):
        Req = deepcopy( self.basicRequest )
        Req[ 'originTimeStamp' ] = self.now()
        Req[ 'subscriberNumber' ] = msisdn[-9:]
        Req[ 'subscriberNumberNAI' ] = 2
        Req[ 'offerID' ] = offerId
        Req[ 'originTimeStamp' ] = self.now()
        return self.airServer.DeleteOffer(Req)

    def getOffers(self,msisdn):
        Req = deepcopy( self.basicRequest )
        Req[ 'originTimeStamp' ] = self.now()
        Req[ 'subscriberNumber' ] = msisdn[-9:]
        Req[ 'subscriberNumberNAI' ] = 2
        Req[ 'requestInactiveOffersFlag' ] = True
        Req[ 'offerRequestedTypeFlag' ] = '11110000'
        return self.airServer.GetOffers(Req)

    def DeleteOffer( self, msisdn, offer):
        Req = deepcopy( self.basicRequest )
        Req[ 'originTimeStamp' ] = self.now()
        Req[ 'subscriberNumber' ] = msisdn[-9:]
        Req[ 'subscriberNumberNAI' ] = 2
        Req[ 'offerID' ] = int(offer)
        self.logger.debug( Req )
        return self.airServer.DeleteOffer( Req )

    def Refill( self, msisdn, refill_id, amount):
        Req = deepcopy( self.basicRequest )
        Req[ 'originTimeStamp' ] = self.now()
        Req[ 'subscriberNumber' ] = msisdn[-9:]
        Req[ 'transactionAmount'] = str(amount)
        Req[ 'transactionCurrency' ] = 'MGA'
        Req[ 'subscriberNumberNAI' ] = 2
        Req['refillProfileID'] = refill_id
        self.logger.debug( Req )
        return self.airServer.Refill( Req )

    def updateUsageThresholdsAndCounters( self, msisdn, uc, ut, thresh_value):
        Req = deepcopy( self.basicRequest )
        Req[ 'originTimeStamp' ] = self.now()
        Req[ 'subscriberNumber' ] = msisdn[-9:]
        Req[ 'subscriberNumberNAI' ] = 2
        Req['usageThresholdUpdateInformation'] = [{'usageThresholdID':int(ut), \
                'usageThresholdValueNew':str(thresh_value)}]
        Req['usageCounterUpdateInformation'] = [{'usageCounterID':int(uc), \
                'usageCounterValueNew':'0'}]
        self.logger.debug( Req )
        return self.airServer.UpdateUsageThresholdsAndCounters( Req )

    def GetUsageThresholdsAndCounters( self, msisdn):
        Req = deepcopy( self.basicRequest )
        Req[ 'originTimeStamp' ] = self.now()
        Req[ 'subscriberNumber' ] = msisdn[-9:]
        Req[ 'subscriberNumberNAI' ] = 2
        self.logger.debug( Req )
        return self.airServer.GetUsageThresholdsAndCounters( Req )

def bill_subscriber(resources):
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    amount = '-%s00' %str(parameters['configurations']['price'])
    transactionId = str(parameters['transaction_id'])
    external_data_1 = 'rdx_%s' %(parameters['service_id'],)
    external_data_2 = 'rdx_%s' %(parameters['package_id'],)
    


if __name__ == "__main__":
    #main()
    from datetime import datetime,timedelta
    svr = AIRHandler({'transactionId':'65433','externalData1':'data','externalData2':'data'})
    print str(datetime.now())+': start air call'
    #print svr.GetUsageThresholdsAndCounters('254731619189')
    #print svr.setServiceClass('254733431360',97)
    #print svr.getAccumulators('254733431360')
    print svr.getBalanceAndDate('261330494860')
    #print str(datetime.now())+'...done....'
    #print svr.updateOffer('254788268612',19)
    #print svr.getAccumulators('254787440680')
    #print svr.deleteOffer('254735267974',8)
    #print svr.getOffers('254722701852')
