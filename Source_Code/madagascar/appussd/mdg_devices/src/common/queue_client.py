import json
from kombu.pools import producers
from kombu import Connection

from mdg_devices.src.configs.general import QUEUES

class QueueClient(object):
    def __init__(self, 
            routing_key = QUEUES['routing_key'],
            exchange = QUEUES['exchange'], 
            log = None,
            ):
        self.routing_key = routing_key
        self.exchange = exchange
        self.log = log
        self._create_pool()

    def _create_pool(self):
        self.con = Connection(hostname='127.0.0.1',
                virtual_host='data',
                userid='rabbitmg',
                port=5672,
                password='mgrabbituser')
        self._create_exchange()
        self.pool_ = producers[self.con]

    def publish(self, message):
        self.message = message
        if self._publish():
            return True

    def _publish(self):
        try:
            msg = self.message
            cdr = 'PUBLISHING: %s' % (msg)
            self._log(cdr)
            with self._acquire() as producer:
                producer.publish(json.dumps(msg),
                        exchange = self.exchange,
                        serializer = 'json',
                        routing_key = self.routing_key)
                self._release(producer)
            cdr = 'PUBLISHED: %s' % (msg)
            self._log(cdr)
        except Exception, err:
            raise err

    def _release(self, con):
        self.pool_.release(con)

    def _acquire(self):
        return self.pool_.acquire( block=True)

    def _log(self, logging):
        try:
            self.log.info(logging)
        except:
            print logging

    def _create_exchange(self):
        self.channel = self.con.channel()
        self.channel.exchange_declare(self.exchange,
                type='topic', durable=True,
                auto_delete=False)
        self._log(self.channel)

if __name__ == '__main__':
    f = QueueClient()
    f.publish("{'tags':'many'}")
