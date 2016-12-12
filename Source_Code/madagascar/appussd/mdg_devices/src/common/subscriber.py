"""
Handles subscriber logic. 
"""

from mdg_devices.src.common.sadm import SoapConnector
from mdg_devices.src.common.ema import get_imei
from mdg_devices.src.configs.general import IMEI_SOURCE



class Subscriber(object):
    """
    class to handle subscribers
    """
    def __init__(self, msisdn=None, t_id=None, con=None, logger=None):
        """ initialize"""
        self.msisdn = msisdn
        self.transaction_id = t_id
        self.con = con
        self.logger = logger
        if not t_id:
            self._get_transaction_id()

    def _get_soap(self):
        return SoapConnector()

    def get_imei_sadm(self):
        """
        calls SADM to get imei of the sub
        """
        params = {'msisdn' : '+'+self.msisdn}
        try:
            soap = self._get_soap()
            resp = dict(soap.get_subscriber_info(params))
            self.imei = resp['imei']
        except Exception, err:
            pass

    def get_imei_ema(self):
        """
        calls ema to get the imei of the sub
        """
        try:
            self.imei = get_imei(self.msisdn, self.logger)
        except Exception, err:
            pass

    def get_imei(self):
        """
        calls the appropriate node for IMEI
        """
        if IMEI_SOURCE == 'EMA':
            return self.get_imei_ema()
        else:
            return self.get_imei_sadm()

    def _get_package_id(self):
        """
        gets the package id allowed for this imei
        """
        pass

    def _get_transaction_id(self):
        """
        gets the transaction Id for this sub's
        transaction
        """
        sql = 'select devices_sqc.nextval from dual'
        try:
            cur = self.con.connection().cursor()
            cur.execute(sql)
            ret = cur.fetchall()
            t_id = ret[0][0]
            self.transaction_id = str(t_id)
        except Exception, err:
            raise err

