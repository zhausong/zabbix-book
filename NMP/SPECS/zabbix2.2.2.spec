#
%define zabbix_group zabbix
%define zabbix_user zabbix

Name:	        zabbix	
Version:	2.2.2
Release:	0%{?dist}.zbx
Summary:	zabbix monitor
Vendor:         admin@itnihao.com

Group:	        System Environment/Daemons	
License:	GPL
URL:		http://www.zabbix.com
Source0:	http://downloads.sourceforge.net/project/zabbix/ZABBIX%20Latest%20Stable/2.2.2/zabbix-2.2.2.tar.gz
Source1:        zabbix_custom.tar.gz
Source2:        zabbix-apache-web.conf
Source3:        zabbix-java-gateway.init
Source4:        cmdline-jmxclient-0.10.3.jar
Source5:        zabbix_java_gateway_cmd
Source6:	zabbix-logrotate.in
Source7:	zabbix-nginx-web.conf

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRequires:	libssh2-devel
BuildRequires:	net-snmp-devel
BuildRequires:	curl-devel
BuildRequires:	unixODBC-devel
BuildRequires:	OpenIPMI-devel
BuildRequires:	java-devel >= 1.6.0

Requires(pre):  gcc
Requires(post): chkconfig	
Provides: Monitor

%description
 Zabbix is the ultimate open source availability and performance monitoring solution. Zabbix offers advanced monitoring, alerting, and visualization features today which are missing in other monitoring systems, even some of the best commercial ones

%package server
Summary:server version of zabbix
Group: System Environment/Daemons
#Requires:            libssh-devel 
Requires:            libssh2-devel 
Requires:            net-snmp-devel
Requires:            curl-devel
Requires:            fping
Requires:            unixODBC-devel 
Requires:            OpenIPMI-devel 
Requires:            libdbi-dbd-mysql      
Requires(post):      /sbin/chkconfig
Requires(preun):     /sbin/chkconfig
Requires(preun):     /sbin/service
Requires(postun):    /sbin/service

%description server
Zabbix server common files

%package agent
Summary:             Zabbix Agent
Group:               Applications/Internet
Requires(pre):       shadow-utils
Requires(post):      /sbin/chkconfig
Requires(preun):     /sbin/chkconfig
Requires(preun):     /sbin/service
Requires(postun):    /sbin/service

%description agent
The Zabbix client agent, to be installed on monitored systems.


%package proxy
Summary:             Zabbix Proxy
Group:               Applications/Internet
Requires(pre):       shadow-utils
Requires(post):      /sbin/chkconfig
Requires(preun):     /sbin/chkconfig
Requires(preun):     /sbin/service
Requires(postun):    /sbin/service
Requires:            fping

%description proxy
The Zabbix proxy


%package web-apache
Summary:             Zabbix Web for apache
Group:               Applications/Internet
BuildArch:           noarch
Requires(pre):       shadow-utils
Requires(post):      /sbin/chkconfig
Requires(preun):     /sbin/chkconfig
Requires(preun):     /sbin/service
Requires(postun):    /sbin/service
Requires:            httpd
Requires:            php
Requires:            php-mysql
Requires:            php-gd
Requires:            php-xml
Requires:            php-mbstring
Requires:            php-xmlrpc
Requires:            php-bcmath

%description web-apache
The Zabbix web-apache

%package web-nginx
Summary:             Zabbix Web for nginx
Group:               Applications/Internet
BuildArch:           noarch
Requires(pre):       shadow-utils
Requires(post):      /sbin/chkconfig
Requires(preun):     /sbin/chkconfig
Requires(preun):     /sbin/service
Requires(postun):    /sbin/service
Requires:	     nginx
%description web-nginx
The Zabbix web-nginx

%package java-gateway
Summary         : Zabbix java gateway
Group           : Applications/Internet
#Requires        : zabbix = %{version}-%{release}
Requires        : java >= 1.5.0
Requires(post)  : /sbin/chkconfig
Requires(preun) : /sbin/chkconfig
Requires(preun) : /sbin/service

