1.��װoracle�Ŀͻ���������
rpm  -ivh  oracle-instantclient11.2-basic-11.2.0.3.0-1.x86_64.rpm
rpm  -ivh  oracle-instantclient11.2-devel-11.2.0.3.0-1.x86_64.rpm
rpm  -ivh  oracle-instantclient11.2-sqlplus-11.2.0.3.0-1.x86_64.rpm
rpm  -ivh  cx_Oracle-5.1.2-11g-py26-1.x86_64.rpm
rpm  -ivh  python-argparse-1.2.1-2.el6.noarch.rpm

2.���ļ�·��
#vim /etc/ld.so.conf.d/oracle.conf #������������
/usr/lib/oracle/11.2/client64/lib
#ldconfig -v

3.�ű������ļ�
#cp  pyora.py /etc/zabbix/scripts/pyora.py
#cp  py_oracle.conf /etc/zabbix/zabbix_agentd.conf.d/oracle.conf

4.web����xml�ļ�ORACLE_zbx_templates.xml
host�������ú�����
Macro	 	Value	 
{$ADDRESS}    192.168.153.153
{$ARCHIVE}    VGDATA
{$DATABASE}   clouddb
{$PASSWORD}   123456
{$USERNAME}   testuser

出自http://bicofino.io/blog/2013/12/09/monitoring-oracle-with-zabbix/



