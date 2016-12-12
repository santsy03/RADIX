def test_enqueue_request():
    from core import enqueue_request
    resources = {}
    parameters = {}
    parameters['msisdn'] = '2617272618'
    parameters['package'] = '1'
    resources['parameters'] = parameters
    return enqueue_request(resources)

if __name__ == '__main__':
    print test_enqueueRequest()
