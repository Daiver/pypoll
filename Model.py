#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/mysqldb-clean/build/lib.linux-x86_64-2.7/')
#sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/mysqldb/build/lib.linux-x86_64-2.7/')

from datetime import date

import MySQLdb as mdb

import peewee as pw
myDB = pw.MySQLDatabase("pract", host="localhost", user="root", passwd="123")

class Person(pw.Model):
    name = pw.CharField()
    birthday = pw.DateField()
    is_relative = pw.BooleanField()

    class Meta:
        database = myDB

class Poll(pw.Model):
    name    = pw.CharField()
    created = pw.DateField()
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

