"""
module to assist in db 
transactions
"""
from configs.config import databases
from mg_data_interface.src.configs.config import INSERT_METRIC 
from mg_data_interface.src.configs.config import INSERT_CDR_METRIC 
from mg_data_interface.src.configs.config import UPDATE_CDR_METRIC 
from mg_data_interface.src.lib.con import generate_connection
from utilities.secure.core import decrypt
from utilities.metrics.core import response_time
import cx_Oracle
from datetime import datetime
from DBUtils.PooledDB import PooledDB
import json
import traceback

'''
cons = generate_connection()
connections = cons['connections']
'''

class DataCDR(object):
    """
    class that handles db operations 
    to the data_cdr table
    """

    def __init__(self):
        '''initialises the db connection
        '''
        self.pool = PooledDB(
                cx_Oracle, 
                maxcached = 5,
                maxconnections = 50,
                user = decrypt(databases['core']['username']),
                password = decrypt(databases['core']['password']),
                dsn = databases['core']['string']
                )
  
        self.start_time = datetime.now()

    def insert_record(self, parameters, logger):
        '''
        inserts a new subscription record
        parameters should have 
        1) msisdn
        2) transaction_id
        3) recipient
        4) package
        5) cost
        6) status
        7) type
        8) created_at
        '''

        if parameters['transaction_type'] == 'B':
            params = {}
            params['msisdn'] = parameters['msisdn']
            params['transaction_id'] = parameters['transactionId']
            params['recipient'] = parameters['b_msisdn']
            params['package'] = parameters['packageId']
            params['cost'] = parameters['msisdn']
            params['status'] = parameters['status']
            params['type'] = parameters['transaction_type']

            sql = '''insert into data_cdr(id,msisdn,transaction_id,recipient,package,cost,status,type,created_at)\
                    values (DATA_CDR_SEQ.NEXTVAL,:msisdn,:transaction_id,:recipient,:package,:cost,:status,:type,systimestamp)'''
                    
        else:
            params = {}
            params['msisdn'] = parameters['msisdn']
            params['transaction_id'] = parameters['transactionId']
            params['package'] = parameters['packageId']
            params['cost'] = parameters['msisdn']
            params['status'] = parameters['status']
            params['type'] = parameters['transaction_type']

            sql = '''insert into data_cdr(id,msisdn,transaction_id,package,cost,status,type,created_at)\
                    values (DATA_CDR_SEQ.NEXTVAL,:msisdn,:transaction_id,:package,:cost,:status,:type,systimestamp)'''
        con = self.pool.connection()
        cursor = con.cursor()

        try:
            cursor.execute(sql, params)
        except Exception, err:
            cursor.close()
            con.close()
            logger.error("operation: insert_record || error %s"\
                   % (str(err)))
            #return False
            raise err
        else:
            cursor.connection.commit()
            cursor.close()
            con. close()
            response_time(INSERT_METRIC, self.start_time)
            return True

    def insert_web_response(self, msisdn, request_id, response, logger):
        con = self.pool.connection()
        cursor = con.cursor()
        response = json.dumps(response)
        sql = ''' 
        insert into bundle_responses (id, msisdn, request_id, response, created_at,
        action) values (bndl_resp_seq.NEXTVAL,:msisdn,:request_id,:response, systimestamp, '1') 
        '''
        params = {'msisdn':msisdn,'request_id':request_id, 'response':response}
        try:
            cursor.execute(sql, params)
        except Exception, err:
            raise err
            if logger is not None:
                logger.error(str(err))
        else:
            cursor.connection.commit()
            cursor.close()
            con. close()
            if logger is not None:
                logger.info("inserted web response")


    def insert_cdr(self, message, logger, context = None):
        '''
        inserts a my meg 15 cdr based on params extracted from the table
        '''
        con = self.pool.connection()
        cursor = con.cursor()

        msisdn = str(message['msisdn']).strip()
        status = int(str(message['status']).strip())
        b_msisdn = str(message['b_msisdn']).strip()
        package_id = str(message['package_id']).strip()
        trans_id =str(message['transactionId']).strip()
        action = "purchase"

        if context:
            status = context

        strt_time = datetime.now()
        sql = '''
        INSERT INTO MEG_FIFTN_CDR(MSISDN,B_MSISDN,ACTION,CREATED_AT,MODIFIED_AT,TRANSACTION_ID,STATUS_CODE)
        VALUES(:msisdn,:b_msisdn,:action,systimestamp, systimestamp,:trans_id,:status)
        '''
        params = {'msisdn':msisdn,'status':status,'b_msisdn':b_msisdn,'action':action,'trans_id':trans_id}
        try:
            cursor.execute(sql, params)
        except Exception, err:
            if logger is not None:
                logger.error(str(err))
            else:
                raise err
        else:
            cursor.connection.commit()
            cursor.close()
            con. close()
            response_time(INSERT_CDR_METRIC, strt_time, logger)
            info = "inserted cdr: msisdn: %s, b_msisdn: %s, data prov trans_id: %s" % (msisdn,
                    b_msisdn, str(trans_id))
            stop = datetime.now()
            duration = str((stop - strt_time).total_seconds())
            logger.debug('time: insert cdr: %s' % duration)

            if logger is not None:
                logger.info(info)
            else:
                print info

    def update_count(self, message, logger, current_block):
        '''
        updates a my meg fifteen count based on the current time
        '''
        con = self.pool.connection()
        cursor = con.cursor()
        msisdn = str(message['msisdn']).strip()
        status = int(str(message['status']).strip())
        b_msisdn = str(message['b_msisdn']).strip()
        results = None
        try:
            results = self.get_status(message, logger)
        except Exception, err:
            logger.error(traceback.format_exc())
        else:
            if results:
                current_count = int(results[current_block])
                current_count += 1

                to_update =  "%s_COUNT" % (current_block.upper())
                debug = "updating the %s: because its %s" % (to_update, current_block)
                logger.debug(debug)

                strt_time = datetime.now()

                sql = '''
                UPDATE MEG_FIFTN_TRACKER SET %s = :current_count, completed_at = systimestamp
                WHERE MSISDN = :b_msisdn ''' % (to_update)
                #logger.debug(sql)
                params={'b_msisdn':b_msisdn,'current_count':current_count}
                try:
                    cursor.execute(sql, params)
                except Exception, err:
                    logger.error(traceback.format_exc())
                else:
                    cursor.connection.commit()
                    cursor.close()
                    con. close()
                    response_time(UPDATE_CDR_METRIC, strt_time, logger)
                    stop = datetime.now()
                    duration = str((stop - strt_time).total_seconds()) 
                    logger.debug('time: update count: %s' % duration)

                    info = "updated TRACKER: msisdn: %s, NEW_COUNT %s, BLOCK: %s" % (b_msisdn,
                            str(current_count), current_block)
                    logger.info(info)


    def get_status(self, message, logger):
        '''
        get the current record from the tracker
        '''
        con = self.pool.connection()
        cursor = con.cursor()
        msisdn = str(message['msisdn']).strip()
        b_msisdn = str(message['b_msisdn']).strip()
        
        sql = ("SELECT ID, MSISDN, MORNING_COUNT,AFTERNOON_COUNT," +
                "COMPLETED_AT FROM MEG_FIFTN_TRACKER WHERE MSISDN = :MSISDN")
        params = {'MSISDN':b_msisdn}
        
        try:
            cursor.execute(sql, params)
            results = cursor.fetchall()
        
        except Exception, err:
            error = "error; op: get_current_status: msisdn: %s" %(msisdn)
            logger.error(error)
            logger.error(traceback.format_exc())
            return None
        else:
            if not results:
                return None
            else:
                info = "current status: %s. msisdn %s" % (str(results), msisdn)
                logger.debug(info)
                conf = {}
                results = results[0]
                conf['id'] = results[0]
                conf['morning'] = results[2]
                conf['afternoon'] = results[3]
                conf['completed_at'] = results[4]
                cursor.close()
                con.close()
                return conf



        






if __name__ == '__main__':
    import pprint
    fancy_printer = pprint.PrettyPrinter(indent =4)

    message = {u'status': u'5', u'b_msisdn': u'261334933535', u'name': u'MyMeg 15', u'msisdn': u'261334933535', u'args': {u'can_renew': u'0', u'is_night': u'False', u'routing_key': u'meg_fiftn'}, u'transaction_type': u'A', u'package_id': u'1', u'transactionId': u'1917', u'balance': {u'meg_15': {u'amount': 42127360, u'expiry': False}}}
    db = DataCDR()
    db.insert_cdr(message, None)

