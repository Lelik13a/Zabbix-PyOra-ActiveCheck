# Description
**WARNING** Breacking changes:

- Scripts updated from python2 to python3.

- Changed settings file: added support sections for multiple oracle SIDs. (configparser)

- Zabbix template updated from 3.2 version to 4.4 and added {$ORAPORT} macros.


Oracle database monitoring through Zabbix.

Based on https://github.com/bicofino/Pyora


Scripts checks database's parameters and send data to zabbix server.


**pyora-discovery.py** performs discovery databases asm volumes, tablespaces and users.

**pyora-items-list.py** gets items list from zabbix server that will be checked and creates item list file.

**pyora-active.py** performs requests to oracle database and sends report to zabbix server.

**pyora_settings.ini** contains zabbix login and password to oracle database. Its included in scripts.

# Dependencies
oracle instantclient

zabbix-agent

python 3

cx-Oracle

python-argparse

configparser

py-zabbix

Tested with python 3.6.8, cx-Oracle (7.3.0), py-zabbix (1.1.7)

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

2. Create zabbix api user in web-interface with read permissions on group, where databases hosts will be.

3. Install on the host from which the checks will be performed:

	a. oracle instantclient

	b. https://pypi.python.org/pypi/cx_Oracle

	c. https://github.com/blacked/py-zabbix
	
	d. zabbix agent

4. Copy externalscripts/* to /usr/lib/zabbix/externalscripts/

5. Set scripts mode bits:
<pre><code>
chmod 755 /usr/lib/zabbix/externalscripts/pyora-active.py /usr/lib/zabbix/externalscripts/pyora-discovery.py /usr/lib/zabbix/externalscripts/pyora-items-list.py
</code></pre>

6. Edit /usr/lib/zabbix/externalscripts/pyora_settings.ini

7. Copy zabbix_agentd.d/oracle_pyora.conf to /etc/zabbix/zabbix_agentd.d/ and restart zabbix agent.

8. Create directory which will be contains items list for every database.
<pre><code>
mkdir /usr/lib/zabbix/cache
chown zabbix:zabbix /usr/lib/zabbix/cache
</code></pre>

9. Import to zabbix "Template Pyora active send".

10. Create via zabbix web interface host, from which the checks will be performed.

Fill macros:

	* {$ADDRESS} - address oracle database	
	* {$DATABASE} - databases SID
	* {$ORAPORT} - oracle port
	* {$ZABBIXURL} - zabbix api URL, like "http://zabbix.net.local" (needed for pyora-items-list.py script)
	* {$ZABBIXUSER} - zabbix api user
	* {$ZABBIXPASSWORD} - zabbix api password
	* {$ASMHIGH} - warn level for asm volume fill in percents
	* {$HIGH} - warn level for tablespace fill in percents

Link "Template Pyora active send" to this host.

11. Create cron job with databases parameters, like:
<pre><code>
*/10 * * * * zabbix /usr/lib/zabbix/externalscripts/pyora-active.py  --address database_address --database database_SID
</code></pre>


12. Configure needed template and hosts items 

Usage and tests
=================
<pre><code>
# Show the tablespaces names in a JSON format
pyora-discovery.py --address db_address --database db_SID show_tablespaces

# Create items list for database "SID" with address "10.0.0.1". Zabbix host "SID on db_host" and zabbix API user/password: DBmonitor/pass
pyora-items-list.py  --zabbixurl http://zabbix.net.local --zabbixuser "DBmonitor" --zabbixpassword "pass" --hostname "SID on db_host" --address "10.0.0.1" --database "SID"


# pyora-active.py -h
pyora-active.py [-h] --address ADDRESS --database DATABASE
                       [--username USERNAME] [--password PASSWORD]
                       [--port PORT] [--ora1000] [--verbose]

optional arguments:
  -h, --help           show this help message and exit
  --address ADDRESS    Oracle database address
  --database DATABASE  Oracle database SID
  --username USERNAME  Oracle database user
  --password PASSWORD  Oracle database user's password
  --port PORT          Oracle database port
  --ora1000            recconnect to Oracle database when request tablespace's
                       size (bug 17897511)
  --verbose, -v        Additional verbose information


# Perform checks by items list and print additional verbose information for every check
pyora-active.py  --address 10.0.0.1 --database SID  -v

Processing: uptime
                        883231
Data to send:
[{"host": "SID on db_host", "value": "883231", "key": "uptime"}]
{"failed": 0, "chunk": 1, "total": 1, "processed": 1, "time": "0.000050"}


Processing: version
                        Oracle Database 11g Release 11.2.0.4.0 - 64bit Production
Data to send:
[{"host": "SID on db_host", "value": "Oracle Database 11g Release 11.2.0.4.0 - 64bit Production", "key": "version"}]
{"failed": 0, "chunk": 1, "total": 1, "processed": 1, "time": "0.000045"}
</code></pre>


