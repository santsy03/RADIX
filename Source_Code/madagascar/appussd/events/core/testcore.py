from datetime import datetime, timedelta
from utilities.logging.core import log
from utilities.db.core import get_connection
from utilities.secure.core import decrypt
from utilities.metrics.core import count
from events.config import status, DATABASE as db
from events.config import CONSUMER

def setup(resources={}):
    from cx_Oracle import SessionPool
    resources['connections'] = SessionPool(decrypt(db['user']), decrypt(db['password']),
                 decrypt(db['connection_string']), 1, 5, 1, threaded=True)
    return resources


def dequeue_active_events(resources):
    '''
    removes all the events for the given msisdn, service, event from the events queue
    '''
    sql = ('update service_events set can_execute = 0 where'+
            ' msisdn =:msisdn and service_id = :service_id and event_id = :event_id and can_execute = 1')
    params = {}
    parameters = resources['parameters']
    params['service_id'] = parameters['service_id']
    params['msisdn'] = parameters['msisdn']
    params['event_id'] = parameters['event_id']
    try:
        connection = get_connection(resources)
        cursor = connection.cursor()
        cursor.execute(sql,params)
        mycount = cursor.rowcount
        cursor.connection.commit()
    except Exception, err:
        error = 'operation: get_renewals, desc: failed to retrieve renewal entries, error: %s' %str(err)
        log(resources,error,'error')
        raise err
    finally:
        try:
            cursor.close()
            return mycount
        except Exception, err:
            pass

def create_event(resources):
    '''
    creates an entry for renewal for a given service
    '''
    sql = ('insert into service_events(msisdn,service_id,parameters,'+
            ' execute_at, can_execute, event_id, status) values(:msisdn, :service_id, '+
            ':parameters, :execute_at, :can_execute, :event_id,0)')
    params = {}
    parameters = resources['parameters']
    params['service_id'] = parameters['service_id']
    params['msisdn'] = parameters['msisdn']
    params['execute_at'] = parameters['execute_at']
    params['can_execute'] = parameters['can_execute']
    params['event_id'] = parameters['event_id']
    params['parameters'] = parameters['parameters']
    try:
        dequeue_active_events(resources)
        connection = get_connection(resources)
        cursor = connection.cursor()
        cursor.execute(sql,params)
        cursor.connection.commit()
    except Exception, err:
        error = 'operation: get_events, desc: failed to retrieve event entries, error: %s' %str(err)
        log(resources,error,'error')
        raise err
    finally:
        try:
            cursor.close()
        except Exception, err:
            pass

def get_events(resources):
    '''
    retrieves entries from the events queue
    '''
    sql = ('select id,msisdn,service_id,event_id,parameters'+
            ' from service_events'+
            ' where can_execute = 1 and status = %s and execute_at < :now' %str(status['scheduled']))
    try:
        connection = get_connection(resources)
        cursor = connection.cursor()
        #params = {'now': datetime.now() + timedelta(hours=1) }
        params = {'now': datetime.now() }
        cursor.execute(sql, params)
        results = cursor.fetchall()
        count = cursor.rowcount
        if int(count) == 0:
            results = False
    except Exception, err:
        error = 'operation: get_renewals, desc: failed to retrieve renewal entries, error: %s' %str(err)
        log(resources,error,'error')
        raise err
    finally:
        try:
            cursor.close()
        except Exception, err:
            pass
    return results

def get_service(resources):
    '''
    retrieves the details for active services
    '''

    sql = ('select id, name from services where status = 1 and id = :service_id')
    try:
        parameters = resources['parameters']
        service_id = parameters['service_id']
        params = {'service_id': str(service_id).strip()}
        connection = get_connection(resources)
        cursor = connection.cursor()
        cursor.execute(sql, params)
        results = cursor.fetchone()
        count = cursor.rowcount
        if count == 0:
            results = False
    except Exception, err:
        error = 'operation: get_services, desc: failed to retrieve service details, error: %s' %str(err)
        log(resources,error,'error')
        raise err
    finally:
        try:
            cursor.close()
        except Exception, err:
            pass
    return results

