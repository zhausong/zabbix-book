#!/usr/bin/env python
# coding: utf-8
"""
    Author: Danilo F. Chilene
	Email:	bicofino@gmail.com
"""

version = 0.1
import argparse,cx_Oracle
import inspect
import re

def bytes2human(n):
  '''
  http://code.activestate.com/recipes/578019
  >>> bytes2human(10000)
  '9.8K'
  >>> bytes2human(100001221)
  '95.4M'
  '''
  symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
  prefix = {}
  for i, s in enumerate(symbols):
    prefix[s] = 1 << (i+1)*10
  for s in reversed(symbols):
    if n >= prefix[s]:
      value = float(n) / prefix[s]
      return '%.1f%s' % (value, s)
  return '%sB' % n

class Checks(object):

	def check_active(self):
		'''Check Intance is active and open'''
		sql = "select to_char(case when inst_cnt > 0 then 1 else 0 end,'FM99999999999999990') retvalue from (select count(*) inst_cnt from v$instance where status = 'OPEN' and logins = 'ALLOWED' and database_status = 'ACTIVE')"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def rcachehit(self):
		'''Read Cache hit ratio'''
		sql = "SELECT to_char((1 - (phy.value - lob.value - dir.value) / ses.value) * 100, 'FM99999990.9999') retvalue \
	            FROM   v$sysstat ses, v$sysstat lob, \
	                   v$sysstat dir, v$sysstat phy \
	            WHERE  ses.name = 'session logical reads' \
	            AND    dir.name = 'physical reads direct' \
	            AND    lob.name = 'physical reads direct (lob)' \
	            AND    phy.name = 'physical reads'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def dsksortratio(self):
		'''Disk sorts ratio'''
		sql = "SELECT to_char(d.value/(d.value + m.value)*100, 'FM99999990.9999') retvalue \
	             FROM  v$sysstat m, v$sysstat d \
	             WHERE m.name = 'sorts (memory)' \
	             AND d.name = 'sorts (disk)'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def activeusercount(self):
		'''Count of active users'''
		sql = "select to_char(count(*)-1, 'FM99999999999999990') retvalue from v$session where username is not null \
	             and status='ACTIVE'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def dbsize(self):
		'''Size of user data (without temp)'''
		sql = "SELECT to_char(sum(  NVL(a.bytes - NVL(f.bytes, 0), 0)), 'FM99999999999999990') retvalue \
	             FROM sys.dba_tablespaces d, \
	             (select tablespace_name, sum(bytes) bytes from dba_data_files group by tablespace_name) a, \
	             (select tablespace_name, sum(bytes) bytes from dba_free_space group by tablespace_name) f \
	             WHERE d.tablespace_name = a.tablespace_name(+) AND d.tablespace_name = f.tablespace_name(+) \
	             AND NOT (d.extent_management like 'LOCAL' AND d.contents like 'TEMPORARY')"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			#print bytes2human(int(i[0]))
			print i[0]

	def dbfilesize(self):
		'''Size of all datafiles'''
		sql = "select to_char(sum(bytes), 'FM99999999999999990') retvalue from dba_data_files"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			#print bytes2human(int(i[0]))
			print i[0]

	def version(self):
		'''Oracle version (Banner)'''
		sql = "select banner from v$version where rownum=1"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def uptime(self):
		'''Instance Uptime (seconds)'''
		sql = "select to_char((sysdate-startup_time)*86400, 'FM99999999999999990') retvalue from v$instance"
		self.cur.execute(sql)
		res = self.cur.fetchmany(numRows=3)
		for i in res:
			print i[0]

	def commits(self):
		'''User Commits'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'user commits'"
		self.cur.execute(sql)
		res = self.cur.fetchmany(numRows=3)
		for i in res:
			print i[0]

	def rollbacks(self):
		'''User Rollbacks'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'user rollbacks'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def deadlocks(self):
		'''Deadlocks'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'enqueue deadlocks'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def redowrites(self):
		'''Redo Writes'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'redo writes'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def tblscans(self):
		'''Table scans (long tables)'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'table scans (long tables)'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def tblrowsscans(self):
		'''Table scan rows gotten'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'table scan rows gotten'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def indexffs(self):
		'''Index fast full scans (full)'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'index fast full scans (full)'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def hparsratio(self):
		'''Hard parse ratio'''
		sql = "SELECT to_char(h.value/t.value*100,'FM99999990.9999') retvalue \
	             FROM  v$sysstat h, v$sysstat t \
	             WHERE h.name = 'parse count (hard)' \
	             AND t.name = 'parse count (total)'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def netsent(self):
		'''Bytes sent via SQL*Net to client'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'bytes sent via SQL*Net to client'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def netresv(self):
		'''Bytes received via SQL*Net from client'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'bytes received via SQL*Net from client'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def netroundtrips(self):
		'''SQL*Net roundtrips to/from client'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'SQL*Net roundtrips to/from client'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def logonscurrent(self):
		'''Logons current'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'logons current'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]
	  
	def lastarclog(self):
		'''Last archived log sequence'''
		sql = "select to_char(max(SEQUENCE#), 'FM99999999999999990') retvalue from v$log where archived = 'YES'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def lastapplarclog(self):
		'''Last applied archive log (at standby).Next items requires [timed_statistics = true]'''
		sql = "select to_char(max(lh.SEQUENCE#), 'FM99999999999999990') retvalue \
	             from v$loghist lh, v$archived_log al \
	             where lh.SEQUENCE# = al.SEQUENCE# and applied='YES'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def freebufwaits(self):
		'''Free buffer waits'''
		sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'free buffer waits'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def bufbusywaits(self):
		'''Buffer busy waits'''
		sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'buffer busy waits'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def logswcompletion(self):
		'''log file switch completion'''
		sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'log file switch completion'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def logfilesync(self):
		'''Log file sync'''
		sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'log file sync'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def logprllwrite(self):
		'''Log file parallel write'''
		sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'log file parallel write'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def enqueue(self):
		'''Enqueue waits'''
		sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'enqueue'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def dbseqread(self):
		'''DB file sequential read waits'''
		sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'db file sequential read'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def dbscattread(self):
		'''DB file scattered read'''
		sql="select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'db file scattered read'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def dbsnglwrite(self):
		'''DB file single write'''
		sql="select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'db file single write'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def dbprllwrite(self):
		'''DB file parallel write'''
		sql="select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'db file parallel write'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def directread(self):
		'''Direct path read'''
		sql="select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'direct path read'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def directwrite(self):
		'''Direct path write'''
		sql="select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'direct path write'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def latchfree(self):
		'''latch free.'''
		sql="select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'latch free'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]
	
	def tablespace(self, name):
		sql = '''SELECT df.tablespace_name "TABLESPACE", ROUND ( (df.bytes - SUM (fs.bytes)) * 100 / df.bytes, 2) "USED" FROM sys.sm$ts_free fs, (  SELECT tablespace_name, SUM (bytes) bytes FROM sys.sm$ts_avail GROUP BY tablespace_name) df WHERE fs.tablespace_name(+) = df.tablespace_name and df.tablespace_name = '{0}' GROUP BY df.tablespace_name, df.bytes ORDER BY 1'''.format(name)
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[1]

	def show_tablespaces(self):
		'''List tablespace names in a JSON like format for Zabbix use'''
		sql = "SELECT tablespace_name FROM dba_tablespaces ORDER BY 1";
		self.cur.execute(sql)
		res = self.cur.fetchall()
		rowarray_list = []
		print '{'
		print "\t\"data\":[\n\n"
		for i in res:
			print '\t{\n'
			teste = "\t\t\"{0}\":\"{1}\"{2},\n".format('{#TABLESPACE}', re.sub("[\(\)\{\<>,']", '', str(i,)), '}')
			print teste[0:-1]
		print ']';
		print '}';

	def check_archive(self,archive):
		'''List archive used'''
		sql = "select trunc((total_mb-free_mb)*100/(total_mb)) PCT from v$asm_diskgroup_stat where name='{0}' ORDER BY 1".format(archive)
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

#	def query_lock(self):
#		'''Check query lock'''
#		sql = "SELECT count(*) FROM gv$lock l WHERE l.TYPE <> 'MR' and block=1"
#		sql = "SELECT DECODE(request,0,'Holder: ','Waiter: ')||sid sess, id1, id2, lmode, request, type FROM GV$LOCK \
#WHERE (id1, id2, type) IN (SELECT id1, id2, type FROM GV$LOCK WHERE request>0) ORDER BY id1, request"
#		self.cur.execute(sql)
#		res = self.cur.fetchall()
#		for i in res:
#			print i[0]

	def query_lock(self):
		'''Query lock 2'''
		sql = "SELECT count(*) FROM gv$lock l WHERE  block=1"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def query_redologs(self):
		'''Redo logs'''
		sql = "select COUNT(*) from v$LOG WHERE STATUS='ACTIVE'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def query_rollbacks(self):
		'''Rollback'''
		sql = "select nvl(trunc(sum(used_ublk*4096)/1024/1024),0) from gv$transaction t,gv$session s where ses_addr = saddr"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def query_sessions(self):
		'''Sessions'''
		sql = "select count(*) from gv$session where username is not null and status='ACTIVE'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

	def query_temp(self):
		'''Query temp'''
		sql = "select nvl(sum(blocks*8192)/1024/1024,0) from gv$session s, gv$sort_usage u where s.saddr = u.session_addr"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			print i[0]

class Main(Checks):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--username')
        parser.add_argument('--password')
        parser.add_argument('--address')
        parser.add_argument('--database')

        subparsers = parser.add_subparsers()

        for name in dir(self):
            if not name.startswith("_"):
                p = subparsers.add_parser(name)
                method = getattr(self, name)
                argnames = inspect.getargspec(method).args[1:]
                for argname in argnames:
                    p.add_argument(argname)
                p.set_defaults(func=method, argnames=argnames)
        self.args = parser.parse_args()
    
    def db_connect(self):
		a = self.args
		username = a.username
		password = a.password
		address = a.address
		database = a.database
		self.db = cx_Oracle.connect('''{0}/{1}@{2}/{3}'''.format(username,password,address,database))
		self.cur = self.db.cursor()

    def db_close(self):
    	self.db.close()

    def __call__(self):
    	try:
        	a = self.args
        	callargs = [getattr(a, name) for name in a.argnames]     
        	self.db_connect()
        	try:
        		return self.args.func(*callargs)
        	finally:
        		self.db_close()
        except Exception, err:
        	print 0

if __name__ == "__main__":
    main = Main()
    main()
