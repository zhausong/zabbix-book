#Percona-Server数据库的二进制安装方法

#下载文件
```
#wget http://www.percona.com/redir/downloads/Percona-Server-5.6/LATEST/binary/linux/x86_64/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64.tar.gz   
# tar  xf  Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64.tar.gz   
# mv  Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64  /usr/local/    
#cd  /usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/   
# cp  support-files/mysql.server  /etc/init.d/mysqld   
```
#建立用户   
```
#groupadd -g 27 mysql    
#useradd -g 27 -s /sbin/nologin mysql   
```
#改变权限   
```
#chown -R  mysql.mysql /usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/   
```
提示：如果路径不为/usr/local，则需要修改启动脚本/etc/init.d/mysqld   
#启动percona-server服务   
注意不能存在文件/etc/my.cnf，否则，由于my.cnf里的不正确配置而导致mysql不能正常启动，因为mysqld脚本里面默认路径会去找/etc/my.cnf这个文件。
```
#mysqld --verbose --help|grep my.cnf    
my.cnf将会存在于以下路径，依次为优先级匹配。   
/etc/my.cnf   
/etc/mysql/my.cnf   
/usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/etc/my.cnf   
~/.my.cnf   
```
但在测试的时候，发现并未读取   
```
/usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/etc/my.cnf    
``` 
#配置my.cnf文件
```
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
```
以上my.cnf为简单的参数配置，后期还需要对此进行调整
```
#mkdir  -p  /usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/var/run   
#mkdir  -p  /usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/var/log   
```
#初始化mysql 
```
#mkdir  /opt/bak   
#mv  /etc/my.cnf  /opt/bak   
#./scripts/mysql_install_db  \   
--user=mysql    \   
--basedir=/usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/   \   
--datadir=/usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/data/   
#./bin/mysqld_safe  &   
#chkconfig  mysqld  on   
#/etc/init.d/mysqld   start   
```  
#配置环境变量 
```
#vim  ~/.bash_profile    
PATH=PATH:HOME/bin:/usr/local/Percona-Server-5.6.15-rel63.0-519-static-openssl-1.0.1e.Linux.x86_64/bin  
```
   
