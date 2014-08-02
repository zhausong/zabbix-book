#!/usr/bin/env python
# coding=utf8
# Last modified: 2014-08-02 14:11 
# Author: itnihao
# Mail: itnihao@qq.com
import json
devices_arry = []

f=open('/proc/mounts','r')
mounts_arry=f.read().split("\n")

for line in mounts_arry:
    if len(line) > 0:
        fs_arry=line.split()
        result=fs_arry[1].find('chroot')
        if result == -1:
            devices_arry += [{"{#FSNAME}":fs_arry[1],"{#FSTYPE}":fs_arry[2]}]

print json.dumps({'data':devices_arry},sort_keys=True,indent=7,separators=(',',':'))
