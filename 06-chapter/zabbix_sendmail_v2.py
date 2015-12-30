#!/usr/bin/python 
#coding:utf-8 
#author: itnihao
#mail: itnihao@qq.com
#url: https://github.com/itnihao/zabbix-book/edit/master/06-chapter/zabbix_sendmail_v2.py
 
import smtplib 
from email.mime.text import MIMEText 
import os 
import argparse
import logging
import datetime
 
#QQ enterprise
#smtp_server = 'smtp.exmail.qq.com' 
#smtp_port = 25 
#smtp_user = 'itnihao_zabbix@itnihao.com'
#smtp_pass = '1234567890'

#163 Mail
#smtp_server = 'smtp.163.com' 
#smtp_port = 25 
#smtp_user = 'itnihao_zabbix@163.com'
#smtp_pass = '1234567890'

#QQ Mail
smtp_server ='smtp.qq.com'
smtp_port = 25 
smtp_user   ='itnihao_zabbix@qq.com'
smtp_pass   ='1234567890'

def send_mail(mail_to,subject,content): 
    msg = MIMEText(content,_subtype='plain', _charset='utf-8')
    msg['Subject'] = unicode(subject,'UTF-8')
    msg['From'] = smtp_user 
    msg['to'] = mail_to 
    global sendstatus
    global senderr
     
    try: 
        if smtp_port == 465:
            smtp = smtplib.SMTP_SSL()
        else:
            smtp = smtplib.SMTP() 
        smtp.connect(smtp_server,smtp_port) 
        smtp.login(smtp_user,smtp_pass) 
        smtp.sendmail(smtp_user,mail_to,msg.as_string()) 
        smtp.close() 
        print 'send ok'
        sendstatus = True 
    except Exception,e: 
        senderr=str(e)
        print senderr
        sendstatus = False 
     
def logwrite(sendstatus,mail_to,content):
    logpath='/var/log/zabbix/alert'

    if not sendstatus:
        content = senderr

    if not os.path.isdir(logpath):
        os.makedirs(logpath)

    t=datetime.datetime.now()
    daytime=t.strftime('%Y-%m-%d')
    daylogfile=logpath+'/'+str(daytime)+'.log'
    logging.basicConfig(filename=daylogfile,level=logging.DEBUG)
    os.system('chown zabbix.zabbix {0}'.format(daylogfile))
    logging.info('*'*130)
    logging.debug(str(t)+' mail send to {0},content is :\n {1}'.format(mail_to,content))


if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Send mail to user for zabbix alerting')
    parser.add_argument('mail_to',action="store", help='The address of the E-mail that send to user ')
    parser.add_argument('subject',action="store", help='The subject of the E-mail')
    parser.add_argument('content',action="store", help='The content of the E-mail')
    args = parser.parse_args()
    mail_to=args.mail_to
    subject=args.subject
    content=args.content

    send_mail(mail_to,subject,content)
    logwrite(sendstatus,mail_to,content)
