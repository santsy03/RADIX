from utilities.metrics.metricHandler import heartBeat
from utilities.logging.core import log

def send_metric(metrics, metric_type='timer'):
    '''wrapper function for sending metrics.
    invokes respective metric sending func based on
    type of metric

    @params: metrics dict, and metric_type
    '''
    if metric_type == 'timer':
        period(metrics)
    if metric_type == 'counter':
        beat(metrics)


def beat(metrics):
    '''sends counter metrics

    @param: dict containing name_space key
    '''
    _metric = metrics['name_space']
    hb = heartBeat()
    try:
        hb.beat(_metric)
    except Exception, e:
        err = '[ERROR] Sending beat metric failed', str(e)
        log({}, err, error=True)
    else:
        log({}, 'Metric sent: %s' % _metric )


def period(metrics):
    '''sends timer metrics

    @param: dict containing name_space and 
    start_time keys
    '''
    _metric = metrics['name_space']
    start_time = metrics['start_time']
    hb = heartBeat()
    try:
        hb.period(_metric, start_time)
    except Exception, e:
        err = '[ERROR] Sending period metric failed', str(e)
        log({}, err, error=True)
    else:
        log({}, 'Metric sent: %s' % _metric )

def response_time(metric, start_time, logger = None):
    '''
    sends a timing message to the metrics server
    '''
    hb = heartBeat()
    try:
        hb.period(metric, start_time)
    except Exception, e:
        if logger:
            err = "ERROR Sending period metric failed: %s" % (str(e))
            logger.error(err)
        else:
            print str(e)
    else:
        if logger:
            logger.debug("metric sent %s" % (metric))
        else:
            print "metric sent %s" % (metric)


def count(metric):
    hb = heartBeat()
    try:
        hb.beat(metric)
    except Exception, e:
        err = '[ERROR] Sending beat metric failed', str(e)
        log({}, err, error=True)
    else:
        log({}, 'Metric sent: %s' % metric )

