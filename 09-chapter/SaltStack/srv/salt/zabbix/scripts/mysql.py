#!/usr/bin/env python
# -*- coding: utf-8 -*-
#File:mysql_status.py
import MySQLdb,sys
#your
user = 'zabbix'
passwd = 'zabbix'
status = sys.argv[1]
try:
    conn = MySQLdb.connect(host = 'localhost',user = user,passwd = passwd,connect_timeout = 2)
    cursor = conn.cursor()
    sql = "SHOW STATUS"
    cursor.execute(sql)
    alldata = cursor.fetchall()
    for data in alldata:
        if data[0] == status :
            #print data[0],data[1]
            print data[1]
            break
    cursor.close()
    conn.close()
except Exception, e:
    print e
    sys.exit()

'''
Open_tables
Opened_tables
Max_used_connections
Threads_connected
Qcache_free_blocks
Qcache_total_blocks
Handler_read_first
Handler_read_key
Handler_read_rnd_next
Slow_queries
'''
