from unittest import TestCase, main
from mocker import Mocker, ARGS
from kombu.pools import producers
from kombu import Connection


class test_consumer(TestCase):

    def setUp(self,):
        self.resources = {}
        self.exchange = 'test_1'
        connection = Connection('amqp://datauser:hooVee9I@localhost:5672/data')
        self.resources['producers'] = producers[connection]

    def test_send_delivery(self):
        from data_provisioning.src.core.server_data_provisioning import Consumer
        msg = {'key':'value'}
        routing_key = 'video1.*'
        resources = self.resources
        resources['logger'] = None
        test_id = 1
        consumer = Consumer(test_id, resources)
        consumer.send_delivery(resources, routing_key, msg)

    def test_handle_delivery_success(self):
        '''
        this test case handles the scenario where the subscriber is successfully provisioned
        '''
        from data_provisioning.src.core.server_data_provisioning import Consumer

        response = {}
        response['status'] = 5
        response['resp'] = {'status': '5'}

        body = {}
        body['msisdn'] = '254735267974'
        body['package_id'] = 1
        body['transactionId'] = 123
        body['args'] = {'routing_key':'video1.*'}

        body = str(body)
        method = None
        header = None

        mocker = Mocker()
        mock_object = mocker.mock()
        mock_object.send_delivery(ARGS)
        mocker.result(True)

        mock_object.resources['connections']
        mocker.result(True)

        mock_object.logger
        mocker.result(True)

        mock_object.resources['producers']
        mocker.result(True)


        mocker1 = Mocker()
        mock_process_request = mocker1.replace('data_provisioning.src.core.core.processRequest')
        mock_process_request(ARGS)
        mocker1.result(response)

        mocker2 = Mocker()
        mock_channel = mocker2.mock()
        mock_channel.basic_ack(ARGS)
        mocker2.result(True)

        mocker3 = Mocker()
        mock_method = mocker3.mock()
        mock_method.delivery_tag
        mocker3.result(3)

        mocker.replay()
        mocker1.replay()
        mocker2.replay()
        mocker3.replay()

        Consumer.handle_delivery.im_func(mock_object, mock_channel, mock_method, header, body)

        mocker.restore()
        mocker.verify()
        mocker1.restore()
        mocker1.verify()
        mocker2.restore()
        mocker2.verify()
        mocker3.restore()
        mocker3.verify()


if __name__ == '__main__':
    main()
