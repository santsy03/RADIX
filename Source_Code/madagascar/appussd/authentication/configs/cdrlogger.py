'''
cdr logging
'''
def log_cdr(resources, msg, level='debug'):
    try:
        from utilities.logging.core import log
        if 'logger' in resources:
            _logger = resources['logger']
        else:
            _logger = False
        resources['logger'] = resources['cdr_logger']
        log(resources, msg, level)

    except Exception, err:
        print 'ERROR - log_cdr() - %r' % err
        raise err

    finally:
        if _logger:
            resources['logger'] = _logger
        else:
            del(resources['logger'])

