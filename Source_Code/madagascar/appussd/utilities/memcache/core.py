from utilities.metrics.core import send_metric
from utilities.metrics.config import memc_hits
from utilities.metrics.config import memc_failed
from utilities.logging.core import log
from configs.config import MEMCACHE
try:
    import memcache
except ImportError:
    log( {}, '!! Memcache Python Client not installed !!', 'error' )

class MemcacheHandler:
    def __init__(self, hosts=[MEMCACHE['host']]):
        self.memc_client = memcache.Client(hosts, debug=1, socket_timeout=3)

    def set(self, key, value, retention_period=int(MEMCACHE['retention_period']) ):
        memc_metrics = {}
        memc_metrics['name_space'] = memc_hits
        memc = self.memc_client
        memc_set = memc.set( key, value, time=int(retention_period) )
        if str(memc_set) != '0':
            log({}, 'MEMCACHE: Set -- %s -- %s -- %s' % (key, value, 
                str(retention_period)), 'info')
            send_metric(memc_metrics, 'counter')
            del(memc_metrics)
        else:
            log({}, 'MEMCACHE: Error: failed to set. %s' % (memc_set), 'error')
            memc_metrics['name_space'] = memc_failed
            send_metric(memc_metrics, 'counter')
            del(memc_metrics)
    def get(self, key):
        memc = self.memc_client
        return memc.get(key)

    def delete(self, key):
        memc = self.memc_client
        if memc.delete(key) != 0:
            # Nonzero on success.
            log( {}, ' MEMCACHE: Successfully deleted %s' % str(key) )
        else:
            log( {}, ' MEMCACHE: Could not delete %s' % str(key), 'error' )

    def flush_all(self):
        memc = self.memc_client
        memc.flush_all()
        log( {}, ' MEMCACHE: Memory flushed', 'info' )
