#!/usr/bin/env python3
# coding: utf-8
# vim: tabstop=4 shiftwidth=4 expandtab smarttab noautoindent 
"""
	Based on: https://github.com/bicofino/Pyora
    Author: Danilo F. Chilene
	Email:	bicofino at gmail dot com

	Author: Aleksey A.
	Email: lelik.13a at gmail dot com
"""

import argparse
import cx_Oracle
import inspect
import json
import re
#import pyora_config
from configparser import ConfigParser
import os

version = 0.3


class Checks(object):
    def show_tablespaces(self):
        """List tablespace names in a JSON like format for Zabbix use"""
        sql = "SELECT tablespace_name FROM dba_tablespaces ORDER BY 1"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        key = ['{#TABLESPACE}']
        lst = []
        for i in res:
            d = dict(zip(key, i))
            lst.append(d)
        print ( json.dumps({'data': lst}) )

    def show_tablespaces_temp(self):
        """List temporary tablespace names in a JSON like
        format for Zabbix use"""
        sql = "SELECT TABLESPACE_NAME FROM DBA_TABLESPACES WHERE \
              CONTENTS='TEMPORARY'"

        self.cur.execute(sql)
        res = self.cur.fetchall()
        key = ['{#TABLESPACE_TEMP}']
        lst = []
        for i in res:
            d = dict(zip(key, i))
            lst.append(d)
        print ( json.dumps({'data': lst}) )

    def show_asm_volumes(self):
        """List als ASM volumes in a JSON like format for Zabbix use"""
        sql = "select NAME from v$asm_diskgroup_stat ORDER BY 1"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        key = ['{#ASMVOLUME}']
        lst = []
        for i in res:
            d = dict(zip(key, i))
            lst.append(d)
        print ( json.dumps({'data': lst}) )

    def show_users(self):
        """Query the list of users on the instance"""
        sql = "SELECT username FROM dba_users ORDER BY 1"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        key = ['{#DBUSER}']
        lst = []
        for i in res:
            d = dict(zip(key, i))
            lst.append(d)
        print ( json.dumps({'data': lst}) )


class Main(Checks):
    def __init__(self):

        parser = argparse.ArgumentParser()
        parser.add_argument('--address')
        parser.add_argument('--port', default=1521)
        parser.add_argument('--database')

        subparsers = parser.add_subparsers()

        for name in dir(self):
            if not name.startswith("_"):
                p = subparsers.add_parser(name)
                method = getattr(self, name)
                argnames = inspect.getargspec(method).args[1:]
                for argname in argnames:
                    p.add_argument(argname)
                p.set_defaults(func=method, argnames=argnames)
        self.args = parser.parse_args()

        config = ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), 'pyora_settings.ini'))

#        self.args.username = pyora_config.username
#        self.args.password = pyora_config.password
        if config.has_section(self.args.database):
            self.args.username = config.get(self.args.database, "username")
            self.args.password = config.get(self.args.database, "password")
        else:
            self.args.username = config.get("DEFAULT", "username")
            self.args.password = config.get("DEFAULT", "password")

    def db_connect(self):
        dsn = cx_Oracle.makedsn(self.args.address, self.args.port, self.args.database)
        self.pool = cx_Oracle.SessionPool(
            user=self.args.username,
            password=self.args.password,
            dsn=dsn,
            min=1,
            max=3,
            increment=1)
        self.db = self.pool.acquire()
        self.cur = self.db.cursor()

    def db_close(self):
        self.cur.close()
        self.pool.release(self.db)

    def __call__(self):
        try:
            a = self.args
            callargs = [getattr(a, name) for name in a.argnames]
            self.db_connect()
            try:
                return self.args.func(*callargs)
            finally:
                self.db_close()
        except Exception as err:
            print ("")
            print ( str(err) )


if __name__ == "__main__":
    main = Main()
    main()
