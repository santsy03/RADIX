'''
utility database functions
'''
import cx_Oracle
from datetime import datetime, timedelta
from utilities.logging.core import log

def get_connection(resources, db_name='connections'):
    '''
    retrieves a connection object from the given connection pool
    '''
    lookup_counter = 0
    while True:
        lookup_log = "Looking for connection: Attempt: {}".format(lookup_counter)
        log(resources, lookup_log, "debug")
        lookup_counter = lookup_counter + 1
        try:
            connection = resources[db_name].acquire()
	    #db_stats = 'acquired connections: %s, open connections: %s ' %(str(resources[db_name].busy), str(resources[db_name].opened)) 
            #log(resources, db_stats, 'info')
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

def execute_query(resources, sql, params, db_name='connections'):
    '''
    retrieves a database connection and executes the query
    '''
    parameters = resources['parameters']
    start_at = datetime.now()
    connection = get_connection(resources, db_name)
    cursor = connection.cursor()
    complete_at = datetime.now()
    try:
        cursor.execute(sql, params)
        duration = complete_at - start_at
        parameters['cursor'] = cursor
        resources['parameters'] = parameters
        return resources
    except Exception, err:
        sql_exec_error = 'operation: utilities.db.execute_query. error: %s' % str(err)
        log(resources, sql_exec_error, 'error')
        raise err



def call_stored_function(resources, stored_function, return_type, params, db_name='connections'):
    '''
    retrieves a database connection and invokes stored function
    @params:
            1. resources        [M] :  dict with connection object
            2. stored_function  [M] :  name of the SF
            3. return_type      [M] :  the data type returned by the SF.('number','string','timestamp')
            4. params           [M] :  list with the arguments expected by the SF
            5. db_name          [O] :  key in resources with connection object.

    @return: resources with cursor and SF response
    '''
    parameters = resources['parameters']
    start_at = datetime.now()
    connection = get_connection(resources, db_name)
    cursor = connection.cursor()
    complete_at = datetime.now()
    if return_type == 'number':
        ret = cx_Oracle.NUMBER
    elif return_type == 'string':
        ret = cx_Oracle.STRING
    elif return_type == 'timestamp':
        ret = cx_Oracle.TIMESTAMP
    try:
        resp = cursor.callfunc(stored_function, ret, params)
        duration = complete_at - start_at
        cursor.connection.commit()
        cursor.close()
        parameters['stored_func_resp'] = resp
        resources['parameters'] = parameters
        return resources
    except Exception, err:
        sp_exec_error = 'operation: utilities.db.call_stored_function. error: %s' % str(err)
        log(resources, sp_exec_error, 'error')
        raise err


def call_stored_procedure(resources, stored_proc, params, db_name='connections'):
    '''
    retrieves a database connection and invokes a stored procedure
    @params:
            1. resources        [M] :  dict with connection object
            2. stored_proc      [M] :  name of the SP
            3. params           [M] :  list with the arguments expected by the SF
            4. db_name          [O] :  key in resources with connection object.

    @return: resources with cursor and SF response
    '''
    parameters = resources['parameters']
    connection = get_connection(resources, db_name)
    cursor = connection.cursor()
    try:
        resp = cursor.callproc( stored_proc, params )
        cursor.connection.commit()
        cursor.close()
        resources['parameters']['proc_resp'] = resp
        return resources
    except Exception, err:
        sp_err = 'operation: utilities.db.call_stored_procedure - %s' % str(err)
        log(resources, sp_err, 'error')
        raise err


