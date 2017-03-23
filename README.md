# Description
Oracle database monitoring through Zabbix.
Basied on https://github.com/bicofino/Pyora

Scripts checks database's parameters and send data to zabbix server.

pyora-discovery.py performs discovery databases asm volumes, tablespaces and users.
pyora-items-list.py gets items list from zabbix server that will be checked and creates item list file.
pyora-active.py performs requests to oracle database and sends report to zabbix server.
pyora_config.py contains zabbix login and password to oracle database. Its included in scrypts.

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
CREATE USER ZABBIX IDENTIFIED BY 'REPLACE WITH PASSWORD' DEFAULT TABLESPACE SYSTEM TEMPORARY TABLESPACE TEMP PROFILE DEFAULT ACCOUNT UNLOCK;
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

2. Create zabbix api user with read permissions on group where databases hosts will be

3. Install on the host from which the checks will be performed

	a. oracle instantclient

	b. https://pypi.python.org/pypi/cx_Oracle/5.2.1

	c. https://github.com/blacked/py-zabbix
	
	d. zabbix agent

4. Copy externalscripts/* to /usr/lib/zabbix/externalscripts/

5. chmod 755 /usr/lib/zabbix/externalscripts/pyora-active.py /usr/lib/zabbix/externalscripts/pyora-discovery.py /usr/lib/zabbix/externalscripts/pyora-items-list.py

6. Edit /usr/lib/zabbix/externalscripts/pyora_config.py

7. Copy zabbix_agentd.d/oracle_pyora.conf to /etc/zabbix/zabbix_agentd.d/ and restart zabbix agent

8. Create via zabbix web interface host from which the checks will be performed.

Fill macros:

	* {$ADDRESS} - address oracle database	








