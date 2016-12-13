import memcache
from configs.config import MEMCACHE_HOSTS
from twisted.python import log

class SessionManager(object):
    """Memcache-based session manager"""

    def __init__(self, hosts=MEMCACHE_HOSTS, expiry=0, prefix=''):
        self.HOSTS = hosts
        self.HOSTS_VERBOSE = "|".join(hosts)
        self.MEMCACHE = memcache.Client(hosts)
        self.EXPIRY = expiry
        self.PREFIX = prefix
        self.EXPIRY_VERBOSE = ("{:.2}min".format(self.EXPIRY/60.0)
                               if self.EXPIRY else "Never")
        print "SET UP SESSIONS CACHE: %r" % self 

    def real_key(self, key):
        return "{}{}".format(self.PREFIX, key)

    def __setitem__(self, key, value):
        try:
            self.MEMCACHE.set(self.real_key(key), value, time=self.EXPIRY)
        except Exception, exc:
            log.err("SessionCache:Set-Error")
            raise(exc)

    def __getitem__(self, key):
        try:
            sess_data = self.MEMCACHE.get(self.real_key(key))
        except Exception, exc:
            log.err("SessionCache:Get-Error")
            raise(exc)
        if sess_data is not None:
            return sess_data
        else:
            raise KeyError("Session not found with key:{}".format(key))

    def __delitem__(self, key):
        try:
            resp = self.MEMCACHE.delete(self.real_key(key))
        except Exception, exc:
            log.err("SessionCache:Delete-Error")
            raise(exc)
        return resp

    def __repr__(self):
        _args = (self.HOSTS_VERBOSE, self.EXPIRY_VERBOSE, self.PREFIX)
        return "SessionManager[Hosts:[{}]/Expiry:{}:Prefix:{}]".format(*_args)
    __str__ = __unicode__ =  __repr__

