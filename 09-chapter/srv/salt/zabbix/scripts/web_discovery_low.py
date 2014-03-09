#!/usr/bin/env python 
# coding=utf8 
# Last modified: 2013-04-12 14:47 
# Author: itnihao 
# Mail: admin@itnihao.com 
 
import os 
import json 
 
r=open('WEB.txt','r').read().split() 
devices = [] 
 
for devpath in  r: 
        device = os.path.basename(devpath) 
        devices += [{'{#SITENAME}':device}] 
 
print json.dumps({'data':devices},sort_keys=True,indent=7,separators=(',',':'))