%description java-gateway
The Zabbix java gateway

%package mysql
Summary         : Zabbix server mysql
Group           : Applications/Internet
%description mysql
The Zabbix mysql


%prep
%setup -q

%build
common_flags="
     --enable-dependency-tracking
     --enable-server
     --enable-proxy  
     --enable-java
     --enable-agent 
     --enable-ipv6
     --with-net-snmp
     --with-libcurl
     --with-openipmi
     --with-unixodbc
     --with-ldap
     --with-ssh2
     --with-libcurl
     --with-libxml2
     --sysconfdir=%{_sysconfdir}/zabbix
     --datadir=%{_sharedstatedir}
     "
%configure $common_flags --enable-server --with-mysql  --with-cc-opt="%{optflags} $(pcre-config --cflags)"
make %{?_smp_mflags}



%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{_sbindir}
%{__install} -d %{buildroot}%{_sysconfdir}/rc.d/init.d
%{__install} -d %{buildroot}%{_datadir}/%{name}
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}/scripts
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}/zabbix_agentd.conf.d
%{__install} -d %{buildroot}%{_mandir}/man1/
%{__install} -d %{buildroot}%{_mandir}/man8/
%{__install} -d %{buildroot}%{_localstatedir}/log/%{name}
%{__install} -d %{buildroot}%{_localstatedir}/run/%{name}
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}/externalscripts
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}/alertscripts
%{__install} -d %{buildroot}%{_datadir}/%{name}
%{__install} -d %{buildroot}%{_sysconfdir}/logrotate.d

%{__make} DESTDIR=$RPM_BUILD_ROOT install


