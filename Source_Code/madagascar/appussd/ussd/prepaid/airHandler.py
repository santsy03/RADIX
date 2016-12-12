import logging
from datetime import tzinfo,timedelta,datetime
from copy import deepcopy
from tools import *
#import pytz

from ussd.services.common.secure.secure import decrypt
from ussd.configs.core import air

username = decrypt(air['airUser']) #'USSDMG'
password = decrypt (air['airPass'])#USSDMG'
host = air['airHost']
url = 'http://%s:%s@172.25.154.86:10010/Air' %(str(username),str(password))
#url = 'http://%s:%s@172.23.1.100:10318/Air' %(str(username),str(password))

class AIRHandler:
      logger = logging.getLogger('AIRHandler')
      originHostName = host
      def __init__( self,origNodeType='EXT',origHost= host):
                self.origNodeType = origNodeType
                self.origHost = origHost
                self.url= url
                self.basicRequest =  {}
                self.basicRequest[ 'originNodeType' ] = origNodeType
                self.basicRequest[ 'originHostName' ] = origHost
                self.basicRequest[ 'originTransactionID' ] = '18282'
                self.USER_AGENT = 'IVR/3.1/1.0'
                self.transport = Transporter( Transporter.HTTP, self.USER_AGENT )
                self.airServer = xmlrpclib2.ServerProxy( self.url, self.transport, verbose=False)

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

      def updateFaFList( self, msisdn, action, fafNum, fafInd, service_name,owner='Subscriber'):
                """ fafAction have to be one of below option
                fafAction: ADD, SET, DELETE
                """
                Req = deepcopy( self.basicRequest )
                Req[ 'originTimeStamp' ] = self.now()
                Req[ 'subscriberNumber' ] = msisdn
                Req[ 'fafAction' ] = action
                Req[ 'originOperatorID' ] = service_name
                Req[ 'subscriberNumberNAI' ] = 1
                Req[ 'chargingRequestInformation' ] = {'chargingType':2}
                Req[ 'fafInformation' ] = { 'fafNumber': fafNum ,'fafIndicator':fafInd, 'owner': owner }
                self.logger.debug( Req )
                return self.airServer.UpdateFaFList( Req )

      def updateFaFListWithoutCharge( self, msisdn, action, fafNum, fafInd, service_name,owner='Subscriber'):
                """ fafAction have to be one of below option
                fafAction: ADD, SET, DELETE
                """
                Req = deepcopy( self.basicRequest )
                Req[ 'originTimeStamp' ] = self.now()
                Req[ 'subscriberNumber' ] = msisdn
                Req[ 'fafAction' ] = action
                Req[ 'originOperatorID' ] = service_name
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
          updReq[ 'transactionCurrency' ] = 'MGA'
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

      def setServiceClass( self, msisdn, sc ,service_name,tarrif_name):
                Req = deepcopy( self.basicRequest )
                Req[ 'originTimeStamp' ] = self.now()
                Req[ 'subscriberNumber' ] = msisdn
                Req[ 'serviceClassAction' ] = 'SetOriginal'
                Req[ 'subscriberNumberNAI' ] = 1
                Req[ 'externalData1' ] = service_name
                Req[ 'externalData2' ] = tarrif_name
                Req[ 'serviceClassNew' ] = sc
                Req['chargingRequestInformation'] = {'chargingType':2}
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
    #print svr.updateBalanceAndDate('2617272618',-100)
    #print svr.getFaFList('261337150441')
    print svr.getBalanceAndDate('261337150441')
    #print svr.getBalanceAndDate('261330770007')
    #print  '*************************************************'
    #print svr.getAccountDetails('254733431360') 
    #print svr.getAllowedServiceClasses('254733558117') 
    #print svr.updateFaFList('261337150441','ADD','0337272618',1,'ussd2mgFnFApplication')
    #print svr.updateFaFListWithoutCharge('261337150441','DELETE','0337272618',1,'ussd2mgFnFApplication')
    #print svr.updateSubscriberSegmentation('254733725373',1,True)
    #dt=datetime(2010, 7, 28, 5, 4, 1) 
    #print svr.updateDedicatedAccount('254733725373',5,'dedicatedAccountValueNew',2,dt) 
    #print svr.updateDedicatedAccount('254733725373','2','adjustmentAmountRelative',2,dt,'mdsa') 
    #print svr.setServiceClass('261337150441',6,'changeTarrifPlan','Jiaby Jiaby') 
    #print svr.setServiceClassTemporary('261337272618',6) 
    #print svr.delServiceClassTemporary('254733725373',97) 
    #print svr.getBalanceAndDate('254735193646')
    #print str(datetime.now())+'...done....'
