'''
module with the queueing client
'''

from mg_aapcn_me2u.src.configs.config import QUEUES as queues
from mg_aapcn_me2u.src.configs.config import DEBUG

import pika
import uuid

class InternetMe2uClient(object):
    '''
    class to enqueue all prov requests
    for me2u
    '''

    def __init__(self, request):
        '''
        intialise a few global variables
        '''
        from pika.adapters import SelectConnection
        if DEBUG:
            self.queue = queues['test']
        else:
            self.queue = queues['prod']
        self.response = None
        self.channel = None
        self.request = request
        self.corr_id = str(uuid.uuid4())
        self.callBackQueue = None
        self.connection = None
        self.connection = SelectConnection(pika.ConnectionParameters\
                ( host = '127.0.0.1'),
                self.on_response_connected)
        self.connection.ioloop.start()

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
            self.connection.close()
            self.connection.ioloop.start()

    def on_response_connected(self, connection):
        print 'connected ..'
        self.connection = connection
        self.connection.channel(self.on_channel_open)

    def on_response_channel_open(self, channel):
        self.responseChannel = channel
        result = self.responseChannel.queue_declare\
                (exclusive=True)

    def on_connected(self, connection):
        self.connection = connection
        self.connection.channel(self.on_channel_open)

    def on_channel_open(self, channel):
        '''
        called when rabbit MQ has opened our channel
        '''
        print 'channel opened'
        self.channel = channel
        self.channel.queue_declare(queue=self.queue, 
                durable = True,
                exclusive = False,
                auto_delete = False,
                callback = self.on_queue_declared)

    def on_queue_declared(self, frame):
        '''
        called when rabbitMQ tells us our queue has been 
        declared. Frame is the response from rabbitMQ
        '''
        self.channel.basic_publish(exchange='', 
                routing_key = self.queue,properties = pika.BasicProperties(),
                body=str(self.request))
        self.connection.close()
        print 'message delivered'

if __name__ == '__main__':
    #sender_msisdn, recipient, amount, pin, lang
    #msg format = sender_msisdn||recipient||amount||pin||lang
    _msg = "x||y||z||ussd"
    print InternetMe2uClient(_msg)

