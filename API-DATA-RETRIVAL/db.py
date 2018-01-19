# -*- coding: utf-8 -*-

import MySQLdb
import os
import string
from _mysql_exceptions import Error

class DBconnection():
    configPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"config")
    config = open(configPath,"r").read()
    details = config.split("\n")
    _user = details[0].split(":")[1]
    _db = details[1].split(":")[1]
    _passwd = details[2].split(":")[1]
    _host = details[3].split(":")[1]
    _port = int(details[4].split(":")[1])
    printable = set(string.printable)

    def __init__(self):
        self.connection = MySQLdb.connect(host=DBconnection._host,
                             port=DBconnection._port,
                             user=DBconnection._user,
                             password=DBconnection._passwd,
                             db=DBconnection._db)

    def connect(self):
        try:
            self.connection = MySQLdb.connect(host=DBconnection._host,
                                          port=DBconnection._port,
                                          user=DBconnection._user,
                                          password=DBconnection._passwd,
                                          db=DBconnection._db)
        except Error as err:
            print(err)

        return self.connection

