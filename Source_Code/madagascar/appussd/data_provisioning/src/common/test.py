def test_getSubscriberType():
    from core import getSubscriberType
    resources = {}
    parameters = {'msisdn':'254731769049'}
    resources['parameters'] = parameters
    print getSubscriberType(resources)


if __name__ == '__main__':
    test_getSubscriberType()
