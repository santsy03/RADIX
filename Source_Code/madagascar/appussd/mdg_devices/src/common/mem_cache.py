import memcache
try:
    from configs.config import MEMCACHE_HOSTS
except ImportError:
    MEMCACHE_HOSTS = ['127.0.0.1:11211']


def log(res={}, string='', level='debug'):
    print '%r - %r' % (level, string)


class mem_cached():
    """
    memcache class
    """

    def __init__(self):
        self.server = memcache.Client(MEMCACHE_HOSTS)

    def set(self, key, value, expiry=240):
        """
        This method is used to set a new value
        in the memcache server.
        """
        resp = self.server.set(key, value, expiry)
        if int(resp) != 0:
            log({}, 'MEMCACHE: Set -- %s -- %s' % (key, str(expiry)), 'info')
        else:
            log({}, 'MEMCACHE: Error: failed to set. %s' % (resp), 'info')

    def set_all(self, _dict, expiry):
        """
        sets multiple vales in memcaceh server
        """
        num = len(_dict)
        log({}, 'MEMCACHE: Setting %s imeis ' % (num), 'info')
        resp = self.server.set_multi(_dict, expiry)

    def get(self, key):
        """
        This method is used to retrieve a value
        from the memcache server
        """
        return self.server.get(key)

    def delete(self, key):
        """
        This method is used to delete a value from the
        memcached server. Lazy delete
        """
        self.server.delete(key)

    def replace(self, key, value):
        """
        This method is used to update a value in the
        memcached server
        """
        resp = self.server.replace(key, value)
        if int(resp) != 0:
            log({}, 'replaced {0} with {1}'.format(key, value), 'debug')
        else:
            log({}, 'replace failed', 'error')


if __name__ == '__main__':
    i = mem_cached()
    #y= i.set('simon','kenya')
    f = i.get('simon')
    print f