%{__install} -m 755 misc/init.d/fedora/core/zabbix_agentd   $RPM_BUILD_ROOT%{_initrddir}/zabbix-agent
%{__install} -m 755 misc/init.d/fedora/core/zabbix_server   $RPM_BUILD_ROOT%{_initrddir}/zabbix-server
%{__install} -m 755 misc/init.d/fedora/core/zabbix_server   $RPM_BUILD_ROOT%{_initrddir}/zabbix-proxy
%{__install} -m 755 %{SOURCE3}                              $RPM_BUILD_ROOT%{_initrddir}/zabbix-java-gateway
%{__install} -m 755 %{SOURCE4}                              $RPM_BUILD_ROOT/usr/sbin/zabbix_java/lib/
%{__install} -m 755 %{SOURCE5}                              $RPM_BUILD_ROOT/usr/sbin/zabbix_java_gateway_cmd
%{__install} -d -m  755      $RPM_BUILD_ROOT%{_datadir}/%{name}-database/mysql/
%{__mv} database/mysql/*     $RPM_BUILD_ROOT%{_datadir}/%{name}-database/mysql/
%{__mv} frontends/php/*      $RPM_BUILD_ROOT%{_datadir}/%{name}


%{__sed} -i "s@BASEDIR=/usr/local@BASEDIR=/usr@g"                    $RPM_BUILD_ROOT%{_initrddir}/zabbix-server
%{__sed} -i "s@PIDFILE=/tmp@PIDFILE=/var/run/zabbix@g"               $RPM_BUILD_ROOT%{_initrddir}/zabbix-server
%{__sed} -i "s@BASEDIR=/usr/local@BASEDIR=/usr@g"                    $RPM_BUILD_ROOT%{_initrddir}/zabbix-agent
%{__sed} -i "s@PIDFILE=/tmp@PIDFILE=/var/run/zabbix@g"               $RPM_BUILD_ROOT%{_initrddir}/zabbix-agent
%{__sed} -i "s@BINARY_NAME=zabbix_server@BINARY_NAME=zabbix_proxy@g" $RPM_BUILD_ROOT%{_initrddir}/zabbix-proxy
%{__sed} -i "s@BASEDIR=/usr/local@BASEDIR=/usr@g"                    $RPM_BUILD_ROOT%{_initrddir}/zabbix-proxy
%{__sed} -i "s@PIDFILE=/tmp@PIDFILE=/var/run/zabbix@g"               $RPM_BUILD_ROOT%{_initrddir}/zabbix-proxy


install -m 0755 -p src/zabbix_server/zabbix_server $RPM_BUILD_ROOT%{_sbindir}/
install -m 0755 -p src/zabbix_proxy/zabbix_proxy   $RPM_BUILD_ROOT%{_sbindir}/
install -m 0755 -p src/zabbix_get/zabbix_get       $RPM_BUILD_ROOT%{_sbindir}/
install -m 0755 -p src/zabbix_sender/zabbix_sender $RPM_BUILD_ROOT%{_sbindir}/
install -m 0755 -p src/zabbix_agent/zabbix_agent   $RPM_BUILD_ROOT%{_sbindir}/
install -m 0755 -p src/zabbix_agent/zabbix_agentd  $RPM_BUILD_ROOT%{_sbindir}/
install -m 0644 -p conf/zabbix_server.conf         $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
install -m 0644 -p conf/zabbix_agent.conf          $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
install -m 0644 -p conf/zabbix_agentd.conf         $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
install -m 0644 -p conf/zabbix_proxy.conf          $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
install -m 0644 -p man/zabbix_agentd.man           $RPM_BUILD_ROOT%{_mandir}/man8/zabbix_agentd.8
install -m 0644 -p man/zabbix_server.man           $RPM_BUILD_ROOT%{_mandir}//man8/zabbix_server.8
install -m 0644 -p man/zabbix_proxy.man            $RPM_BUILD_ROOT%{_mandir}/man8/zabbix_proxy.8
install -m 0644 -p man/zabbix_get.man              $RPM_BUILD_ROOT%{_mandir}/man1/zabbix_get.1
install -m 0644 -p man/zabbix_sender.man           $RPM_BUILD_ROOT%{_mandir}/man1/zabbix_sender.1
#cp -ar frontends/php                               $RPM_BUILD_ROOT%{_datadir}/%{name}

%{__tar} xf %{SOURCE1} -C $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -m 0644 -p %{SOURCE2}  $RPM_BUILD_ROOT/%{_datadir}/%{name}
install -m 0644 -p %{SOURCE7}  $RPM_BUILD_ROOT/%{_datadir}/%{name}

sed -i \
    -e 's|# PidFile=.*|PidFile=%{_localstatedir}/run/%{name}/zabbix_agentd.pid|g' \
    -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/%{name}/zabbix_agentd.log|g' \
    -e '/# UnsafeUserParameters=0/aUnsafeUserParameters=1\n' \
    -e '/# Include.*zabbix_agentd.conf.d\//aInclude=\/etc\/zabbix\/zabbix_agentd.conf.d\/\n' \
    -e '/StartAgents=3/aStartAgents=5\n' \
    -e 's|# LogFileSize=.*|LogFileSize=0|g' \
    -e 's|Server=127.0.0.1$|Server=127.0.0.1,10.10.10.1|g' \
    -e 's|ServerActive=127.0.0.1$|ServerActive=127.0.0.1:10051,10.10.10.1:10051|g' \
    -e 's|# EnableRemoteCommands=0|EnableRemoteCommands=1|g' \
    -e 's|# LogRemoteCommands=0|LogRemoteCommands=1|g' \
    -e 's|LogFileSize=0|LogFileSize=10|g' \
    -e 's|/usr/local|/usr|g' \
     $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/zabbix_agentd.conf

sed -i \
    -e 's|/usr/local|/usr|g' \
    -e '/# UnsafeUserParameters=0/aUnsafeUserParameters=1\n' \
    -e 's@# Include=/usr/etc/zabbix_agentd.conf.d@Include=/etc/zabbix/zabbix_agentd.conf.d@g' \
     $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/zabbix_agent.conf

sed -i \
    -e 's|# PidFile=.*|PidFile=%{_localstatedir}/run/%{name}/zabbix_server.pid|g' \
    -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/%{name}/zabbix_server.log|g' \
    -e 's|# LogFileSize=.*|LogFileSize=0|g' \
    -e 's|^DBUser=root|DBUser=zabbix|g' \
    -e '/# DBPassword=/aDBPassword=zabbix\n' \
    -e 's|# DBSocket=/tmp/mysql.sock|DBSocket=%{_sharedstatedir}/mysql/mysql.sock|g' \
    -e 's|# ExternalScripts=\${datadir}/zabbix/externalscripts|ExternalScripts=%{_sysconfdir}/%{name}/externalscripts|' \
    -e '/^# AlertScriptsPath=/a \\nAlertScriptsPath=%{_sysconfdir}/%{name}/alertscripts' \
    -e '/^# SNMPTrapperFile=.*/a \\nSNMPTrapperFile=/var/log/snmptt/snmptt.log' \
    -e 's|/usr/local|/usr|g' \
     $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/zabbix_server.conf

