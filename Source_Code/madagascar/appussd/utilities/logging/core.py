def Xlog(resources, text, error=False):
    '''
    logs the text using the logger defined in resources.
    if none defined, prints the results on screen.

    @params: 
        1. resources dict (to check if logger is available)
        2. text to log
        3. log entry type <info/error> as boolean. 
            (default is info)
    '''
    if resources.has_key('logger'):
        logger = resources['logger']
        if error == False:
            logger.error(text)
            print 'ERROR -- %s' % str(text)
        else:
            txt = 'INFO -- %s' % str(text)
            logger.info(txt)
            print text
    else:
        if error:
            print 'ERROR: %s' % str(text)
        else:
            print text


def log(resources, msg, level='debug'):
    """
    logs to either screen or log file depending on setting
    """
    if resources.has_key('logger'):
        eval("resources['logger'].%s(msg)" %level)
    else:
        print '%s-%s' % (level.upper(), msg)

