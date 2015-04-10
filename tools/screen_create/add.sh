#!/bin/bash

for group in Zabbix-Server
do

    for items in "Memory usage" "CPU utilization" "Network TCP Connect status" "CPU load" 
        do
	k=$(echo ${items}|sed "s/ /_/g")
	python screen_creator.py -c config --add-all-group  ${group} "${items}" --hsize=2 --vsize=11 --width=500 --height=100 "${group}_${k}"
    done 
done
