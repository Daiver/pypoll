#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/mysqldb-clean/build/lib.linux-x86_64-2.7/')
#sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/mysqldb/build/lib.linux-x86_64-2.7/')

from datetime import date

import MySQLdb as mdb

from Model import myDB, Person

#import peewee as pw
#myDB = pw.MySQLDatabase("pract", host="localhost", user="root", passwd="123")

#class Person(pw.Model):
    #name = pw.CharField()
    #birthday = pw.DateField()
    #is_relative = pw.BooleanField()

    #class Meta:
        #database = myDB

from bottle import route, run, template, request, Bottle

#app = Bottle()

#@route('/hello/<name>')
@route('/<name>')
def index(name):
    try:
        #con = mdb.connect('localhost', 'root', '123', 'pract');
        #cur = con.cursor()
        #cur.execute("SELECT VERSION()")

        #ver = cur.fetchone()

        myDB.connect()
        #Person.create_table()
        #uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15), is_relative=True)
        #uncle_bob.save()
        grandma = Person.select().where(Person.name == 'Bob').get()

        return template('templates/index.html', name=str(request.remote_addr),
                       info=str(grandma.name))
    except Exception, e:
        return template('templates/index.html', name='', info=(e))
    #return template('<b>Hello {{name}}</b>!', name=name)

if __name__ == '__main__':
    run(server='cgi')
