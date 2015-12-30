#!/usr/bin/env python 
#coding=utf-8 
 
#导入模块，urllib2是一个模拟浏览器HTTP方法的模块
import json
import urllib2
import sys
from urllib2 import Request, urlopen, URLError, HTTPError
 
#url and url header 
#zabbix的api 地址，用户名，密码，这里修改为自己实际的参数
zabbix_url="http://zabbix-gui.itnihao.com/api_jsonrpc.php" 
zabbix_header = {"Content-Type":"application/json"} 
zabbix_user   = "admin" 
zabbix_pass   = "zabbix" 
auth_code     = ""
 
#auth user and password 
#用户认证信息的部分，最终的目的是得到一个SESSIONID
#这里是生成一个json格式的数据，用户名和密码
auth_data = json.dumps(
        {
            "jsonrpc":"2.0",
            "method":"user.login",
            "params":
                    {
                        "user":zabbix_user,
                        "password":zabbix_pass
                    },
            "id":0
        }) 
 
# create request object 
request = urllib2.Request(zabbix_url,auth_data) 
for key in zabbix_header: 
    request.add_header(key,zabbix_header[key]) 
 
#auth and get authid 
try: 
    result = urllib2.urlopen(request) 
    #对于出错新的处理
except HTTPError, e:
    print 'The server couldn\'t fulfill the request, Error code: ', e.code
except URLError, e:
    print 'We failed to reach a server.Reason: ', e.reason
else: 
    response=json.loads(result.read()) 
    result.close() 
    #判断SESSIONID是否在返回的数据中
    if  'result'  in  response:
        auth_code=response['result']
    else:
        print  response['error']['data']
  
# request json 
json_data={ 
        "method":"host.delete", 
        "params":['10113'] 
    }
json_base={
    "jsonrpc":"2.0",
    "auth":auth_code,
    "id":1
}
json_data.update(json_base)
#用得到的SESSIONID去通过验证，获取主机的信息（用http.get方法）
if len(auth_code) == 0:
    sys.exit(1)
if len(auth_code) != 0:
    get_host_data = json.dumps(json_data) 
  
    # create request object 
    request = urllib2.Request(zabbix_url,get_host_data) 
    for key in zabbix_header: 
        request.add_header(key,zabbix_header[key]) 
  
    # get host list 
    try: 
        result = urllib2.urlopen(request) 
    except URLError as e: 
        if hasattr(e, 'reason'): 
            print 'We failed to reach a server.' 
            print 'Reason: ', e.reason 
        elif hasattr(e, 'code'): 
            print 'The server could not fulfill the request.' 
            print 'Error code: ', e.code 
    else: 
        response = json.loads(result.read()) 
        result.close() 
        
        #将所有的主机信息显示出来
        print response
        #显示主机的个数
        print "Number Of Hosts: ", len(response['result']) 
