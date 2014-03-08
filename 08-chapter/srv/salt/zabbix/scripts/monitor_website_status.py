#!/usr/bin/env python
# coding=utf8
# Filename: monitor_idc.py
# Last modified: 2013-04-23 16:54
# Author: itnihao
# Mail: admin@itnihao.com
# Description:

import urllib, urllib2,sys,re

monitor_item =  sys.argv[1]
idc =  sys.argv[2]
url  =  "http://www.iqm.cn/index.php/Member/RTTask/getmonitorInfoByAjax"
page_url =  "http://www.iqm.cn/index.php/Member/RTTask"
web_monitor =  "http://testidc.orshsoft.com"
data =  "monitorip="+idc + "&url="+web_monitor+"&host=0.0.0.0&bandwidth=512&task_type=get"
data =  data.encode("utf8")

def web_site_status():
    request  =  urllib2.Request(url,data)
    opener   =  urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response =  opener.open(request)
    the_page =  response.read()
    values   =  eval(the_page)
#for v in values:
#    for i in v:
#        print  i, "-------------",v[i]
    for v in values:
        code=v["time"]
        pat =  re.compile(r'HTTP.+?OK')
        code_status= re.findall(pat, code)
        if  monitor_item == "status":
            print str(code_status)[13:16]
        else:
            print v[monitor_item]



def idc_site():
    s=urllib2.urlopen(page_url).read()
    pat=re.compile(r'type="checkbox" value=".+?[0-9]+" id=')
    urls=    re.findall(pat, s)
    for i in urls:
        i=i.replace('type="checkbox" value="', '')
        idc= i.replace('" id=', '')
        print idc


#idc_site()
web_site_status()
