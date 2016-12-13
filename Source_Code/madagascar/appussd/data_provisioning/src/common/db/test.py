#!/usr/bin/env python
def test_getConnection():
    #from data_provisioning.src.common.db.core import getConnection
    from core import getConnection
    resources = setup()
    #print getConnection(resources)
    
def setup():
    import cx_Oracle
    resources = {}
    resources['connections'] = cx_Oracle.SessionPool('pavp','pavp654','172.23.0.159:1524/fnr',4,10,1,threaded=True)
    connection = resources['connections'].acquire()
    return resources

if __name__ == '__main__':
    test_getConnection()
