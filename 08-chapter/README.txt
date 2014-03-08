```
shell#rpm  -ivh  http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm       
```
##install salt-master   
```
shell#yum  install  salt-master          
```

##install salt-minion
```
shell#yum  install salt-minion    
```
#configuration salt-minion   
```
shell#vim  /etc/salt/minion    
master: salt-master.itnihao.com     #master IP or DNS   
id: zabbix-agent.itnihao.com       #minion  ID   
```


#salt-key   
```
shell#salt-key -a zabbix-agent.itnihao.com   
```



#top.sls
```
shell#mkdir  /srv/salt/ 
```

#highstate
```
shell#salt  '*'  state.highstate
```
