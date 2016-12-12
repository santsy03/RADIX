#!/usr/bin/env python2.7

def sendMetric(resources):
    '''
    Function for sending Metric
    '''
    from ussd.metrics.metricHandler import heartBeat
    type = resources['type']
    nameSpace = resources['nameSpace']
    roho = heartBeat()
    if type == 'beat':
        #nameSpace = internetTemplate.substitute(package=package)
        nameSpace = nameSpace.replace(' ','')
        roho.beat(nameSpace)
        resp = roho.beat(nameSpace)
    elif type == 'timer':
        nameSpace = nameSpace
        now = resources['start']
        resp = roho.period(nameSpace,now)
    else:
        return 'No metric'

if __name__ == '__main__':
    from datetime import datetime
    resources = {}
    #parameters = {}
    resources['package'] = 'test'
    resources['type'] = 'timer'
    resources['nameSpace'] = 'test.time'
    resources['start'] = datetime.now()
    print sendMetrix(resources)

