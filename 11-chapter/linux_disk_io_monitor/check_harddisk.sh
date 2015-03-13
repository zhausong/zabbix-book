#!/bin/bash
# function:monitor redisstatus from zabbix
# License: GPL
# mail:admin@itnihao.com
# version:1.0 date:2013-02-04

diskname_discovery () {
    HardDisk=($(grep '\b[a-z][a-z][a-z]\+\b'  /proc/diskstats|awk '{print $3}'))
    [ "${HardDisk[0]}" == "" ] && exit
    printf '{\n'
    printf '\t"data":[\n'
    for((i=0;i<${#HardDisk[@]};++i))
    {
        num=$(echo $((${#HardDisk[@]}-1)))
        if [ "$i" != ${num} ];
        then
           printf "\t\t{ \n"
           printf "\t\t\t\"{#DISKNAME}\":\"${HardDisk[$i]}\"},\n"
        else
           printf  "\t\t{ \n"
           printf  "\t\t\t\"{#DISKNAME}\":\"${HardDisk[$num]}\"}]}\n"
        fi
    }
}

case "$1" in
diskname_discovery)
    diskname_discovery
    ;;
*)
    echo "Usage: $0 {diskname_discovery}"
    ;;
esac
