from datetime import datetime
from utilities.logging.core import log
from utilities.db.core import get_connection
from utilities.secure.core import decrypt
from utilities.metrics.core import send_metric
from events.config import status
from events.config import CONSUMER
from DBUtils.PooledDB import PooledDB
import cx_Oracle
from configs.config import databases

def setup(resources={}):
    resources['connections'] =PooledDB(
                cx_Oracle,
                maxcached = 5,
                maxconnections = 50,
                user = decrypt(databases['core']['username']),
                password = decrypt(databases['core']['password']),
                dsn = databases['core']['string']
                )
 
    return resources


def dequeue_active_events(resources):
    '''
    removes all the events for the given msisdn, service, event from the events queue
    '''
    sql = ('update service_events set can_execute = 0 where status = 0 and'+
            ' msisdn =:msisdn and service_id = :service_id and event_id = :event_id'+
            ' and can_execute = 1')
    params = {}
    parameters = resources['parameters']
    params['service_id'] = parameters['service_id']
    params['msisdn'] = parameters['msisdn']
    params['event_id'] = parameters['event_id']
    try:
        connection = get_connection(resources)
        cursor = connection.cursor()
        cursor.execute(sql,params)
        cursor.connection.commit()
        status = cursor.rowcount
    except Exception, err:
        error = 'operation: get_renewals, desc: failed to retrieve renewal entries, error: %s' %str(err)
        log(resources,error,'error')
        raise err
    finally:
        try:
            cursor.close()
        except Exception, err:
            pass
        return status

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

def get_events(resources, use_connection=None):
    '''
    retrieves entries from the events queue
    '''
    sql = ("SELECT ID,MSISDN,SERVICE_ID,EVENT_ID,PARAMETERS,EXECUTE_AT "
           "FROM SERVICE_EVENTS "
           "WHERE CAN_EXECUTE=1 AND STATUS=%s AND EXECUTE_AT<:now "
           "FOR UPDATE SKIP LOCKED") % str(status['scheduled'])
    try:
        connection = use_connection or get_connection(resources)
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

def check_renew_status(resources, service_id=None, event_id=None):
    '''Function gets the events queued for a subscriber.
    The event should still be pending.
    
    event_id parameter is optional.
        if supplied, this function will return pending events 
        for the specific event_id

    service_id parameter is optional.
        if supplied, this function will return pending events 
        for the specific service_id
    '''
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    sql = 'select * from service_events where msisdn = :msisdn \
and can_execute = 1 and status = 0'
    params = {'msisdn':msisdn}
    if event_id:
        sql = '%s and event_id = :event_id' % sql
        params['event_id'] = event_id
    if service_id:
        sql = '%s and service_id = :service_id' % sql
        params['service_id'] = service_id
    try:
        connection = get_connection(resources)
        cursor = connection.cursor()
        cursor.execute(sql, params)
        records = cursor.fetchall()
        #log(resources, records, 'debug')
        count = cursor.rowcount
        if int(count) == 0:
            results = False
        else:
            results = records
        parameters['pending_records'] = results
        return pack_events(resources)
    except Exception, err:
        error = ' operation check_renew_status failed for %s, error:%s' % (
                msisdn, str(err))
        log(resources, error, 'error')
        raise err
        

def pack_events(resources):
    '''
    Function that gets a dump of pending events from service_events 
    and organizes them according to service ids.
    '''
    parameters = resources['parameters']
    pending = parameters['pending_records']
    if pending == False:
        resources['parameters']['renewal_details'] = False
        return resources
    params = {}
    try:
        for record in pending:
            data = record[0]
            service = record[2]
            data = record[0]
            params[data] = {}
            params[data]['service_id'] = service
            params[data]['event_id'] = record[5]
            params[data]['executed_at'] = record[3]
            params[data]['package_name'] = record[6].split(',')[2]

    except Exception, err:
        error = 'operation pack_events failed. error:%s' % (str(err))
        log(resources, error, 'error')
        parameters['renewal_details'] = False
        raise err
    else:
        parameters['renewal_details'] = params
        return resources