def load_service_module(resources):
    '''
    loads the given function for the given service for currently
    active services
    '''
    service_details = resources['parameters']['service_details']
    service_name = service_details[1]
    try:
        stmt = "import %s.handlers.core" %(service_name,)
        #log(resources,stmt,'debug')
        exec(stmt)
        stmt = "service_handler = %s.handlers.core.event_handler" %(service_name,)
        #log(resources,stmt,'debug')
        exec(stmt)
        return service_handler
    except Exception, err:
        error = 'operation: load_service_module: desc: %s, error:%s' %(stmt, str(err))
        log(resources, error,'error')

def update_status(resources, status, transaction_id):
    '''
     - tags a given renewal entry as queued in the database to 
     preven a renewal entry from being picked more than once

    '''
    sql = ('update service_events set status = :status where id = :id')
    try:
        connection = get_connection(resources)
        cursor = connection.cursor()
        params = {'id': transaction_id, 'status': status}
        cursor.execute(sql, params)
        cursor.connection.commit()
    except Exception, err:
        error = ('operation: get_renewals, desc: failed to update renewal'+
                ' entries, error: %s' %str(err))
        log(resources,error,'error')
        raise err
    finally:
        try:
            cursor.close()
        except Exception, err:
            pass

def enqueue_events(resources, event):
    '''
    passes the details of the event to the events queue
    '''
    from events.common.queue import Queue_Client as client
    queue_name = CONSUMER['queue_name']
    transaction_id = str(event[0])
    msisdn = str(event[1]).strip()
    service_id = str(event[2]).strip()
    event_id = str(event[3]).strip()
    args = str(event[4]).strip()
    msg = '%s|%s|%s|%s|%s' %(msisdn, service_id, event_id, transaction_id, args)
    try:
        client(queue_name, msg)
    except Exception, err:
        error = ('operation: enqueue_events, desc: failed to enqueue event,'+
                ' error:%s' %str(err))
        log(resources, error, 'error')
        raise err

def process_events(resources):
    '''
    picks and enqueues renewal requests
    '''
    events = get_events(resources)
    if events:
        for event in events:
            try:
                enqueue_events(resources, event)
                update_status(resources, status['queued'], event[0])
                count('application.events.generated.success')
            except Exception, err:
                error = ('operation: process_events, desc: failed to process'+
                        ' event requests, error: %s' %str(err))
                log(resources, error, 'error')
                count('application.events.generated.error')
                raise err
            else:
                pass
        info = 'processed %d events' %len(events)
        log(resources, info, 'info')

def handle_event(resources): 
    '''
    dequeues and processes event requests
    '''
    parameters = resources['parameters']
    msg = parameters['msg']
    try:
        msisdn, service_id, event_id, request_id, args = msg.split('|')
        parameters['msisdn'] = msisdn
        parameters['service_id'] = service_id
        parameters['event_id'] = event_id
        parameters['request_id'] = request_id
        parameters['args'] = args
        resources['parameters'] = parameters
        service_details = get_service(resources)
        if service_details:
            resources['parameters']['service_details'] = service_details
            event_handler = load_service_module(resources)
            event_handler(resources)
            del(event_handler)
            update_status(resources, int(status['processed']), int(request_id))
            count('application.events.processed.success')
        else:
            update_status(resources, int(status['error']), int(request_id))
            count('application.events.processed.error')
    except Exception, err:
        try:
            error = ('operation: handle_renewal_request, desc: failed to process'+
            'renewal request, error: %s' %str(err))
            log(resources, error,'error')
            update_status(resources, status['error'], request_id)
            count('application.events.processed.error')
        except Exception, err1:
            pass
        raise err
