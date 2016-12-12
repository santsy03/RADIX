#!/usr/bin/env python
import pika
import uuid

class Queue_Client(object):
    def __init__(self, queue_name,request):
        from pika.adapters import SelectConnection
        self.queue = queue_name
        self.response = None
        self.channel = None
        self.request = request
        self.corrId = str(uuid.uuid4())
        self.callBackQueue = None
        self.connection = None
        self.connection = SelectConnection(pika.ConnectionParameters(host='127.0.0.1'),self.on_response_connected)
        self.connection.ioloop.start()

    def on_response(self,ch,method,props,body):
        if self.corrId == props.correlation_id:
            self.response = body
            self.connection.close()
            self.connection.ioloop.start()

    def on_response_connected(self,connection):
        print 'connected ..'
        self.connection = connection
        self.connection.channel(self.on_channel_open)

    def on_channel_open(self,channel):
        print 'channel opened'
        self.channel = channel
        self.channel.queue_declare(queue=self.queue,durable=True,exclusive=False,auto_delete=False,callback=self.on_queue_declared)

    def on_queue_declared(self,frame):
        self.channel.basic_publish(exchange='',routing_key=self.queue,properties = pika.BasicProperties(),body=str(self.request))
        #self.channel.queue_purge(queue='events_queue_dev')
        self.connection.close()
        print 'message delivered'

if __name__ == '__main__':
    msg = '261336173681|1|2|516|2,5,MyMeg 20,0,0'
    print Queue_Client('events_queue_pro',msg)
