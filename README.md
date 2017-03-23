# Description
Oracle database monitoring through Zabbix.
Basied on https://github.com/bicofino/Pyora

Scripts checks database's parameters and send data to zabbix server.

# Dependencies
oracle instantclient

zabbix-agent

python

cx-Oracle

python-argparse

py-zabbix


Installation
============
1. Create Oracle user for Pyora usage
<pre><code>
CREATE USER ZABBIX IDENTIFIED BY '<REPLACE WITH PASSWORD>' DEFAULT TABLESPACE SYSTEM TEMPORARY TABLESPACE TEMP PROFILE DEFAULT ACCOUNT UNLOCK;
GRANT CONNECT TO ZABBIX;
GRANT RESOURCE TO ZABBIX;
ALTER USER ZABBIX DEFAULT ROLE ALL;
GRANT SELECT ANY TABLE TO ZABBIX;
GRANT CREATE SESSION TO ZABBIX;
GRANT SELECT ANY DICTIONARY TO ZABBIX;
GRANT UNLIMITED TABLESPACE TO ZABBIX;
GRANT SELECT ANY DICTIONARY TO ZABBIX;
GRANT SELECT ON V_$SESSION TO ZABBIX;
GRANT SELECT ON V_$SYSTEM_EVENT TO ZABBIX;
GRANT SELECT ON V_$EVENT_NAME TO ZABBIX;
GRANT SELECT ON V_$RECOVERY_FILE_DEST TO ZABBIX;
</code></pre>


2. Install
	a. install oracle instantclient
	b. https://pypi.python.org/pypi/cx_Oracle/5.2.1
	c. https://github.com/blacked/py-zabbix