sed -i \
    -e 's|# PidFile=.*|PidFile=%{_localstatedir}/run/%{name}/zabbix_proxy.pid|g' \
    -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/%{name}/zabbix_proxy.log|g' \
    -e 's|# LogFileSize=.*|LogFileSize=0|g' \
    -e 's|^DBUser=root|DBUser=zabbix|g' \
    -e '/# DBPassword=/aDBPassword=zabbix\n' \
    -e 's|# DBSocket=/tmp/mysql.sock|DBSocket=%{_sharedstatedir}/mysql/mysql.sock|g' \
    -e 's|# ExternalScripts=\${datadir}/zabbix/externalscripts|ExternalScripts=%{_sysconfdir}/%{name}/externalscripts|' \
    -e 's|/usr/local|/usr|g' \
     $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/zabbix_proxy.conf

# install log rotation
cat %{SOURCE6} | sed -e 's|COMPONENT|server|g' >      $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix-server
cat %{SOURCE6} | sed -e 's|COMPONENT|agentd|g' >      $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix-agent
cat %{SOURCE6} | sed -e 's|COMPONENT|proxy|g'  >      $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix-proxy

cat  $RPM_BUILD_ROOT/usr/sbin/zabbix_java/settings.sh | sed \
    -e 's|^PID_FILE=.*|PID_FILE="/var/run/zabbix/zabbix_java.pid"|g' \
    > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/zabbix_java_gateway.conf

# change log directory of zabbix_java.log
sed -i -e 's|/tmp/zabbix_java.log|/var/log/zabbix/zabbix_java_gateway.log|g' $RPM_BUILD_ROOT/usr/sbin/zabbix_java/lib/logback.xml


%{__rm} -rf $RPM_BUILD_ROOT/usr/bin

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT


%files server
%defattr(-,root,root,-)
%doc
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/log/%{name}
%attr(0775,root,zabbix)   %dir %{_localstatedir}/run/%{name}
%config(noreplace)  %{_sysconfdir}/%{name}/zabbix_server.conf
%config(noreplace)  %{_sysconfdir}/%{name}/scripts
%config(noreplace)  %{_sysconfdir}/logrotate.d/zabbix-server
%{_sbindir}/zabbix_sender
%{_sbindir}/zabbix_server
%{_sbindir}/zabbix_get

%{_initrddir}/zabbix-server

%config(noreplace) %{_sysconfdir}/%{name}/externalscripts
%config(noreplace) %{_sysconfdir}/%{name}/alertscripts

%{_mandir}/man8/zabbix_server.8*
%{_mandir}/man1/zabbix_get.1*
%{_mandir}/man1/zabbix_sender.1*

