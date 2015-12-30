#Ubuntu下搭建Zabbix   
#一、操作系统的安装  
安装Ubuntu，过程略  
#二、DEB源的配置   
参考文档
```
https://www.zabbix.com/documentation/2.2/manual/installation/install_from_packages 
```
各版本的配置信息如下   
```
 Zabbix 2.2 for Debian 6:
# wget http://repo.zabbix.com/zabbix/2.2/debian/pool/main/z/zabbix-release/zabbix-release_2.2-1+squeeze_all.deb
# dpkg -i zabbix-release_2.2-1+squeeze_all.deb
# apt-get update

Zabbix 2.2 for Debian 7:
# wget http://repo.zabbix.com/zabbix/2.2/debian/pool/main/z/zabbix-release/zabbix-release_2.2-1+wheezy_all.deb
# dpkg -i zabbix-release_2.2-1+wheezy_all.deb
# apt-get update

Zabbix 2.2 for Ubuntu 12.04 LTS:
# wget http://repo.zabbix.com/zabbix/2.2/ubuntu/pool/main/z/zabbix-release/zabbix-release_2.2-1+precise_all.deb
# dpkg -i zabbix-release_2.2-1+precise_all.deb
# apt-get update

Zabbix 2.2 for Ubuntu 14.04 LTS:
# wget http://repo.zabbix.com/zabbix/2.2/ubuntu/pool/main/z/zabbix-release/zabbix-release_2.2-1+trusty_all.deb
# dpkg -i zabbix-release_2.2-1+trusty_all.deb
# apt-get update

#cat /etc/apt/sources.list.d/zabbix.list  #源里面的记录如下
deb http://repo.zabbix.com/zabbix/2.2/ubuntu trusty main
deb-src http://repo.zabbix.com/zabbix/2.2/ubuntu trusty main
```
安装Zabbix-Server   
3.1、安装Zabbix-Server   
```
# sudo  apt-get install zabbix-server-mysql  php5-mysql zabbix-frontend-php 
```
3.2、配置zabbix_server.conf   
```
# vi /etc/zabbix/zabbix_server.conf
DBHost=localhost
DBName=zabbix
DBUser=zabbix
DBPassword=zabbix
```
3.3、设置开机启动项   
```
#vim  /etc/default/zabbix-server
START=yes
```
3.4、启动zabbix-server服务   
```
#sudo service zabbix-server start
```

3.5、启动MySQL服务   
```
#sudo  service  mysql start
```

3.6、创建Zabbix数据库   
```
# mysql -uroot
mysql> create database zabbix character set utf8 collate utf8_bin;
mysql> grant all privileges on zabbix.* to zabbix@localhost identified by 'zabbix';
mysql> flush privileges；
```
3.7、导入Zabbix数据库   
```
#cd /usr/share/zabbix-server-mysql/
#sudo gunzip *.gz
#mysql -u zabbix -p zabbix < schema.sql
#mysql -u zabbix -p zabbix < images.sql
#mysql -u zabbix -p zabbix < data.sql


#sudo cp /usr/share/doc/zabbix-frontend-php/examples/zabbix.conf.php.example /etc/zabbix/zabbix.conf.php
#sudo cp /usr/share/doc/zabbix-frontend-php/examples/apache.conf /etc/apache2/sites-enabled/apache.conf
# cat /etc/apache2/sites-enabled/apache.conf 
# Define /zabbix alias, this is the default
<IfModule mod_alias.c>
    php_value max_execution_time 300
    php_value memory_limit 128M
    php_value post_max_size 16M
    php_value upload_max_filesize 2M
    php_value max_input_time 300
    php_value date.timezone Europe/Riga
    Alias /zabbix /usr/share/zabbix
</IfModule>
```
启动apache   
```
#sudo service apache2 restart
```

3.8、配置Zabbix Web   
配置Web的过程略，需要注意事项。   
由于apache以www-data用户启动，而配置文件需要写道/etc/zabbix目录，所以需要对其授权。   
```
#chown  www-data.www.data  /etc/zabbix -R
```
在web页面安装完成后，可以将其权限改为Zabbix用户所有。   
```
#chown  zabbix.zabbix   /etc/zabbix -R
```
配置完成后，  
```
#cat /etc/zabbix/zabbix.conf.php 
<?php
// Zabbix GUI configuration file
global $DB;

$DB['TYPE']     = 'MYSQL';
$DB['SERVER']   = 'localhost';
$DB['PORT']     = '3306';
$DB['DATABASE'] = 'zabbix';
$DB['USER']     = 'zabbix';
$DB['PASSWORD'] = 'zabbix';

// SCHEMA is relevant only for IBM_DB2 database
$DB['SCHEMA'] = '';

$ZBX_SERVER      = 'localhost';
$ZBX_SERVER_PORT = '10051';
$ZBX_SERVER_NAME = 'zabbix-web-ui';

$IMAGE_FORMAT_DEFAULT = IMAGE_FORMAT_PNG;
?>
```

安装Zabbix-Agent    
```
#sudo apt-get update
#sudo apt-get install zabbix-agent
#sudo vim /etc/zabbix/zabbix_agentd.conf
Server=10.10.10.10
Hostname=Web-DB-001
#sudo service zabbix-agent restart
```



登录Zabbix Web   
访问http://10.10.10.10/zabbix   
Username = Admin   
Password = zabbix   








