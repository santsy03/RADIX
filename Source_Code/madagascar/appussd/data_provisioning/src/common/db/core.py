import cx_Oracle

def debug(msg):
    from data_provisioning.src.configs.core import debug
    if debug:
        print '[debug] : %s' %str(msg)

def getConnection(resources, db_name='connections'):
    '''
    retrieves a connection object from the given connection pool
    '''
    while True:
        try:
            connection = resources[db_name].acquire()
            resp =  connection.ping()
            if resp == None:
                return connection
            else:
                resources[db_name].drop(connection)
        except cx_Oracle.Error, err:
            ora_error = '''operation:utilities.db.get_connection, desc: failed to\n
                retrieve connection, error: %s''' % err
            log(resources, ora_error, 'error')
            resources[db_name].drop(connection)
        except AttributeError, err:
            connection = resources[db_name].connection()
            return connection
        except Exception, err:
            conn_error = '''operation:utilities.db.get_connection, desc: failed to\n
                retrieve connection, error: %s''' % err
            log(resources, conn_error, 'error')
            resources[db_name].drop(connection)

