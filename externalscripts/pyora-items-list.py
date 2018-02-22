#!/usr/bin/python
from pyzabbix import ZabbixAPI
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--zabbixurl', required=True)
parser.add_argument('--zabbixuser', required=True)
parser.add_argument('--zabbixpassword', required=True)
parser.add_argument('--hostname', required=True)
parser.add_argument('--address', required=True)
parser.add_argument('--database', required=True)

args = parser.parse_args()

try:
    zapi = ZabbixAPI(
        args.zabbixurl, user=args.zabbixuser, password=args.zabbixpassword)
except Exception:
    sys.exit("Can't connect to Zabbix API")

path = "/usr/lib/zabbix/cache/items-" + args.address + "-" + args.database + ".list"
try:
    file = open(path, "w")
except IOError:
    sys.exit("Can't open items file list")

# get only enabled zabbix trapper items
for item in zapi.item.get(
        extendoutput=True,
        host=args.hostname,
        monitored=True,
        filter={'type': '2'}):

    # skip status check keyname
    if item['key_'] == "failedchecks": continue
    try:
        file.write("" + args.hostname + "," + item['key_'] + "\n")
    except IOError:
        sys.exit("Can't write to items list")

print "OK"
file.close()
