from unittest import TestCase,main
from datetime import datetime, timedelta

sampleDedicatedAccountDetails = [{'dedicatedAccountID': 1, 'dedicatedAccountValue1': '0', 'expiryDate': "<DateTime '99991231T00:00:00+1200' at d418560>"}, {'dedicatedAccountID': 3, 'dedicatedAccountValue1': '0', 'expiryDate': "<DateTime '99991231T00:00:00+1200' at d4185a8>"}, {'dedicatedAccountID': 6, 'dedicatedAccountValue1': '0', 'expiryDate': "<DateTime '99991231T00:00:00+1200' at d4185f0>"}, {'dedicatedAccountID': 7, 'dedicatedAccountValue1': '0', 'expiryDate': "<DateTime '99991231T00:00:00+1200' at d418638>"}, {'dedicatedAccountID': 8, 'dedicatedAccountValue1': '8', 'expiryDate': "<DateTime '20121219T12:00:00+0000' at d418680>"}, {'dedicatedAccountID': 10, 'dedicatedAccountValue1': '0', 'expiryDate': "<DateTime '99991231T00:00:00+1200' at d4186c8>"}]

class test_airHandler(TestCase):
    def test_convertAirDateTimeTZ1200(self,):
        from sacc.src.common.airHandler import convertAirDateTime,GMT330
        from datetime import datetime

        #airDateTime = '20121214T12:00:00+0000'
        airDateTime = '99991231T00:00:00+1200'
        #expected = datetime(9999,12,31,0,0,0,tzinfo=GMT330())
        expected = datetime(9999,12,31,0,0,0)
        actual = convertAirDateTime(airDateTime)
        self.assertEqual(expected,actual)

    def test_convertAirDateTimeTZ0000(self,):
        from sacc.src.common.airHandler import convertAirDateTime,GMT330
        from datetime import datetime

        airDateTime = '20121214T12:00:00+0000'
        #expected = datetime(2012,12,14,12,0,0,tzinfo=GMT330())
        expected = datetime(2012,12,14,12,0,0)
        actual = convertAirDateTime(airDateTime)
        self.assertEqual(expected,actual)

    def test_getDedicatedAccountDetailsExists(self):
        '''tests whether the getAccountDetails method returns the correct details for dedicatedAccountDetails listing 
        with the details for the given dedicatedAccountId'''
        from sacc.src.common.airHandler import getDedicatedAccountDetails
        dedicatedAccountDetails = sampleDedicatedAccountDetails
        dedicatedAccountId = 7
        actual = getDedicatedAccountDetails(dedicatedAccountDetails,dedicatedAccountId) 
        expected = dedicatedAccountDetails[3]
        self.assertEqual(actual,expected)

    def test_getDedicatedAccountDetailsDoesNotExist(self):
        '''tests whether the getAccountDetails method returns the correct details for dedicatedAccountDetails listing 
        with the details for the given dedicatedAccountId'''
        from sacc.src.common.airHandler import getDedicatedAccountDetails
        dedicatedAccountDetails = sampleDedicatedAccountDetails
        dedicatedAccountId = 12
        actual = getDedicatedAccountDetails(dedicatedAccountDetails,dedicatedAccountId) 
        expected = False
        self.assertEqual(actual,expected)

def test_set_bundle_details():
    from sacc.src.common.core import setup, set_bundle_details
    from datetime import datetime, timedelta
    resources = setup()
    parameters = {}
    parameters['msisdn'] = '254735267974'
    parameters['packageId'] = 1
    parameters['expiry'] = datetime.now() + timedelta(days = 2)
    balance = {'volume': '10'}
    parameters['balance'] = balance
    parameters['volumeString'] = '20 MB'
    parameters['transactionId'] = '5555'
    parameters['packageName'] = '10 MB Daily'
    resources['parameters'] = parameters
    set_bundle_details(resources)

def test_get_bundle_details():
    from sacc.src.common.core import setup, get_bundle_details
    resources = setup()
    parameters = {}
    parameters['msisdn'] = '254735267974'
    resources['parameters'] = parameters
    resources = get_bundle_details(resources)
    print str(resources['parameters'])

if __name__ == '__main__':
    #test_set_bundle_details()
    test_get_bundle_details()
