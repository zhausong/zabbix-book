##《Zabbix企业级分布式监控系统》勘误列表

前言 陈益超改为陈艺超

P22  362+67+4=433  @一期一会     
P40  /etc/snmp/snmpd.conf  
P47 trends_unit(存储非符号的整数)更正为trends_uint表。
P56  将在（16.3）节中   
P62  图web app少了下划线   
P72 只有部分触发器（函数）  
P102 表 5-1 Name 选项，**$1、$2…$9** 指的是 Item Key 的第 **1、2…9** 个参数，原文说是「Item 名称」的参数。  
P103 表 5-1 Units 选项，与时间相关的单位 **unixtime**、**uptime**、**s** 全部是小写字母。首字母大写导致显示时不能正常转换。  
P124 开始部分应该概述功能，第二版增加 
P143 '15'（天）代表'86400s'（秒）更正为'1d'（天）代表'86400s'（秒)。@jun-东莞-运维
P153 表6-5 Recovery message写了两遍   @Miku酱
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

