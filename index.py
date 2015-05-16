#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/mysqldb-clean/build/lib.linux-x86_64-2.7/')
#sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/mysqldb/build/lib.linux-x86_64-2.7/')

import MySQLdb as mdb

from bottle import route, run, template, request, Bottle

#app = Bottle()

#@route('/hello/<name>')
@route('/<name>')
def index(name):
    try:
        con = mdb.connect('localhost', 'root', '123', 'pract');
        cur = con.cursor()
        cur.execute("SELECT VERSION()")

        ver = cur.fetchone()
        return template('templates/index.html', name=str(request.remote_addr),
                       info=ver)
    except Exception, e:
        return template('templates/index.html', name='', info=(e))
    #return template('<b>Hello {{name}}</b>!', name=name)

if __name__ == '__main__':
    run(server='cgi')
