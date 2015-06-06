#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/mysqldb-clean/build/lib.linux-x86_64-2.7/')
#sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/mysqldb/build/lib.linux-x86_64-2.7/')

from datetime import date
import datetime

import MySQLdb as mdb

import peewee as pw

dbName     = "pract"
dbHost     = "localhost"
dbUser     = "root"
dbPassword = "123"

myDB = pw.MySQLDatabase(dbName, host=dbHost, user=dbUser, passwd=dbPassword)


class Poll(pw.Model):
    url             =    pw.CharField()
    name                = pw.CharField()
    created             = pw.DateTimeField(default=datetime.datetime.now)
    doubleIPAllowed     = pw.BooleanField(default=True)
    doubleTokensAllowed = pw.BooleanField(default=False)
    # = pw.BooleanField()

    class Meta:
        database = myDB

class PollItem(pw.Model):
    owner    = pw.ForeignKeyField(Poll, related_name='items')
    caption  = pw.CharField()
    position = pw.IntegerField()

    class Meta:
        database = myDB

class PollVote(pw.Model):
    pollItem = pw.ForeignKeyField(PollItem, related_name='votes')
    addres   = pw.CharField()
    token    = pw.CharField()

    class Meta:
        database = myDB

