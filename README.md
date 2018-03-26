##《Zabbix企业级分布式监控系统》
   本项目是《Zabbix企业级分布式监控系统》一书的附件部分(不仅限于附件，还有扩充内容)，该书可在各大网站买到。  
<table>
    <tr>
        <td>网站名称</td>
        <td>链接</td>
    </tr>
        <tr>
        <td>亚马逊</td>
        <td>http://www.amazon.cn/3/dp/B00MN6QEYK</td>
    </tr>
    <tr>
        <td>china-pub</td>
        <td>http://product.china-pub.com/4275086</td>
    </tr>
        <tr>
        <td>京东</td>
        <td>http://t.cn/RPY5JtR</td>
    </tr>
        <tr>
        <td>当当</td>
        <td>http://t.cn/RPHauKF</td>
    </tr>
    </tr>
        <tr>
        <td>官方收录地址</td>
        <td>http://www.zabbix.com/documentation.php</td>
    </tr>    
</table>

##### QQ交流群
```
本书的读者QQ群【Zabbix群加群验证信息：Zabbix监控】 ：
Zabbix企业级分布式监控 2群  189342378（500人可加） 
Zabbix企业级分布式监控 1群  271659981（1000人已满）
```
![图1](static/img/zabbix-QQ-group-1.jpeg)

### 勘误列表
```
https://github.com/itnihao/zabbix-book/blob/master/error-fix/README.md
```

### 该书的目录如下：   

第一部分Zabbix基础

第一章，监控系统简介
====================================
```
   1.1为何需要监控系统     
   1.2监控系统的实现 
   1.3监控系统的开源软件现状 
      1.3.1 MRTG
      1.3.2 Cacti
      1.3.3 SmokePing
      1.3.4 Graphite 
      1.3.5 Nagios
      1.3.6 Zenoss Core
      1.3.7 Ganglia 
      1.3.8 OpenTSDB
      1.3.9 Zabbix
   1.4监控系统的原理探究    
```
第二章，Zabbix简介  
==
```
   2.1 Zabbix的客户    
   2.2 使用Zabbix的准备    
   2.3 Zabbix为何物	    
   2.4 选择Zabbix的理由	    
   2.5 Zabbix的架构	    
   2.6 zabbix运行流程	    
   2.7 Zabbix功能特性	    
```
第三章，安装部署	    
==
```
   3.1 安装环境概述
       3.1.1 硬件条件
       3.1.2 软件条件 
       3.1.3 部署环境的考虑 
   3.2 zabbix_server服务端的安装	   
       3.2.1 安装 Zabbix-Server
       3.2.2 安装 MySQL 数据库服务  
       3.2.3 配置 zabbix_server.conf  
       3.2.4 防火墙、Selinux 和权限的设置  
       3.2.5 配置 Web 界面  
       3.2.6 故障处理 ....
   3.3 zabbix-agent客户端的安装	 
       3.3.1 安装 Zabbix-Agent 
       3.3.2 防火墙的设置
       3.3.3 配置 zabbix_agentd.conf 
   3.4 snmp监控方式的安装配置	    
   3.5 Windows上安装zabbix-agent	    
   3.6 其他平台的安装	    
   3.7 zabbix_get的使用	    
   3.8 zabbix术语（命令）相关	    
   3.9 Zabbix-server对数据的存储	 
        3.9.1 Zabbix 对数据存储 
        3.9.2 MySQL 表分区实例 
   3.10 Zabbix init脚本解释    	    
   3.11安全和高可用    	    
   3.12zabbix数据库的备份     	
```
第四章，快速配置使用	    
==
```
   4.1配置流程	    
   4.2主机组的添加	    
   4.3模板的添加	    
   4.4添加主机	    
   4.5 Graphs的配置	    
   4.6 screen的配置	    
   4.7 Slide shows的配置	    
   4.8 zatree的使用	    
   4.9 map的配置	    
   4.10 WEB监控	 
   4.10.1 Web 监控的原理 
       4.10.2 Web 监控指标 
       4.10.3 Zabbix 中 Web 监控的配置 
       4.10.4 认证的支持 
       4.10.5 触发器的设置 
       4.10.6 排错
   4.11 IT服务	    
   4.12报表	    
   4.13资产管理	    
```
第五章，深入配置使用	    
==
```
   5.1 Items的添加
       5.1.1 Items 的含义 
       5.1.2 如何添加 Items 
   5.2 Items key的添加	    
   5.3 ITEMS的类型	   
       5.3.1 Zabbix-Agent 
       5.3.2 Simple check
       5.3.3 日志监控方式 
       5.3.4 监控项计算(Calculated) 
       5.3.5 聚合检测(Aggregate)
       5.3.6 内部检测(Internal) 
       5.3.7 SSH、Telnet 和扩展检测 .
   5.4宏的配置	    
   5.5维护时间	    
   5.6事件确认	    
   5.7数据的导入导出配置	    
```
第六章 ，告警的配置	    
==
```
   6.1 告警的概述	    
   6.2Trigger的配置	
       6.2.1 Trigger 的状态 
       6.2.2 Trigger 的配置步骤
       6.2.3 Trigger 告警依赖 
       6.2.4 Trigger 正则中的单位
       6.2.5 Trigger 表达式举例
       6.2.6 Trigger 函数
   6.3添加 Actions	    
       6.3.1 Actions 概述
       6.3.2 Actions 的配置
       6.3.3 Conditions 的配置
       6.3.4 Operations 的功能
       6.3.5 告警消息发送的配置 
       6.3.6 执行远程命令的配置 
   6.4邮件告警配置实例	
       6.4.1 创建 Media 
       6.4.2 创建用户 
       6.4.3 创建 Actions
   6.4.2创建用户	    
   6.5自定义脚本告警	    
   6.6邮件告警脚本的配置实例	    
   6.7告警升级的机制	    
   6.8告警配置故障排查	    
```
   
