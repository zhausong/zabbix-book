#!/bin/bash
#author: itnihao
#mail: itnihao@qq.com
#http://wwww.itnihao.com

source /etc/bashrc
source /etc/profile

MySQL_USER=zabbix
MySQL_PASSWORD=zabbix
MySQL_HOST=localhost
MySQL_PORT=3306
MySQL_DUMP_PATH=/mysql_backup
MySQL_DATABASE_NAME=zabbix
DATE=$(date '+%Y-%m-%d')

[ -d ${MySQL_DUMP_PATH} ] || mkdir ${MySQL_DUMP_PATH}
cd ${MySQL_DUMP_PATH}
[ -d logs    ] || mkdir logs
[ -d ${DATE} ] || mkdir ${DATE}
cd ${DATE}


TABLE_NAME_ALL=$(mysql -u${MySQL_USER} -p${MySQL_PASSWORD} -P${MySQL_PORT} -h${MySQL_HOST} ${MySQL_DATABASE_NAME} -e "show tables"|egrep -v "(Tables_in_zabbix|history*|trends*|acknowledges|alerts|auditlog|events|service_alarms)")
for TABLE_NAME in ${TABLE_NAME_ALL}
do
    mysqldump -u${MySQL_USER} -p${MySQL_PASSWORD} -P${MySQL_PORT} -h${MySQL_HOST} ${MySQL_DATABASE_NAME} ${TABLE_NAME} >${TABLE_NAME}.sql
    sleep 1
done


[ "$?" == 0 ] && echo "${DATE}: Backup zabbix succeed"     >> ${MySQL_DUMP_PATH}/logs/ZabbixMysqlDump.log
[ "$?" != 0 ] && echo "${DATE}: Backup zabbix not succeed" >> ${MySQL_DUMP_PATH}/logs/ZabbixMysqlDump.log


cd ${MySQL_DUMP_PATH}/
rm -rf $(date +%Y%m%d --date='5 days ago')
exit 0
