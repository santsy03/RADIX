debug=True


BASE_URL = 'http://172.30.135.114:4041/SADMWSI/prov'
USER_NAME = 'RadixUSSD'
PASSWORD  = 'RadixUSSD'
URL_ROOT = '?wsdl'

TIP_SERVICE_URL = "http://172.30.135.111:7080/tipws/services/TipService"

CONTEXT = {}

CONTEXT['getSubInfo'] = {}
CONTEXT['getSubInfo']['service'] = 'TipWSIService'
CONTEXT['getSubInfo']['port'] = 'TipService'

CONTEXT['provision'] = {}
CONTEXT['provision']['service'] = 'ProvisioningService'
CONTEXT['provision']['port'] = 'ProvisioningPort'

CONTEXT['de_enroll'] = {}
CONTEXT['de_enroll']['service'] = 'DeEnrollmentService'
CONTEXT['de_enroll']['port'] = 'DeEnrollmentService'

SADM_TIMEOUT = 5

