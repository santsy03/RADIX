def dbHandler1(resources,action):
    from data_provisioning.src.configs.dbconfig import db
    from cx_Oracle import SessionPool
    dbusername = db['username']
    dbpassword = db['password']
    ip = db['ip']
    port = db['port']
    sid = db['sid']
    connections = SessionPool(dbusername,dbpassword,ip+':'+port+'/'+sid,10,500,5,threaded=True)
    cursor = (connections.acquire()).cursor()
    parameters = resources['parameters']
    msisdn = parameters['msisdn']
    requestId = parameters['requestId']
    #packageId = parameters['packageId']
    #response = select(resources,'request')[6]
    #createdAt = select(resources,'request')[7]


    if action == 'userProfile':
        userId = select(resources,'request_userId')
        request_status = select('request')[2]
        status = select(resources,request_status)
        sql = 'SELECT * FROM user_profiles WHERE id = :userId'
        sql.execute(sql,{'userId':userId})
        resp = cursor.fetchall()
        cursor.connection.commit()
        return resp
    elif action == 'storedProc':
        transactionId = getTransId()[0]
        #transactionId = cursor.callfunc(generate_TransactionId,int,parameters[userId,requestId,msisdn,packageId,status,response,createdAt])
        return transactionId
    
    elif action == 'request':
        sql = 'select * from requests where request_id=:requestId'
        sql.execute(sql,{'request_id':requestId})
        resp = cursor.fetchall()
        cursor.connection.commit()
        return resp
    elif action == 'package':
        sql = 'select * from packages where package_id=:packageId'
        sql.execute(sql,{'packageId':packageId})
        resp = cursor.fetchall()
        cursor.connection.commit()
        return resp


def dbHandler2(resources,action):
    from cx_Oracle import SessionPool
    from data_provisioning.src.configs.dbconfig import db
    dbusername = db['username']
    dbpassword = db['password']
    ip = db['ip']
    port = db['port']
    sid = db['sid']
    connections = SessionPool(dbusername,dbpassword,ip+':'+port+'/'+sid,10,500,5,threaded=True)
    if action == 'request':
        try:
            transactionId = parameters['transactionId']
            cursor = (connections.acquire()).cursor()
            sql = 'select * from requests where id = :transactionId'
            cursor.execute(sql,{'transactionId':transactionId})
        except Exception,e:
            error = 'Error:%s'%(str(e),)
            print error
            raise e
        else:
            resp = cursor.fetchone()
            #cursor.connection.commit()
            cursor.close()
            return resp
    elif action == 'package':
        try:
            cursor = (connections.acquire()).cursor()
            packageId = dbHandler(resources,'cdr')[2]
            sql = 'select * from packages where id = :packageId'
            cursor.execute(sql,{'packageId':packageId})
        except Exception,e:
            error = 'Error:%s'%(str(e),)
            print error
            raise e
        else:
            resp = cursor.fetchone()
            #cursor.connection.commit()
            cursor.close()
            return resp
    elif action == 'cdr':
        try:
            transactionId = parameters['transactionId']
            cursor = (connections.acquire()).cursor()
            sql = 'select * from cdrs where transaction_id = :transactionId'
            cursor.execute(sql,{'transactionId':transactionId})
        except Exception,e:
            error = 'Error:%s'%(str(e),)
            print error
            raise e
        else:
            resp = cursor.fetchall()
            #cursor.connection.commit()
            cursor.close()
            return resp

            
def dbHandler(resources,action):
    import cx_Oracle
    from cx_Oracle import SessionPool
    import data_provisioning.src.configs.dbconfig
    from handleRequest import debug
    dbusername = db['username']
    dbpassword = db['password']
    ip = db['ip']
    port = db['port']
    sid = db['sid']
    connections = SessionPool(dbusername,dbpassword,ip+':'+port+'/'+sid,10,500,5,threaded=True)
    parameters = resources['parameters']
    transactionId = parameters['transactionId']
    
    if action == 'provision_response':
        try:
            cursor = (connections.acquire()).cursor()
            sql = 'select table1.package_id, table2.package_name, table1.created_at, table1.status from requests table1,packages table2 where table1.id = :transactionId'
            cursor.execute(sql,{'transactionId':transactionId})
            resp = cursor.fetchall()
            cursor.close()
        except Exception,e:
            print 'Error:'+str(e)
            raise e
        else:
            return resp
        
    elif action == 'balance_response':
        try:
            cursor = (connections.acquire()).cursor()
            sql = 'select table1.package_id, table2.package_name, table1.created_at, table1.status from requests table1,packages table2 where table1.id = :transactionId'
            cursor.execute(sql,{'transactionId':transactionId})
            resp = cursor.fetchall()
            cursor.close()
        except Exception,e:
            print 'Error:'+str(e)
            raise e
        else:
            return resp


    elif action == 'provision_request' or action == 'balance_request':
        userId = parameters['userId']
        requestId = parameters['requestId']
        msisdn = parameters['msisdn']
        packageId = parameters['packageId']
        status = parameters['status']
        cursor = (connections.acquire()).cursor()
        '''call the stored function'''
        try:
            transactionId = cursor.callfunc('generate_TransactionId',cx_Oracle.NUMBER,[userId,requestId,msisdn,packageId,status])
            #transactionId = 25
        except Exception,e:
            error = 'operation:dbHandler action:%s,msisdn=%s,Error:%s'%(action,msisdn,str(e),)
            print error
            raise e
        else:
            print debug('successfully inserted')
            cursor.connection.commit()
            cursor.close()
            return transactionId
    else:
        return debug('Where\'s your action?')

if __name__ == '__main__':
    from datetime import datetime
    resources = {}
    parameters = {}
    parameters['transactionId'] = 4
    parameters['userId'] = 2
    parameters['requestId'] = 3
    parameters['msisdn'] = '254735449662'
    parameters['packageId'] = 4
    parameters['status'] = 0
    parameters['response'] = 'Respo'
    parameters['createdAt'] = datetime.now()
    resources['parameters'] = parameters
    print dbHandler(resources,'provision_request')
