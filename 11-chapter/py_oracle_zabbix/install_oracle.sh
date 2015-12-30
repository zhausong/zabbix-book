# assuming python and pip are already installed 
# installing the instantclient is usually where problems happen
 
# download the following files from oracle
#
#    oracle-instantclient11.2-basic-11.2.0.3.0-1.x86_64.rpm
#    oracle-instantclient11.2-devel-11.2.0.3.0-1.x86_64.rpm
#    oracle-instantclient11.2-sqlplus-11.2.0.3.0-1.x86_64.rpm
 
# install the rpms
rpm -ivh oracle-instantclient11.2-basic-11.2.0.3.0-1.x86_64.rpm 
rpm -ivh oracle-instantclient11.2-sqlplus-11.2.0.3.0-1.x86_64.rpm 
rpm -ivh oracle-instantclient11.2-devel-11.2.0.3.0-1.x86_64.rpm 
 
# the sqlplus package isn't specifically needed, but is usually useful for testing and command line sql connections
 
# configure oracle env (modify exact path based on version of rpm you download)
vim /etc/profile.d/oracle
 
#!/bin/bash
LD_LIBRARY_PATH="/usr/lib/oracle/11.2/client64/lib:${LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
TNS_ADMIN="/etc/oracle"
export TNS_ADMIN
ORACLE_HOME="/usr/lib/oracle/11.2/client64/lib"
export ORACLE_HOME
 
# copy/create your tnsnames.ora file
touch /etc/oracle/tnsnames.ora
 
# symlink headers to ORACLE_HOME to avoid "cannot locate Oracle include files" error
mkdir /usr/lib/oracle/11.2/client64/lib/sdk
ln -s /usr/include/oracle/11.2/client64 /usr/lib/oracle/11.2/client64/lib/sdk/include
 
# done. Install cx_Oracle
pip install cx_Oracle
#https://gist.github.com/jarshwah/3863378
