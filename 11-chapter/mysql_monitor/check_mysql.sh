#!/bin/bash
#author:itnihao
#mail:itnihao@qq.com
#date 2013-12-18
#version v1.0
#function:use zabbix monitor mysql status
mysql=$(which mysql)
zabbix_sender=$(which zabbix_sender)
#注意，如果你的mysql是非标准安装，请写mysql的绝对路径
#mysql=/usr/bin/mysql
var=$2
MYSQL_USER=$3
MYSQL_PASSWORD=$4
MYSQL_Host=$5
[ "${MYSQL_USER}"     = '' ] &&  MYSQL_USER=itnihao
[ "${MYSQL_PASSWORD}" = '' ] &&  MYSQL_PASSWORD=www.itnihao.com
[ "${MYSQL_Host}"     = '' ] &&  MYSQL_Host=localhost

#zabbix-server IP address
Zabbix_Server=$(awk -F"," '/Server=/ {print $2}' /etc/zabbix/zabbix_agentd.conf|egrep -v "(^$)") 
#hostname in zabbix-server web (Hostname)
Hostname=$(egrep "\bHostname=\b" /etc/zabbix/zabbix_agentd.conf|awk -F"=" '{print $2}')


function status {
    [ "${var}" = '' ] && echo ""||${mysql} -u${MYSQL_USER} -p${MYSQL_PASSWORD} -h${MYSQL_Host} -e 'show status'|grep -v Variable_name|grep "\b${var}\b"|awk '{print $2}'
}

function  ping {
    /usr/bin/mysqladmin -u${MYSQL_USER} -p${MYSQL_PASSWORD} -h${MYSQL_Host} ping|grep alive|wc -l
}
function version {
    ${mysql}  -V | cut -f6 -d" " | sed 's/,//'
}

function slave_delay {
        info=$(${mysql} -u${MYSQL_USER} -p${MYSQL_PASSWORD} -h${MYSQL_Host} -e "show slave status\G;" | grep -E "Seconds_Behind_Master:[ ]*[0-9]+" | wc -l)
        if [ $info -eq 0 ]; then
            echo 99999
            exit 0
        else
            ${mysql} -u${MYSQL_USER} -p${MYSQL_PASSWORD} -h${MYSQL_Host} -e "show slave status\G;" | grep "Seconds_Behind_Master" | cut -d':' -f 2|sed "s/^ //g"
        fi
}
function slave_running_status {
        status=$(${mysql} -u${MYSQL_USER} -p${MYSQL_PASSWORD} -h${MYSQL_Host} -e "show slave status\G;")
        if [ "${status}" == "" ];then
            echo 0
        fi
        Slave_IO_Running="$(${mysql} -u${MYSQL_USER} -p${MYSQL_PASSWORD} -h${MYSQL_Host} -e "show slave status\G;" | grep "\bSlave_IO_Running\b"|column -t|awk '{print $2}'|sed "s/ //g")"
        Slave_SQL_Running="$(${mysql} -u${MYSQL_USER} -p${MYSQL_PASSWORD} -h${MYSQL_Host} -e "show slave status\G;" | grep "\bSlave_SQL_Running\b"|column -t|awk '{print $2}'|sed "s/ //g")"
        Slave_Last_IO_Error=$(${mysql} -u${MYSQL_USER} -p${MYSQL_PASSWORD} -h${MYSQL_Host} -e "show slave status\G;" | grep -E "\bLast_IO_Error\b"|column -t|sed "s/Last_IO_Error://g")
        Slave_Last_SQL_Error=$(${mysql} -u${MYSQL_USER} -p${MYSQL_PASSWORD} -h${MYSQL_Host} -e "show slave status\G;" | grep -E "\bLast_SQL_Error\b"|column -t|sed "s/Last_SQL_Error://g")
        Slave_Last_IO_Error_Timestamp=$(${mysql} -u${MYSQL_USER} -p${MYSQL_PASSWORD} -h${MYSQL_Host} -e "show slave status\G;"  |column -t| grep -E "\bLast_IO_Error_Timestamp\b")
        Slave_Last_SQL_Error_Timestamp=$(${mysql} -u${MYSQL_USER} -p${MYSQL_PASSWORD} -h${MYSQL_Host} -e "show slave status\G;" |column -t| grep -E "\bLast_SQL_Error_Timestamp\b")
        
        if [ "${Slave_Last_IO_Error}" != "" -o "${Slave_Last_SQL_Error}" != "" ];then
            msg="Slave_Last_IO_Error_Timestamp:=== ${Slave_Last_IO_Error_Timestamp}\n Slave_Last_IO_Error:=== "${Slave_Last_IO_Error}"\n${Slave_Last_SQL_Error_Timestamp}\nSlave_Last_SQL_Error:=== "${Slave_Last_SQL_Error}""
            ${zabbix_sender} -z ${Zabbix_Server} -p 10051 -s "${Hostname}" -k mysql_slave_error -o "${msg}" -vv
        elif    [ "${Slave_IO_Running}"  != "YES" -a "${Slave_SQL_Running}" != "YES" ];then
            echo 0
        elif  [ "${Slave_IO_Running}"  == "NO" ];then
            echo 1
        elif  [ "${Slave_SQL_Running}" == "NO" ];then
            echo 2
        else
            echo 3
        fi
       
}
case "$1" in
    status)
        status
        ;;
    ping)
        ping
        ;;
    version)
        version
        ;;
    slave_delay)
        slave_delay
        ;;
    slave_running_status)
        slave_running_status
        ;;
    *)
        echo "Usage: $0 {status| ping | version |slave_running_status}"
esac
