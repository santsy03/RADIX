"""
module to assist in db 
transactions
"""
from mg_aapcn_me2u.src.configs.config import UPDATE_CDR_METRIC 
from mg_aapcn_me2u.src.configs.config import UPDATE_CDR_TRACKER_METRIC 
from mg_aapcn_me2u.src.lib.con import generate_connection
from utilities.metrics.core import response_time
from datetime import datetime
import traceback
import cx_Oracle

cons = generate_connection()
connections = cons['connections']


class ME2UDb(object):
    """
    class that handles db operations 
    to the data_cdr table
    """

    def __init__(self):
        '''
        initialises the db connection
        '''
        self.pool = connections


    def generate_trans_id(self, msisdn, recipient, amount, logger):
        '''
        inserts the initial msisdn, amount, recipient
        and returns a transaction id
        @params
            1) msisdn
            2) amount
            3) recipient
        @return
            transaction_id
        '''
        con = self.pool.connection()
        cursor = con.cursor()
        try:
            trans_id = int(cursor.callfunc('gen_me2u_trans_id',
                cx_Oracle.NUMBER, [msisdn, recipient, amount]))
            cursor.connection.commit()
            cursor.close()
        except Exception, err:
            logger.error(str(traceback.format_exc()))
        else:
            info = "msisdn: %s, recipient: %s, amount: %s, trans_id: %s" % (msisdn, 
                    recipient, 
                    amount,
                    trans_id)
            logger.info(info)
            return trans_id

    def update_cdr(self, params, trans_id, logger):
        '''
        updates a me2u cdr
        @params
            1) trans_id
            2) bal_before 
            3) bal_after
            4) rec_bal_before(recipients bal before)
            5) rec_bal_after(recipients bal after)
            6) status

        @return boolean (True or False)
        '''
        con = self.pool.connection()
        cursor = con.cursor()
        strt_time = datetime.now()
        sql = '''
        UPDATE ME2U_CDR SET BAL_BEFORE = :bal_before, BAL_AFTER = :bal_after, 
        REC_BAL_BEFORE = :rec_bal_before, REC_BAL_AFTER = :rec_bal_after, 
        STATUS_CODE = :status, UPDATED_AT = systimestamp WHERE id = :trans_id
        '''
        try:
            cursor.execute(sql, params)
        except Exception, err:
            logger.error(str(err))
        else:
            cursor.connection.commit()
            cursor.close()
            con. close()
            response_time(UPDATE_CDR_METRIC, strt_time, logger)
            info = "updated cdr:trans_id: %s, status: %s" % (params['trans_id'],
                    params['status'])
            stop = datetime.now()
            duration = str((stop - strt_time).total_seconds())
            logger.debug('time: update cdr: %s' % duration)
            logger.info(info)

    def update_count(self, msisdn, logger):
        '''
        updates the count me2u transactions
        Done only AFTER successfull me2u transactions
        @params:
            1) msisdn
        @return boolean (True or False)
        '''
        con = self.pool.connection()
        cursor = con.cursor()
        try:
            results = self.get_status(msisdn, logger)
        except Exception, err:
            logger.error(traceback.format_exc())
        else:
            if results:
                current_count = int(results['count'])
                current_count += 1
                strt_time = datetime.now()

                sql = '''
                UPDATE ME2U_TRACKER SET COUNT = %s, completed_at = systimestamp
                WHERE MSISDN = :msisdn ''' % current_count 
                params = {'MSISDN':msisdn}
                try:
                    cursor.execute(sql, params)
                except Exception, err:
                    logger.error(traceback.format_exc())
                else:
                    cursor.connection.commit()
                    cursor.close()
                    con. close()
                    response_time(UPDATE_CDR_TRACKER_METRIC, strt_time, logger)
                    stop = datetime.now()
                    duration = str((stop - strt_time).total_seconds()) 
                    logger.debug('time: update count: %s' % duration)

                    info = "updated ME2U TRACKER: msisdn: %s, NEW_COUNT %s" % (msisdn,
                            str(current_count))
                    logger.info(info)
            else:
                self.create_initial_record(msisdn, logger)

    def create_initial_record(self, msisdn, logger):
        '''
        creates the very first configuration for
        the tracker table
        '''
        sql = ("INSERT INTO ME2U_TRACKER (MSISDN,COUNT,REQUESTED_AT,COMPLETED_AT,STATUS_CODE)"+
                "VALUES(:msisdn,1,systimestamp, systimestamp,5)")
        params = {'MSISDN':msisdn}

        try:
            connection = self.pool.connection()
            cursor = connection.cursor()
            cursor.execute(sql, params)
        except Exception, err:
            error = "error; op: create_initial_tracker: msisdn: %s" %(msisdn)
            logger.error(error)
            logger.error(traceback.format_exc())
        else:
            cursor.connection.commit()
            cursor.close()
            info = "initial me2u record created: msisdn %s" % (msisdn)
            logger.info(info)




    def get_status(self, msisdn, logger):
        '''
        get the current record from the tracker
        '''
        con = self.pool.connection()
        cursor = con.cursor()
        
        sql = ("SELECT ID, MSISDN, COUNT," +
                "COMPLETED_AT FROM ME2U_TRACKER WHERE MSISDN = :MSISDN")
        params = {'MSISDN':msisdn}
        
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
                conf['msisdn'] = results[1]
                conf['count'] = results[2]
                conf['completed_at'] = results[3]
                return conf
            
    def is_todays_record(self, msisdn, logger):
        '''
        checks whether the record passed has been updated 
        to today
        @params
           resuts: with msisdn and last transaction detail
        @returns
            boolean
        '''
        results = self.get_status(msisdn, logger)
        today = False
        if results:
            last_trans = results['completed_at']
            now = datetime.now()
            
            if (last_trans.day == now.day) and (last_trans.month == now.month) and (last_trans.year == now.year):
                info = "last ME2U transaction took place today %s: %s 's record is still valid" %(str(last_trans), 
                        msisdn)
                logger.debug(info)
                today = True
            else:
                info = "last ME2U transaction took place %s: %s 's record needs updating" %(str(last_trans), 
                        msisdn)
                logger.debug(info)
        else:
            info = "FIRST ME2U TRANSACTION: %s 's record needs creating" %(msisdn)
            logger.debug(info)

            
        return today
    
    def rebase_to_today(self, msisdn, logger):
        '''
        resets the value in the counter to begin counting
        afresh
        @params
            msisdn
        @returns 
            True or False
        '''
        
        sql = ("UPDATE ME2U_TRACKER SET REQUESTED_AT = SYSTIMESTAMP, COMPLETED_AT = SYSTIMESTAMP," 
                + "COUNT = 0 WHERE MSISDN = :msisdn")
        params = {'MSISDN':msisdn}
        
        try:
            connection = self.pool.connection()
            cursor = connection.cursor()
            cursor.execute(sql, params)
        except Exception, err:
            error = "error; op: rebase_to_today: me2u: msisdn: %s" %(msisdn)
            logger.error(error)
            logger.error(traceback.format_exc())
        else:
            cursor.connection.commit()
            cursor.close()
            info = "rebased %s 's record to today" % (msisdn)
            logger.debug(info)

            return True
    def is_allowed(self, msisdn, logger):
        '''
        checks whether a number is allowed to access
        me2u
        @params:
            1)msisdn: the number to check
            2)logger: the logger
        @return:
            boolean
        '''
        sql = "SELECT msisdn, active FROM ME2U_WHITELIST WHERE MSISDN = :msisdn"
        params = {'msisdn':msisdn}
        try:
            connection = self.pool.connection()
            cursor = connection.cursor()
            cursor.execute(sql, params)
        except Exception, err:
            error = "error; op: is allowed: me2u: msisdn: %s" %(msisdn)
            logger.error(error)
            logger.error(traceback.format_exc())
        else:
            res = cursor.fetchall()
            print res
            if not res:
                info = "msisdn: %s is not whitelisted" % (msisdn)
                logger.debug(info)
                return False
            else:
                res = res[0][1]
                if int(res) == 1:
                    return True
                else:
                    return False




if __name__ == '__main__':
    from mg_aapcn_me2u.src.lib.custom_loggers import daemon_logger
    import pprint
    fancy_printer = pprint.PrettyPrinter(indent =4)
    #msisdn = "261330465390"
    msisdn = "261331080927"
    db = ME2UDb()
    logger = daemon_logger('/appussd/mg_aapcn_me2u/src/consumer', 'test.log')
    print db.is_allowed(msisdn, logger)


