import datetime
import random
import traceback
import cx_Oracle
from urllib import urlencode
from urllib2 import urlopen, Request
from datetime import datetime
from DBUtils.PooledDB import PooledDB
from config import AUTH_KEY, PROVISION_URL, ACCOUNT_ID, ROUTING_KEY, ONE, THREE
from config import message as feedback
from configs.config import databases
from utilities.secure.core import decrypt
from utilities.sms.core import send_message


def enqueue_provision_request(package, msisdn, can_renew):
    '''
    enqueues a provisioning request
    '''
    transaction_type = 'A'
    b_msisdn = msisdn
    try:
        parameters = {}
        args = {}
        parameters['msisdn'] = msisdn
        parameters['b_msisdn'] = b_msisdn
        parameters['packageId'] = package
        parameters['authKey'] = AUTH_KEY
        parameters['accountId'] = ACCOUNT_ID
        parameters['transaction_type'] = transaction_type
        parameters['requestId'] = generate_req_id()
        args['routing_key'] = ROUTING_KEY
        args['can_renew'] = can_renew
        parameters['args'] = str(args)
            
        params = urlencode(parameters)
        url = PROVISION_URL
        resp = urlopen(Request(url, params))

    except IOError, err:
        error = 'operation: IO enqueue request, desc: \
        failed to submit provisioning request %s: %s, error:%s'\
         % (msisdn, package, str(err))
        print error
        print traceback.format_exc()
        raise err
                   
    except Exception, err:
        error = 'operation: n - enqueue request, desc: \
        failed to submit provisioning request %s: %s, error: %s'\
         % (msisdn, package, str(err))
        print error
        raise err
    else:
        return (resp.info()).get('Transaction-Id')



def generate_req_id():
    '''
    returns a request id
    '''
    return str(random.randrange(1, 40000000))


def execute_provision_response(message, logger):
    import datetime
    logger.debug(type(message))
    msisdn = message.get('msisdn').strip()
    status = int(str(message.get('status')).strip())
    package_id = str(message.get('package_id'))
    try:
        count = get_subscription_count(msisdn)
        info = "SUB Prov Count:%s|%s"%(str(count), msisdn)
        logger.info(info)
        language = get_sub_language(msisdn)
        if int(package_id) != 0:
            if status == 5:
                now = (datetime.datetime.now()).hour
                val = datetime.datetime.now()
                y,m,d = val.year, val.month, val.day
                if count == 1 and now < ONE:
                    msg = feedback[str(language)]['first_before_one']
                elif count == 1 and val.time() > (datetime.datetime(y,m,d,ONE,0,0)).time():
                    msg = feedback[str(language)]['first_after_one']
                elif count == 2 and now < THREE:
                    msg = feedback[str(language)]['second_before_three']
                elif count == 2 and  val.time() > (datetime.datetime(y,m,d,THREE,0,0)).time():
                    msg = feedback[str(language)]['second_after_three']
                elif count == 3:
                    msg = feedback[str(language)]['third']

            elif status == 7:
                msg = feedback['insufficient_funds']

            elif status == 10:
                msg = feedback[str(language)]['past_time']

            elif status == 11:
                msg = feedback[str(language)]['exceed_three_subscription']

            else:
                msg = feedback['error']
        else:
            pass

    except Exception, err:
        logger.error(traceback.format_exc())

    else:
        info = '%s|%s'%(str(msisdn), str(msg))
        logger.info(info)
        send_message(msisdn, msg, logger)

def get_subscription_count(msisdn):
    from datetime import datetime
    conn = db_setup()
    cursor = conn.cursor()
    today = (datetime.now()).strftime('%d-%b-%y')
    try:
        sql = ("select sub_count from telescopic_subscription\
                where msisdn = :nu and trunc(created_at) = :td")
        params = {}
        params['nu'] = msisdn
        params['td'] = today
        result = cursor.execute(sql, params).fetchall()[0][0]

    except IndexError:
        cursor.close()
        conn.close()
        return 0

    except Exception, err:
        cursor.close()
        conn.close()
        raise err

    else:
        cursor.close()
        conn.close()
        return result


def add_modify_sub_count(resources):
    """
    Inserts or updates a record.
    """
    conn = db_setup()
    cursor = conn.cursor()
    msisdn = resources['parameters']['msisdn']
    try:
        resp = get_subscription_count(msisdn)
        if resp == 0:
            sql = ("insert into telescopic_subscription (id,msisdn,\
                    created_at,modified_at,sub_count) values\
                    (tele_seq.nextval, :nu, sysdate, '', :ct)")
            params = {}
            params['nu'] = msisdn
            params['ct'] =int(resp)  + 1
            cursor.execute(sql, params)
            cursor.connection.commit()

        else:
            sql0 = ("update telescopic_subscription set sub_count = :ct\
                    ,modified_at = sysdate where msisdn = :nu and\
                    trunc(created_at) = :td")
            params = {}
            params['nu'] = msisdn
            params['ct'] = int(resp)  + 1
            params['td'] = today = (datetime.now()).strftime('%d-%b-%y')
            cursor.execute(sql0, params)
            cursor.connection.commit()
    except Exception, e:
        raise e

    else:
        cursor.close()
        conn.close()
        

def get_sub_language(msisdn):
    conn = db_setup()
    cursor = conn.cursor()
    try:
        sql = "select language from service_language where\
                msisdn = :msisdn and id = (select max(id)\
                from service_language where msisdn =:msisdn)"
        param = {}
        param['msisdn'] = msisdn
        cursor.execute(sql, param)
        result = cursor.fetchone()
        count = cursor.rowcount

    except IndexError:
        cursor.close()
        conn.close()
        return 'txt-3'

    except Exception, e:
        print traceback.format_exc()
        cursor.close()
        conn.close()

    else:
        if count == 0:
            cursor.close()
            conn.close()
            return 'txt-3'
        else:
            cursor.close()
            conn.close()
            return result[0]


def db_setup():
    db = databases['core']
    pooled = PooledDB(cx_Oracle,maxcached = 5, maxconnections=100,\
            user = decrypt(db['username']), password = decrypt(db['password'])\
            ,dsn = db['string'], threaded = True)
    conn = pooled.connection()
    return conn


if __name__ == '__main__':
    package = '59'
    can_renew = '0'
    msisdn = '261330465390'
    #print get_sub_language(msisdn)
    print enqueue_provision_request(package, msisdn, can_renew)