%files agent
%defattr(-,root,root,-)
%doc
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/log/%{name}
%attr(0775,root,zabbix) %dir %{_localstatedir}/run/%{name}
%attr(0775,root,zabbix) %dir %{_sysconfdir}/%{name}/zabbix_agentd.conf.d
%config(noreplace)  %{_sysconfdir}/%{name}/zabbix_agent.conf
%config(noreplace)  %{_sysconfdir}/%{name}/zabbix_agentd.conf
%config(noreplace)  %{_sysconfdir}/logrotate.d/zabbix-agent
%{_sbindir}/zabbix_sender
%{_sbindir}/zabbix_agent
%{_sbindir}/zabbix_agentd
%{_sbindir}/zabbix_get
%attr(0755,root,zabbix) %{_sysconfdir}/%{name}/scripts/*
%attr(0755,root,zabbix) %{_sysconfdir}/%{name}/zabbix_agentd.conf.d/*

%{_initrddir}/zabbix-agent

%{_mandir}/man8/zabbix_agentd.8*
%{_mandir}/man1/zabbix_get.1*
%{_mandir}/man1/zabbix_sender.1*


%files proxy
%defattr(-,root,root,-)
%doc
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/log/%{name}
%attr(0775,root,zabbix)   %dir %{_localstatedir}/run/%{name}
%config(noreplace)  %{_sysconfdir}/%{name}/zabbix_proxy.conf
%config(noreplace)  %{_sysconfdir}/%{name}/scripts
%config(noreplace)  %{_sysconfdir}/logrotate.d/zabbix-proxy
%{_sbindir}/zabbix_proxy
%{_initrddir}/zabbix-proxy

%{_mandir}/man8/zabbix_proxy.8*
%config(noreplace) %{_sysconfdir}/%{name}/externalscripts
%config(noreplace) %{_sysconfdir}/%{name}/alertscripts

%files web-apache
%defattr(-,root,root,-)
%config(noreplace) %{_datadir}/%{name}/*


%files web-nginx
%defattr(-,root,root,-)
%config(noreplace) %{_datadir}/%{name}/*


%files java-gateway
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_java_gateway.conf
%{_initrddir}/zabbix-java-gateway
%{_sbindir}/zabbix_java
%{_sbindir}/zabbix_java_gateway_cmd


%files mysql
%defattr(-,root,root,-)
%config(noreplace) %{_datadir}/%{name}-database/mysql/schema.sql
%config(noreplace) %{_datadir}/%{name}-database/mysql/images.sql
%config(noreplace) %{_datadir}/%{name}-database/mysql/data.sql



%post server
if [ $1 -eq 1 ]; then
/sbin/chkconfig zabbix-server on
/sbin/service zabbix-server start
fi
chown root:zabbix /bin/netstat
chmod 4755 /bin/netstat
chown root:zabbix $(which fping)
chmod 4755 $(which fping)

%post agent
if [ $1 -eq 1 ]; then
sed -i "s@Hostname=Zabbix server@Hostname=$HOSTNAME@g" /etc/zabbix/zabbix_agentd.conf
getent group zabbix >/dev/null || groupadd -r  zabbix
getent passwd zabbix >/dev/null || useradd -r -g zabbix -d %{_sharedstatedir}/zabbix -s   /sbin/nologin  -c "zabbix user" zabbix
/sbin/chkconfig zabbix-agent on
/sbin/service zabbix-agent start
chown root:zabbix /bin/netstat
chmod 4755 /bin/netstat
fi

%post proxy
if [ $1 -eq 1 ]; then
/sbin/chkconfig zabbix-proxy on
fi

%post mysql
sed -i.orig -e 's|/usr/bin/traceroute|/bin/traceroute|' /usr/share/zabbix-database/mysql/data.sql
cat<<EOF
#vim /etc/my.cnf
##################################################################################################################
[mysqld]
......
character-set-server=utf8
innodb_file_per_table=1
......
##################################################################################################################

#For zabbix server
##################################################################################################################
chkconfig mysqld on
service mysqld start
MysqlPassword=admin
#setting mysql server root password
mysqladmin -u root password  \${MysqlPassword}
mysql -uroot -p\${MysqlPassword} -e "create database zabbix character set utf8"
mysql -uroot -p\${MysqlPassword} -e "grant all privileges on zabbix.* to zabbix@localhost identified by 'zabbix'"
mysql -uroot -p\${MysqlPassword} -e "flush privileges"

#For zabbix Server; source zabbix server database
mysql -uzabbix -pzabbix zabbix < /usr/share/zabbix-database/mysql/schema.sql
mysql -uzabbix -pzabbix zabbix < /usr/share/zabbix-database/mysql/images.sql
mysql -uzabbix -pzabbix zabbix < /usr/share/zabbix-database/mysql/data.sql

service  zabbix-server start
##################################################################################################################

#For zabbix proxy 
##################################################################################################################
chkconfig mysqld on
service mysqld start
MysqlPassword=admin
#setting mysql server root password
mysqladmin -u root password  \${MysqlPassword}
mysql -uroot -p\${MysqlPassword} -e "create database zabbix_proxy character set utf8"
mysql -uroot -p\${MysqlPassword} -e "grant all privileges on zabbix_proxy.* to zabbix@localhost identified by 'zabbix'"
mysql -uroot -p\${MysqlPassword} -e "flush privileges"
#source zabbix proxy database
mysql -uzabbix -pzabbix zabbix_proxy < /usr/share/zabbix-database/mysql/schema.sql
##################################################################################################################
EOF

%post web-apache
#selinux 
setsebool httpd_can_network_connect on
setsebool -P  httpd_can_network_connect=true
semanage  port -a -t http_port_t -p tcp 10051
chcon  -R  -t  httpd_sys_content_rw_t    /usr/share/zabbix/conf

chown -R apache.apache  /usr/share/zabbix/zabbix
sed -i "s/;date.timezone =/date.timezone = Asia\/Shanghai/g"        /etc/php.ini
sed -i "s#max_execution_time = 30#max_execution_time = 300#g"       /etc/php.ini
sed -i "s#post_max_size = 8M#post_max_size = 32M#g"                 /etc/php.ini
sed -i "s#max_input_time = 60#max_input_time = 300#g"               /etc/php.ini
sed -i "s#memory_limit = 128M#memory_limit = 128M#g"                /etc/php.ini
sed -i "/;mbstring.func_overload = 0/ambstring.func_overload = 2\n" /etc/php.ini
#config apache
sed -i "s/DirectoryIndex index.html index.html.var/DirectoryIndex index.php index.html index.html.var/g" /etc/httpd/conf/httpd.conf
sed -i "s/ServerTokens OS/ServerTokens Prod/g"  /etc/httpd/conf/httpd.conf


[ -d "/etc/httpd/conf.d" ] &&  cp %{_datadir}/%{name}/zabbix-apache-web.conf /etc/httpd/conf.d &&chown -R apache.apache  %{_datadir}/%{name} && cat <<EOF
--------------------------------------------------------
   you installed Apache Server,the configuration file in /etc/httpd/conf.d/zabbix-apache-web.conf
--------------------------------------------------------
EOF
chkconfig httpd on
service httpd restart

[ -d "/etc/httpd/conf.d" ] || cat <<EOF
-------------------------------------------------------------------------------------------
   you should configure Web Server,the web file in %{_datadir}/%{name}
   shell# cp /etc/httpd/conf.d/zabbix-apache-web.conf /etc/httpd/conf.d
-------------------------------------------------------------------------------------------
EOF
cat <<EOF
---------------------------------------------------------------------------------------------
   Author:  itnihao    
   Mail:    admin@itnihao.com    
   Blog:    http://www.itnihao.com

   The felow command is already run:

   shell# yum  install httpd php php-mysql httpd-manual mod_ssl mod_perl mod_auth_mysql php-gd php-xml php-mbstring php-ldap php-pear php-xmlrpc php-bcmath mysql-connector-odbc mysql-devel libdbi-dbd-mysql net-snmp-devel curl-devel libcurl-devel libssh2-devel

   #setting /etc/php.ini for zabbix
   shell# sed -i "s/;date.timezone =/date.timezone = Asia\/Shanghai/g"        /etc/php.ini
   shell# sed -i "s#max_execution_time = 30#max_execution_time = 300#g"       /etc/php.ini
   shell# sed -i "s#post_max_size = 8M#post_max_size = 32M#g"                 /etc/php.ini
   shell# sed -i "s#max_input_time = 60#max_input_time = 300#g"               /etc/php.ini
   shell# sed -i "s#memory_limit = 128M#memory_limit = 128M#g"                /etc/php.ini
   shell# sed -i "/;mbstring.func_overload = 0/ambstring.func_overload = 2\n" /etc/php.ini

   #config apache
   shell# sed -i "s/DirectoryIndex index.html index.html.var/DirectoryIndex index.php index.html index.html.var/g" /etc/httpd/conf/httpd.conf
   shell# sed -i "s/ServerTokens OS/ServerTokens Prod/g"  /etc/httpd/conf/httpd.conf
   shell# cp /etc/httpd/conf.d/zabbix-apache-web.conf /etc/httpd/conf.d

   #selinux 
   shell# setsebool httpd_can_network_connect on
   shell# setsebool -P  httpd_can_network_connect=true
   shell# semanage  port -a -t http_port_t -p tcp 10051
   shell# chcon    -R  -t  httpd_sys_content_rw_t    /usr/share/zabbix/conf

   #startup apache service
   shell# chkconfig httpd on
   shell# service   httpd start
----------------------------------------------------------------------------------------------
EOF


%post web-nginx
#selinux 
setsebool httpd_can_network_connect on
setsebool -P  httpd_can_network_connect=true
semanage  port -a -t http_port_t -p tcp 10051
chcon  -R  -t  httpd_sys_content_rw_t    /usr/share/zabbix/conf

chown -R www.www  /usr/share/zabbix || chown -R nginx.nginx  /usr/share/zabbix || chown -R nobody.nobody  /usr/share/zabbix

#php.ini
sed -i "s/;date.timezone =/date.timezone = Asia\/Shanghai/g"        /etc/php.ini
sed -i "s#max_execution_time = 30#max_execution_time = 300#g"       /etc/php.ini
sed -i "s#post_max_size = 8M#post_max_size = 32M#g"                 /etc/php.ini
sed -i "s#max_input_time = 60#max_input_time = 300#g"               /etc/php.ini
sed -i "s#memory_limit = 128M#memory_limit = 128M#g"                /etc/php.ini
sed -i "/;mbstring.func_overload = 0/ambstring.func_overload = 2\n" /etc/php.ini

#config nginx
grep "include /etc/nginx/conf.d/*.conf" /etc/nginx/nginx.conf
[ -d "/etc/nginx/conf.d/" ] 
status="$?"

if   [ "${status}" != 0 ] 
then
     mkdir /etc/nginx/conf.d/
elif [ "${status}" == 0 ] 
then
    mkdir /etc/nginx/conf.d/bak
    mv /etc/nginx/conf.d/*.conf  /etc/nginx/conf.d/bak
    cp /usr/share/zabbix/zabbix-nginx-web.conf /etc/nginx/conf.d/
fi

[ -f "/etc/init.d/php-fpm" ]
if [ "$?" == 0 ]
then
    #从php-fpm.conf里面读取是用sock还是tcp port方式
    sock=$(egrep "^listen.*=.*" /etc/php-fpm.conf|cut -d "=" -f2|sed "s/ //g"||egrep "^listen.*=.*" /etc/php/php-fpm.conf|cut -d "=" -f2|sed "s/ //g"||egrep "^listen.*=.*" /etc/php.d/php-fpm.conf|cut -d "=" -f2|sed "s/ //g")
    Isexistport=$(echo ${sock}|egrep "[0-9]+.")
    if   [ "${sock}" == "" ]
    then
        sed -i "/;listen = 127.0.0.1:9000/alisten = /var/run/php/php-fpm.sock"
    elif [ "${sock}" != "/var/run/php/php-fpm.sock" -a "${Isexistport}" == "" ]
    then
        sed -i "s@/var/run/php/php-fpm.sock@${sock}/g" /etc/nginx/conf.d/zabbix-nginx-web.conf
    elif [ "${Isexistport}" != "" ] 
    then
        sed -i -e "s@fastcgi_pass   unix:/var/run/php/php-fpm.sock;@fastcgi_pass ${Isexistport}@g" /etc/nginx/conf.d/zabbix-nginx-web.conf
        
    fi 
    service php-fpm restart
else
   echo "/etc/init.d/php-fpm doesn't exist"  
fi
service nginx restart

%post java-gateway
/sbin/chkconfig --add zabbix-java-gateway
chkconfig zabbix-java-gateway on


%pre server
#add zabbix to services
grep zabbix /etc/services
[ "$?" != 0 ] && cat >> /etc/services <<EOF
zabbix-agent    10050/tcp               #Zabbix Agent
zabbix-agent    10050/udp               #Zabbix Agent 
zabbix-trapper  10051/tcp               #Zabbix Trapper 
zabbix-trapper  10051/udp               #Zabbix Trapper
EOF
# Add the "zabbix" user
getent group zabbix >/dev/null || groupadd -r  zabbix
getent passwd zabbix >/dev/null || useradd -r -g zabbix -d %{_sharedstatedir}/zabbix -s   /sbin/nologin  -c "zabbix user" zabbix

%pre agent
#add zabbix to services
grep zabbix /etc/services
[ "$?" != 0 ] && cat >> /etc/services <<EOF
zabbix-agent    10050/tcp               #Zabbix Agent
zabbix-agent    10050/udp               #Zabbix Agent 
zabbix-trapper  10051/tcp               #Zabbix Trapper 
zabbix-trapper  10051/udp               #Zabbix Trapper
EOF
# Add the "zabbix" user
getent group zabbix >/dev/null || groupadd -r  zabbix
getent passwd zabbix >/dev/null || useradd -r -g zabbix -d %{_sharedstatedir}/zabbix -s   /sbin/nologin  -c "zabbix user" zabbix


%preun server
if [ "$1" = 0 ]
then
  /sbin/service zabbix_server stop >/dev/null 2>&1
  /sbin/chkconfig --del zabbix_server
fi

%preun proxy
if [ "$1" = 0 ]
then
  /sbin/service zabbix_proxy stop >/dev/null 2>&1
  /sbin/chkconfig --del zabbix_proxy
fi

%preun agent
if [ "$1" = 0 ]
then
  /sbin/service zabbix_agentd stop >/dev/null 2>&1
  /sbin/chkconfig --del zabbix_agentd
fi


%preun java-gateway
if [ $1 -eq 0 ]
then
  /sbin/service zabbix-java-gateway stop >/dev/null 2>&1
  /sbin/chkconfig --del zabbix-java-gateway
fi


%changelog
* Sun Feb 23 2014  update to 2.2.2 version <admin@itnihao.com>
- add nginx web server
- change init name zabbix_server to zabbix-server etc.

* Tue Nov 5  2013  update to 2.1.9 version <admin@itnihao.com>
- 2.1.9

* Tue Oct 30 2013  add java_gateway <admin@itnihao.com>
- 2.0.8

* Mon Sep 30 2013  update to 2.0.8 version <admin@itnihao.com>
- 2.0.8

* Fri Jul  5 2013  update to 2.0.6 version <admin@itnihao.com>
- 2.0.6

* Mon Feb 18 2013  changed file for agentd <admin@itnihao.com>
- 2.0.5

* Fri Jan 25 2013  First version is build ok <admin@itnihao.com>
- 2.0.4
