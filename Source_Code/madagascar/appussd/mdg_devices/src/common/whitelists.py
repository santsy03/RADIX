"""
File to handle all whitelist logic
"""
from urllib2 import urlopen, Request

from mdg_devices.src.configs.status import STATUS
from mdg_devices.src.common.mem_cache import mem_cached as mem
from mdg_devices.src.configs.general import TWISTED


class Whitelist(object):
    """
    class to handle all whitelists
    """
    def __init__(self, action, action_object, con=None,
            log=None):
        """
        builds the class objects
        """
        self.action = action
        self.action_object = str(action_object)
        self.con = con
        self.log = log
        self.cache = mem()
        self.retailer_prefix = 'Ret_'
        self.imei_prefix = 'Imei_'
        self.control = 'Devices'


    def run_action(self, external=True):
        self.external = external
        if self.action == 'imei':
            self._process_imei()
        elif self.action == 'retailer':
            self._process_retailer()
        elif self.action == 'populate_imei':
            self._populate_imeis()
        elif self.action == 'populate_retailer':
            self._populate_retailers()
        elif self.action == 'use':
            self._mark_used()

    def _process_imei(self):
        '''
        process the imei
        '''
        control = self.cache.get(self.control+'_IMEI')
        port = TWISTED['PORT']
        url = 'http://127.0.0.1:%s/CACHE?action=imeis' % (str(port))
        self._check_imei_from_cache()
        if self.cached_imei:
            self.cached_imei = eval(self.cached_imei)
        self._check_used_imei()
        if self.action_object in self.used_imei:
            self.cached_imei = {'state': int(STATUS['imei_unavailable'])}
        if self.cached_imei:
            cdr = 'processed IMEI: %s, DETAILS: %s ' % (str(self.action_object),
                    str(self.cached_imei))
        else:
            cdr = 'IMEI %s not found in the cache_whitelist' % str(self.action_object)
            #fire http to repopulate memcache
            urlopen(url)
            self._check_imei_from_db()
        self._log(cdr, 'info')

    def _mark_used(self):
        '''
        marks imei as used
        '''
        self._process_imei()
        key = self.imei_prefix+str(self.action_object)[:14]
        self.cached_imei['state'] = int(STATUS['imei_unavailable'])
        value = str(self.cached_imei)
        self.cache.set(key, value)
        cdr = 'IMEI: %s, Marked as used' % (str(self.action_object),
                )
        self._log(cdr, 'info')

    def _process_retailer(self):
        '''
        process the retailer
        '''
        port = TWISTED['PORT']
        url = 'http://127.0.0.1:%s/CACHE?action=retailers' % (str(port))
        self.cached_retailer = False
        self.retailer_found = False
        self._check_retailer_from_cache()
        if  self.cached_retailer:
            #self.cached_retailer = eval(self.cached_retailer)
            #if self.action_object in self.cached_retailer:
            self.retailer_found = True
            cdr = 'RETAILER %s found in the whitelist' % str(self.action_object)
        else:
            #if not self.retailer_found:
            cdr = 'RETAILER %s not found in the whitelist' % str(self.action_object)
            #fire http to repopulate memcache
            urlopen(url)
            self._check_retailer_from_db()
        self._log(cdr, 'info')


    def _fetch_imeis_from_db(self):
        """
        gets all imei is on db
        """
        sql = ("select * from whitelist_imei order by imei")
        imei_list = []
        cdr = 'Populate Cache: Checking IMEI from DB.'
        self._log(cdr, 'info')
        try:
            con_object = self.con.connection()
            cursor = con_object.cursor()
            cursor.execute(sql)
            ret = cursor.fetchall()
            cursor.close()
            con_object.close()
            for item in ret:
                imei = {}
                imei['imei'] = item[0][:14]
                imei['range'] = item[1]
                imei['state'] = item[3]
                imei['claim_status'] = item[8]
                imei_list.append(imei)

            self.db_imei = imei_list
        except Exception, err:
            cdr = 'could not check db for IMEI. Error: %s' % str(err)
            self._log(cdr, 'error')
            try:
                cursor.close()
                con_object.close()
            except:
                pass

    def _check_imei_from_db(self):
        """
        checks if imei is on db
        """
        sql = ("select * from whitelist_imei where substr(imei,1,14) = :imei")
        #sql = ("select * from whitelist_imei where imei = :imei")
        params = {'imei': self.action_object}
        cdr = 'Checking IMEI %s from DB.' % (self.action_object)
        self._log(cdr, 'info')
        try:
            con_object = self.con.connection()
            cursor = con_object.cursor()
            cursor.execute(sql, params)
            ret = cursor.fetchall()
            cursor.close()
            con_object.close()
            for item in ret:
                imei = {}
                imei['imei'] = str(item[0])[:14]
                imei['range'] = item[1]
                imei['state'] = item[3]
                imei['claim_status'] = item[8]
                self.cached_imei = imei
        except Exception, err:
            cdr = 'could not check db Error %s. IMEI: %s' % (str(err),
                self.action_object)
            self._log(cdr, 'error')
            try:
                cursor.close()
                con_object.close()
            except:
                pass

    def _fetch_retailers_from_db(self):
        """
        checks if retailer is on db
        """
        retailer_list = []
        cdr = 'Populate Cache: Checking RETAILERS from DB.'
        self._log(cdr, 'info')
        sql = ("select * from whitelist_retailers")
        try:
            con_object = self.con.connection()
            cursor = con_object.cursor()
            cursor.execute(sql)
            ret = cursor.fetchall()
            cursor.close()
            con_object.close()
            for item in ret:
                retailer = item[0]
                retailer_list.append(retailer)
        except Exception, err:
            cdr = 'could not check db for retailer. Error: %s' % str(err)
            self._log(cdr, 'error')
            try:
                cursor.close()
                con_object.close()
            except:
                pass
        self.db_retailer = retailer_list

    def _check_retailer_from_db(self):
        """
        checks if retailer is on db
        """
        retailer_list = []
        cdr = '%s Checking RETAILERS from DB.' % str(self.action_object)
        self._log(cdr, 'info')
        params = {'retailer': self.action_object}
        sql = ("select * from whitelist_retailers where msisdn = :retailer")
        try:
            con_object = self.con.connection()
            cursor = con_object.cursor()
            cursor.execute(sql, params)
            ret = cursor.fetchall()
            cursor.close()
            con_object.close()
            for item in ret:
                self.retailer_found = item
        except Exception, err:
            cdr = '%s could not check db for retailer. Error: %s' % (
                    self.action_object,
                    str(err))
            self._log(cdr, 'error')
            try:
                cursor.close()
                con_object.close()
            except:
                pass

    def _check_imei_from_cache(self):
        """
        gets imei from caches
        """
        cdr = 'Checking IMEI: %s from cache' % (str(self.action_object))
        self._log(cdr, 'info')
        obj = self.imei_prefix + str(self.action_object)[:14]
        self.cached_imei = self.cache.get(obj)

    def _check_used_imei(self):
        """
        gets used imei from cache
        """
        self.used_imei = self.cache.get('used_imei')
        if not self.used_imei:
            self.used_imei = []
        else:
            self.used_imei = eval(self.used_imei)

    def _check_retailer_from_cache(self):
        """
        gets retailer from cache
        """
        cdr = 'Checking RETAILER: %s from cache' % (str(self.action_object))
        self._log(cdr, 'info')
        retailer = str(self.action_object)
        retailers = self.cache.get('retailers')
        if not retailers:
            retailers = []

        if retailer in retailers:
            self.cached_retailer = True

    def _populate_retailers(self):
        """
        sends a signal to the system to populate retailers
        on cache
        """
        control = False
        if not self.external:
            control = self.cache.get(self.control+'_RETAILER')
        to_cache = {}
        control = False
        #to be deleted
        if not control:
            self._fetch_retailers_from_db()
            ret_len = str(len(self.db_retailer))
            cdr = 'Populate Cache: writing %s retailers to cache' % (str(ret_len))
            self._log(cdr, 'info')
            self.cache.set('retailers', self.db_retailer, 0)
            self.cache.set(self.control+'_RETAILER', 'ON',7200)

    def _populate_imeis(self):
        """sends a signal to the system to populate imei
        on cache"""
        control = False
        if not self.external:
            control = self.cache.get(self.control+'_IMEI')
        to_cache = {}
        used_list = []
        control = False
        #to be deleted
        if not control:
            self._fetch_imeis_from_db()
            for item in self.db_imei:
                if item['state'] == STATUS['imei_unavailable']:
                    used_list.append(str(item['imei']))
                else:
                    key = self.imei_prefix+str(item['imei'])
                    value = str(item)
                    to_cache[key] = value
            if not len(to_cache) > 0:
                used_len = len(used_list)
                cdr = 'Populate Cache: writing %s IMEI as used to cache' % (str(used_len))
                self._log(cdr, 'info')
                self.cache.set('used_imei', str(used_list))
            else:
                used_len = str(len(used_list))
                imei_len = str(len(to_cache))
                cdr = ("Populate Cache: writing %s as IMEI used and %s IMEI as available "
                        "to cache" % (str(used_len), str(imei_len)))
                self._log(cdr, 'info')
                to_cache['used_imei'] = str(used_list)
                self.cache.set_all(to_cache, 0)
            self.cache.set(self.control+'_IMEI', 'ON', 1800)

    def _log(self, logging, level=None):
        """
        logs a string
        level can only be info/ debug/ error
        logging is the actual string to be logged
        """
        if not self.log:
            print logging
        elif self.log and level == 'info':
            self.log.info(logging)
        elif self.log and level == 'debug':
            self.log.debug(logging)
        elif self.log and level == 'error':
            self.log.error(logging)

if __name__ == '__main__':
    W = Whitelist('imei', '353070064260702')
    W.run_action()
    W.cached_imei
    W._check_used_imei()
