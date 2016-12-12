"""
Handles retailer logic. 
"""

from mdg_devices.src.common.whitelists import Whitelist

class Retailer(object):
    """
    class to handle retailer
    """
    def __init__(self, retailer=None):
        """ initialize"""
        self.msisdn = retailer
        self.wlist = Whitelist('retailer', retailer)
        self.t_id = None

    def upload_retailers(self):
        """
        gets the retailers from db
        and loads them to memcache
        """
        self._select_all()
        self._update_cache()

    def _select_all(self):
        """
        selects all from retailers table
        """
        pass

    def _update_cache(self):
        """
        puts the retailers to cache
        """
        pass

    def whitelisted(self):
        """
        checks if retailer has been whitelisted
        """
        self.wlist.run_action()
        self.wlist.exists