第二部分，zabbix中级部分	    
=
第七章，监控方式剖析	    
==
```
   7.1 Zabbix支持的监控方式	    
   7.2 Zabbix监控方式的逻辑	    
   7.3 agent监控方式	    
   7.4 Trapper监控方式	    
        7.4.1 Trapper 的配置步骤
        7.4.2 Trapper 的配置示例
        7.4.3 使用 zabbix-sender 发送数据 
   7.5 SNMP监控方式	 
        7.5.1 SNMP 概述 
        7.5.2 SNMP 协议的运行
        7.5.3 SNMP 协议原理 
        ￼7.5.4 MIB 简
        7.5.5 SNMP 的相关术语 
        7.5.6 配置 Zabbix 以 SNMP 方式监控
   7.6 IPMI监控方式	    
   7.7 JMX监控方式	
        7.7.1 JMX 在 Zabbix 中的运行流程 
        7.7.2 配置 JMX 监控的步骤 
        7.7.3 安装 Zabbix-Java-Gateway 
        7.7.4 配置 Zabbix-Java-Gateway 
        7.7.5 监控 Java 应用程序
        7.7.6 自定义 JMX 的 Key 
        7.7.7 监控 Tomcat 
        7.7.8 Weblogic 的监控 
   7.8命令执行	    
```
第八章，分布式监控	    
==
```
   8.1代理架构	    
   8.2节点架构	    
   8.3主动模式和被动模式
        8.3.1 被动模式
        8.3.2 主动模式 
```
第九章，Zabbix与自动化运维	    
==
```
   9.1监控自动化	    
   9.2网络发现	    
   9.3主动方式的自动注册
        9.3.1 功能概述
        9.3.2 主动方式自动注册的配置
        9.3.3 使用 Host metadata 
        9.3.4 关于自动注册的注意事项 
   9.4 low level discovery	  
        9.4.1 现实案例需求 
        9.4.2 Zabbix 客户端配置 
        9.4.3 Low level discovery 自动发现脚本编写 
        9.4.4 自定义 Key 配置文件
        9.4.5 Web 页面添加 Low level discovery .
   9.5 Zabbix在自动化运维工具的使用	    
```
第十章，使用的经验技巧	    
==
```
   10.1如何有效的设置监控告警	    
   10.2监控项的使用技巧	    
   10.3触发器的使用技巧	    
   10.4触发器配置	    
   10.5谷歌浏览器告警插件	    
   10.6数据图断图的原因	   
```
第十一章，监控案例	    
==
```
   11.1监控tcp连接数	    
   11.2监控nginx	    
   11.3监控php-fpm	    
   11.4监控mysql	    
       11.4.1 用自带的模板监控 MySQL
       11.4.2 用 Percona Monitoring Plugins 监控 MySQL .
   11.5监控tomcat，weblogic
   11.6监控dell服务器	    
   11.7监控Cisco路由器	    
   11.8监控VMware	    
   11.9 hadoop监控	    
   11.10 更多监控	    
```

第三部分Zabbix高级部分
=
第十二章，性能优化	    
==
```
   12.1Zabbix的性能优化的概述	    
   12.2Zabbix的性能优化的依据	    
   12.3配置文件的参数优化	    
   12.4 Zabbix的架构优化	    
   12.5 Zabbix的items中工作模式以及Trigger的优化	    
   12.6 Zabbix的数据库优化	    
   12.7其他方面的	    
```
第十三章，Zabbix API的使用	    
==
```
   13.1 Zabbix API简介	    
   13.2什么是json-rpc	    
   12.3Zabbix API的使用流程
        13.3.1 使用 API 的基本步骤 
        13.3.2 如何使用官方文档获取帮助
        13.3.3 用 CURL 模拟 API 的使用 
        13.3.4 HTTP 头部 Content-Type 设置
        13.3.5 关于用户认证 
        13.3.6 获取主机信息(用 Python 写的示例) 
        13.3.7 添加 Host
        13.3.8 删除 Host
   13.4第三方zabbixAPI模块	    
```
第十四章，使用Zabbix协议	    
==
```
   14.1 Zabbix协议概述
   14.2 Zabbix sender协议
        14.2.1 Sender 数据发送 
        14.2.2 Server 对数据响应的处理 
        14.2.3 Zabbix-Sender 的实例
   14.2 Zabbix get协议
   14.2 Zabbix agent协议
```
第十五章，定制Zabbix安装包	    
==
```
   15.1为什么需要定制安装包	    
   15.2如何定制安装包	    
```
第十六章，大型分布式监控案例	    
==
```
   16.1监控系统构建的概述	    
   16.2监控环境架构图	    
   16.3架构实现的过程	  
       16.3.1 硬件和软件需求
       16.3.2 Zabbix DB 的安装
       16.3.3 安装 Zabbix-Server 
       16.3.4 安装 Zabbix-GUI
       16.3.5 安装 Zabbix-Proxy 
       16.3.6 配置 Zabbix-Agent 
   16.4业务相关的配置	    
       16.4.1 用户的配置 
       16.4.2 业务组的配置 
       16.4.3 监控模板的定制 
       16.4.4 自动发现的配置 
   16.5其他需求   
```
   
第四部分 附录	    
=
第十七章，源码安装及相关配置	    
==
```
   17.1安装zabbix-server	    
   17.2 Zabbix-agent的安装	    
   17.3 关于zabbix的升级	    
```
===
开源文档 
```
《Zabbix使用手册V2.0》下载地址http://pan.baidu.com/s/1qWDHXkK  提取密码为8kq4
```
