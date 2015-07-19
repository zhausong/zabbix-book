
概述
==
screen_create是一个批量创建screen的工具。  
功能：  
==
支持分组创建screen  
支持单个主机创建所有screen  
用法
==
可以用如下脚本创建一个分组的screen，包括 CPU TCP LOAD指标的screen，如需添加更多图，可以自行添加即可
```
#!/bin/bash
for group in Zabbix-Server
do

    for items in "Memory usage" "CPU utilization" "Network TCP Connect status" "CPU load" 
        do
	k=$(echo ${items}|sed "s/ /_/g")
	python screen_creator.py -c config --add-all-group  ${group} "${items}" --hsize=2 --vsize=11 --width=500 --height=100 "${group}_${k}"
    done 
done
```
