#!/usr/bin/env python
import pika
import uuid
from utilities.logging.core import log

class Publisher(object):
    def __init__(self,request,resources):
        from pika.adapters import SelectConnection
        self.resources = resources
        self.queue = resources['parameters']['queue_name']
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
        try:
            self.connection = connection
            self.connection.channel(self.on_channel_open)
        except Exception, err:
            error = 'operation: on_response_connected,error:%s' %str(err)
            log(self.resources, error,'error')

    def on_response_channel_open(self,channel):
        try:
            self.responseChannel = channel
            result = self.responseChannel.queue_declare(exclusive=True,callback=self.on_response_queue_declared)
        except Exception, err:
            error = 'operation: on_response_connected,error:%s' %str(err)
            log(self.resources, error,'error')

    def on_connected(self,connection):
        self.connection = connection
        self.connection.channel(self.on_channel_open)

    def on_channel_open(self,channel):
        try:
            self.channel = channel
            self.channel.queue_declare(queue=self.queue,durable=True,exclusive=False,auto_delete=False,callback=self.on_queue_declared)
        except Exception, err:
            error = 'operation: on_channel_open,error:%s' %str(err)
            log(self.resources, error,'error')

    def on_queue_declared(self,frame):
        try:
            self.channel.basic_publish(exchange='',routing_key=self.queue,properties = pika.BasicProperties(),body=str(self.request))
            self.connection.close()
            info =  'message delivered, %s' %str(self.request)
            log(self.resources, info, 'info')
        except Exception, err:
            error = 'operation: on_queue_declared, error:%s' %str(err)
            log(self.resources, error,'error')

if __name__ == '__main__':
    msg = '200||0||10 MB||22-10-2012T12:00:00||50 MB Bundle'
