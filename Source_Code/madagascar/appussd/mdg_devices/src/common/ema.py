import telnetlib
from mdg_devices.src.configs.ema import (IP, PORT, TIMEOUT,
        USER, PASSWORD)

def get_imei(msisdn, log):
    try:
        tn = telnetlib.Telnet(IP, PORT, TIMEOUT)
        tn.read_until('Enter command:')
        tn.write('LOGIN:%s:%s;\n' % (USER, PASSWORD))
        tn.read_until('Enter command:')
        tn.write('GET:HLRSUB:MSISDN,%s:IMEISV;\n' % (str(msisdn)))
        resp = tn.read_until('Enter command:')
        tn.close()
        cdr = '%s EMA Resp: %s' % (msisdn, str(resp))
        if log:
            log.info(cdr)
        device_imei = False
        if 'IMEISV' in resp:
            device_imei = resp.split(':')[3].split(';')[0].split(',')[1]
            return device_imei[:14]
    except Exception, err:
        error = ('process_ema_request, error:%s' % (str(err)))
        if log:
            log.error(error)
        raise err
