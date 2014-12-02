#!/bin/bash
# function:monitor redisstatus from zabbix
# License: GPL
# mail:admin@itnihao.com
# version:1.0 date:2013-02-04
#chmod 4755 $(which netstat)

redis_discovery () {
port=($(netstat -nlput|awk -F":" '/redis/ {print $0}'|awk -F: '{print $2}'|awk '{print $1}'|grep -v "^$"))
[ "${port[0]}" == "" ] && exit
    printf '{\n'
    printf '\t"data":[\n'
for((i=0;i<${#port[@]};++i))
{
        num=$(echo $((${#port[@]}-1)))
        if [ "$i" != ${num} ];
        then
           printf "\t\t{ \n"
           printf "\t\t\t\"{#REDISPORT}\":\"${port[$i]}\"},\n"
        else
           printf  "\t\t{ \n"
           printf  "\t\t\t\"{#REDISPORT}\":\"${port[$num]}\"}]}\n"
        fi
}
}


case "$1" in
redis_discovery)
    redis_discovery
    ;;
*)
    echo "Usage: $0 {redis_discovery}"
    ;;
esac
