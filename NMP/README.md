===============
1.本RPM包，只支持centos6.X RHEL6.X，如果其他版本系统，需自行rpmbuild.

php安装之前需卸载系统自带的php版本

卸载命令为：rpm -qa|grep php|xargs rpm -e   
rpm -ivh \    
libicu-4.2.1-9.1.el6_2.x86_64.rpm  \   
libmcrypt-2.5.8-9.el6.x86_64.rpm    \       
libjpeg-turbo-1.2.1-1.el6.x86_64.rpm  \   
libtidy-0.99.0-19.20070615.1.el6.x86_64.rpm  \   
php-5.4.25-1.el6.x86_64.rpm   

默认已开启php-fpm服务(service php-fpm start)   
