```
#wget http://www.percona.com/redir/downloads/Percona-Server-5.6/LATEST/binary/linux/x86_64/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64.tar.gz   
# tar  xf  Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64.tar.gz   
# mv  Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64  /usr/local/    
#cd  /usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/   
# cp  support-files/mysql.server  /etc/init.d/mysqld   
```
�����û�   
```
#groupadd -g 27 mysql    
#useradd -g 27 -s /sbin/nologin mysql   
```
�ı�Ȩ��   
```
#chown -R  mysql.mysql /usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/ 
```
��ʾ������·����Ϊ/usr/local������Ҫ�޸������ű�/etc/init.d/mysqld   
����percona-server����   
ע�ⲻ�ܴ����ļ�/etc/my.cnf������������my.cnf���Ĳ���ȷ���ö�����mysql����������������Ϊmysqld�ű�����Ĭ��·����ȥ��/etc/my.cnf�����ļ���   
#mysqld --verbose --help|grep my.cnf    
my.cnf��������������·��������Ϊ���ȼ�ƥ�䡣   
/etc/my.cnf   
/etc/mysql/my.cnf   
/usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/etc/my.cnf   
~/.my.cnf   
���ڲ��Ե�ʱ�򣬷��ֲ�δ��ȡ   
/usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/etc/my.cnf    
   
����my.cnf�ļ�   
# cat /usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/my.cnf    
[mysqld]   
datadir=/usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/data   
socket=/usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/var/run/mysql.sock   
user=mysql   
# Disabling symbolic-links is recommended to prevent assorted security risks   
symbolic-links=0   
character-set-server=utf8   
innodb_file_per_table=1   
   
[mysqld_safe]   
log-error=/usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/var/log/mysqld.log   
pid-file=/usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/var/run/mysqld/mysqld.pid   
����my.cnfΪ�򵥵Ĳ������ã����ڻ���Ҫ�Դ˽��е���   
#mkdir  -p  /usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/var/run   
#mkdir  -p  /usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/var/log   
��ʼ��mysql   
#mkdir  /opt/bak   
#mv  /etc/my.cnf  /opt/bak   
#./scripts/mysql_install_db  \   
--user=mysql    \   
--basedir=/usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/   \   
--datadir=/usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/data/   
#./bin/mysqld_safe  &   
#chkconfig  mysqld  on   
#/etc/init.d/mysqld   start   
   
���û�������   
#vim  ~/.bash_profile    
PATH=PATH:HOME/bin:/usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/bin   
   
