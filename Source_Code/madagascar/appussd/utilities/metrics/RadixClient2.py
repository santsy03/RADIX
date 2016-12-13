from __future__ import absolute_import
import random
from socket import socket, AF_INET, SOCK_DGRAM
import time

__version__ = '1'

Radix_HOST = '127.0.0.1'
Radix_PORT = 10000
Radix_SAMPLE_RATE = None
Radix_BUCKET_PREFIX = None

def counter(bucket, delta=1, sample_rate=None):
    _Radix.incr(bucket, delta, sample_rate)


def timer(bucket, ms, sample_rate=None):
    _Radix.timing(bucket, ms, sample_rate)

class RadixClient(object):

    def __init__(self, host=None, port=None, prefix=None, sample_rate=None):
        self._host = host or Radix_HOST
        self._port = port or Radix_PORT
        self._sample_rate = sample_rate or Radix_SAMPLE_RATE
        self._socket = socket(AF_INET, SOCK_DGRAM)
        self._prefix = prefix or Radix_BUCKET_PREFIX
        if self._prefix and not isinstance(self._prefix, bytes):
            self._prefix = self._prefix.encode('utf8')

    def incr(self, bucket, delta=1, sample_rate=None):
        """Increment a counter by delta.
        """
        value = str(delta).encode('utf8') + b'|c'
        self._send(bucket, value, sample_rate)

    def _send(self, bucket, value, sample_rate=None):
        """Format and send data to Server.
        """
        bucket = bucket if isinstance(bucket, bytes) else bucket.encode('utf8')
        sample_rate = sample_rate or self._sample_rate
        if sample_rate and sample_rate < 1.0 and sample_rate > 0:
            if random.random() <= sample_rate:
                value = value + b'|@' + str(sample_rate).encode('utf8')
            else:
                return
        stat = bucket + b':' + value
        if self._prefix:
            stat = self._prefix + b'.' + stat
        self._socket.sendto(stat, (self._host, self._port))

    def timing(self, bucket, ms, sample_rate=None):
        """Creates a timing sample.
        """
        value = str(ms).encode('utf8') + b'|ms'
        self._send(bucket, value, sample_rate)

def init_Radix(settings=None):
    """Initialize global Radix client.
    """
    global _Radix
    global Radix_HOST
    global Radix_PORT
    global Radix_SAMPLE_RATE
    global Radix_BUCKET_PREFIX

    if settings:
        Radix_HOST = settings.get('Radix_HOST', Radix_HOST)
        Radix_PORT = settings.get('Radix_PORT', Radix_PORT)
        Radix_SAMPLE_RATE = settings.get('Radix_SAMPLE_RATE',
                                          Radix_SAMPLE_RATE)
        Radix_BUCKET_PREFIX = settings.get('Radix_BUCKET_PREFIX',
                                            Radix_BUCKET_PREFIX)
    _Radix = RadixClient(host=Radix_HOST, port=Radix_PORT,
                           sample_rate=Radix_SAMPLE_RATE, prefix=Radix_BUCKET_PREFIX)
    return _Radix

_Radix = init_Radix()
