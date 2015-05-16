#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/mysqldb/build/lib.linux-x86_64-2.7/')

import MySQLdb

from bottle import route, run, template, request, Bottle

app = Bottle()

#@route('/hello/<name>')
@route('/<name>')
def index(name):
    return template('templates/index.html', name=str(request.remote_addr))
    #return template('<b>Hello {{name}}</b>!', name=name)

if __name__ == '__main__':
    run(server='cgi')
