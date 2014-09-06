##《Zabbix企业级分布式监控系统》勘误列表



P22  362+67+4=433  @一期一会     
P40  /etc/snmp/snmpd.conf   
P56  将在（16.3）节中   
P62  图web app少了下划线   
P72 只有部分触发器（函数）  
P124 开始部分应该概述功能，第二版增加   
P161 表6-7的Description应该为Name   @cexpert   
P202 缺少proxy的数据同步参数，第二版增加    
P203 创建的数据库名称应该为   
```
shell# service mysqld start
shell# mysql -uroot -p
mysql> use zabbix_proxy;
mysql> create database zabbix_proxy character set utf8;
mysql> grant all privileges on zabbix_proxy.* to zabbix@localhost identified by 'zabbix'; 
mysql> flush privileges;
```
@唐文军  
P255 nginx监控脚本已经调整，见github-book 11章 fix   
P256 黑体字是一行的   
P265 使用的MySQL脚本需要改变，即261页的MySQL脚本需要改变，见github-book 11章 fix       