def toggle_service(resources, state = 'off'):
    '''
    Function that deactivates certain services from running their
    scheduled events.(stops events for certain services)
    Takes in resources and state( this can be on or off).
    'on' puts the services -on and 'off' puts the service -off.
    '''
    from string import lower
    parameters = resources['parameters']
    service = parameters['service_id']
    state = lower(state)
    if state == 'off':
        sql = 'update service_events set can_execute = 0 where \
service_id = :service and status = 0'
    elif state == 'on':
        sql = 'update service_events set can_execute = 1 where \
service_id = :service and status = 0 and can_execute = 0'
    params = {'service': service}
    try:
        connection = get_connection(resources)
        cursor = connection.cursor()
        cursor.execute(sql, params)
        cursor.connection.commit()
        count = cursor.rowcount
        if int(count) == 0:
            result = False
        else:
            result = True
        return result
    except Exception, err:
        error = 'operation toggle_service failed for %s, error:%s' % (
                service, str(err)
                )
        log(resources, error, 'error')
        return False


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

    log(resources, 'op:events.core.core.load_service_module - %s'%str(service_name), 'debug')

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

def update_status(resources, status, transaction_id, use_connection=None):
    '''
     - tags a given renewal entry as queued in the database to 
     preven a renewal entry from being picked more than once

    '''
    sql = ('update service_events set status = :status where id = :id')
    try:
        connection = use_connection or get_connection(resources)
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
    execute_at = str(event[5])
    msg = '%s|%s|%s|%s|%s|%s' % (
            msisdn, service_id, event_id, transaction_id, args, execute_at)
    try:
        client(queue_name, msg)

        log(resources, 'op:events.core.core.enqueue_events %s'%msg , 'debug')

    except Exception, err:
        error = ('operation: enqueue_events, desc: failed to enqueue event,'+
                ' error:%s' %str(err))
        log(resources, error, 'error')
        raise err

def process_events(resources):
    '''
    picks and enqueues renewal requests
    '''
    locking_connection = get_connection(resources)
    log(resources, 'Set up locking connection for events processing')
    try:
        events = get_events(resources, use_connection=locking_connection)
        if events:
            for event in events:
                try:
                    enqueue_events(resources, event)
                    update_status(resources, status['queued'], event[0],
                                  use_connection=locking_connection)
                    send_metric({'name_space':'application.events.generated.success'},
                            'counter')
                except Exception, err:
                    log(resources, err, 'error')
                    send_metric({'name_space':'application.events.generated.error'}, 'counter')
                    raise err
                else:
                    pass
            info = 'processed %d events' % len(events)
            log(resources, info, 'info')
        else:
            log(resources, 'no events found')
    except Exception, err:
        error = ('operation: process_events, desc: failed to process'+
                ' event requests, error: %s' %str(err))
        log(resources, error, 'error')
    finally:
        try:
            locking_connection.close()
            log(resources, 'Released locking connection')
        except Exception, err:
            error = ('operation: process_events, '
                     'desc: failed to release locking connection'+
                     'error: %s' %str(err))
            log(resources, error, 'error')
            raise err

def handle_event(resources): 
    '''
    dequeues and processes event requests
    '''
    parameters = resources['parameters']
    msg = parameters['msg']
    try:

        log(resources, 'op:events.core.core.handle_event', 'debug')

        msisdn, service_id, event_id, request_id, args, execute_at = msg.split('|')
        parameters['msisdn'] = msisdn
        parameters['service_id'] = service_id
        parameters['event_id'] = event_id
        parameters['request_id'] = request_id
        parameters['args'] = args
        parameters['execute_at'] = execute_at
        resources['parameters'] = parameters
        service_details = get_service(resources)
        if service_details:
            resources['parameters']['service_details'] = service_details
            event_handler = load_service_module(resources)
            event_handler(resources)
            del(event_handler)
            update_status(resources, int(status['processed']), int(request_id))
            send_metric({'name_space':'application.events.processed.success'}, 'counter')
        else:
            update_status(resources, int(status['error']), int(request_id))
            send_metric({'name_space':'application.events.processed.error'})
    except Exception, err:
        try:
            error = ('operation: handle_renewal_request, desc: failed to process'+
            'renewal request, error: %s' %str(err))
            log(resources, error,'error')
            update_status(resources, status['error'], request_id)
            send_metric({'name_space':'application.events.processed.error'}, 'counter')
        except Exception, err1:
            log(resources, err1, 'error')
            pass
        raise err
