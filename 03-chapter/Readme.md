```
# sh partitiontables.sh 
Ready to partition tables.

Ready to update permissions of Zabbix user to create routines

Enter root DB user: root
Enter root password: mysqlpassword     



Do you want to backup the database (recommended) (Y/n): y

Enter output file, press return for default of /tmp/zabbix.sql

Mysqldump succeeded!, proceeding with upgrade...


Ready to proceed:

Starting yearly partioning at: 2014
and ending at: 2014
With 90 days of daily history


Ready to proceed (Y/n): 
y
Altering table: history
Altering table: history_log
Altering table: history_str
Altering table: history_text
Altering table: history_uint
Altering table: trends
Altering table: trends_uint
Creating monthly partitions for table: trends
Creating monthly partitions for table: trends_uint
Creating daily partitions for table: history
Creating daily partitions for table: history_log
Creating daily partitions for table: history_str
Creating daily partitions for table: history_text
Creating daily partitions for table: history_uint


Ready to apply script to database, this may take a while.(Y/n): 
y
Altering tables
history
history_log
history_str
history_text
history_uint
trends
trends_uint
trends
trends_uint
history
history_log
history_str
history_text
history_uint
Installing procedures

Do you want to update the /etc/zabbix/zabbix_server.conf
to disable housekeeping (Y/n): n

Do you want to update the crontab (Y/n): y
The crontab entry can be either in /etc/cron.daily, or added
to the crontab for root

Do you want to add this to the /etc/cron.daily directory (Y/n): y

Enter email of who should get the daily housekeeping reports: 
```
