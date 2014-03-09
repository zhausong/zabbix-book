#!/bin/bash
#
# 
status1=$(ps aux|grep "/usr/sbin/zabbix_server" | grep -v grep | grep -v bash | wc -l)

if [ "${status1}" = "0" ]; then

        /etc/init.d/zabbix-server start
        sleep 3

        status2=$(ps aux|grep zabbix_server | grep -v grep | grep -v bash |wc -l)
        if [ "${status2}" = "0"  ]; then
                /etc/init.d/keepalived stop
        fi
fi
