import logging
from datetime import tzinfo,timedelta,datetime
from copy import deepcopy
from tools import *
from utilities.secure.core import decrypt
from configs.config import databases as db

class AIRHandler:
      logger = logging.getLogger('AIRHandler')
      originHostName = 'web2sms2'
      def __init__(self,origNodeType='ibundles',origHost='dbndls',transactionId=None):
                self.origNodeType = origNodeType
                self.origHost = origHost
                self.url="http://web2sms:w3b2sms@172.30.16.17:10010/Air"
                self.basicRequest =  {}
                self.basicRequest[ 'originNodeType' ] = origNodeType
                self.basicRequest[ 'originHostName' ] = origHost
                self.basicRequest[ 'originTransactionID' ] = '18282'
                if transactionId:
                  self.basicRequest[ 'originTransactionID' ]= transactionId
                self.USER_AGENT = 'IVR/3.1/1.0'
                self.transport = Transporter( Transporter.HTTP, self.USER_AGENT )
                self.airServer = xmlrpclib2.ServerProxy( self.url, self.transport, verbose=False )

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

      def getAccumulators( self, msisdn ):
                accReq = deepcopy( self.basicRequest )
                accReq[ 'originTimeStamp' ] = self.now()
                accReq[ 'subscriberNumber' ] = msisdn
                Req[ 'subscriberNumberNAI' ] = 1
                self.logger.debug( accReq )
                return self.airServer.GetAccumulators( accReq )

      def updateBalanceAndDate(self,msisdn,amount,hostName=originHostName):
          updReq = deepcopy( self.basicRequest )
          updReq[ 'originHostName' ] = hostName
          updReq[ 'originTimeStamp' ] = self.now()
          updReq[ 'subscriberNumber' ] = msisdn
          updReq[ 'transactionCurrency' ] = 'KES'
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

      def getAllowedServiceClasses( self, msisdn ):
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

      def updateDedicatedAccount( self, msisdn, amount, action, account, expiryDate, hostName=originHostName):
          '''
           expiryDate should be a datetime object eg, dt=datetime(2010, 7, 23, 5, 4, 1) 
           usage examples:
              - updateDedicatedAccount('254733725373',5,'dedicatedAccountValueNew',2,dt)
              - updateDedicatedAccount('254733725373','2','adjustmentAmountRelative',2,dt,'mdsa')
 
          '''        

          updReq = deepcopy( self.basicRequest )
          updReq[ 'originHostName' ] = hostName
          updReq[ 'originTimeStamp' ] = self.now()
          updReq[ 'subscriberNumber' ] = msisdn
          updReq[ 'transactionCurrency' ] = 'KES'
          updReq[ 'subscriberNumberNAI' ] = 1        
          dainfo={'dedicatedAccountID':account,action:str(amount)}
          if action=='dedicatedAccountValueNew':
             dainfo['expiryDate']=expiryDate
          elif action=='adjustmentAmountRelative':
             #dainfo['adjustmentDateRelative']=expiryDate
             dainfo['expiryDate']=expiryDate
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
                self.logger.debug( Req )
                return self.airServer.UpdateServiceClass( Req )

if __name__ == "__main__":
    #main()
    from datetime import datetime
    svr = AIRHandler()
    print str(datetime.now())+': start air call'
    #print svr.getAccumulators('733725373') 
    #print svr.updateBalanceAndDate('254734362490',1) 
    #print svr.getFaFList('254733725373') 
    #print svr.getAccountDetails('254733725373') 
    #print svr.getAllowedServiceClasses('254733725373') 
    #print svr.updateFaFList('254733725373','ADD','736737273',3) 
    #print svr.updateSubscriberSegmentation('254733725373',1,True)
    dt=datetime(2010, 11, 28, 5, 4, 1) 
    print dt
    #print svr.updateDedicatedAccount('254733725373',5,'dedicatedAccountValueNew',2,dt) 
    #print svr.updateDedicatedAccount('254736194700','2','adjustmentAmountRelative',2,dt,'cyn') 
    #print svr.setServiceClass('254733725373',2) 
    #print svr.setServiceClassTemporary('254733725373',97,dt) 
    #print svr.delServiceClassTemporary('254733725373',97) 
    print svr.getBalanceAndDate('254732840293')
    #print svr.getAccountDetails('254737051790')
    #print svr.getBalanceAndDate('254734415197')
    print str(datetime.now())+'...done....'
