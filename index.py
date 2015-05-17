#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/mysqldb-clean/build/lib.linux-x86_64-2.7/')
#sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/mysqldb/build/lib.linux-x86_64-2.7/')

from datetime import date
import string
import random

import MySQLdb as mdb

from Model import myDB, Person, Poll, PollItem, PollVote

from bottle import route, run, template, request, Bottle, post, redirect, response, error, abort

#app = Bottle()

def idGenerator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@route('/formtest')
def formtest():
    return template('templates/form.html', text='')

@post('/formtest')
def formtest():
    return template('templates/form.html', text=request.forms.get('name'))

#@route('/hello/<name>')
#@route('/<name>')
#def index1(name):
    #try:
        ##con = mdb.connect('localhost', 'root', '123', 'pract');
        ##cur = con.cursor()
        ##cur.execute("SELECT VERSION()")

        ##ver = cur.fetchone()

        #myDB.connect()
        ##Person.create_table()
        ##uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15), is_relative=True)
        ##uncle_bob.save()
        #grandma = Person.select().where(Person.name == 'Grand').get()

        #return template('templates/index.html', name=str(request.remote_addr),
                       #info=str(grandma.name))
    #except Exception, e:
        #return template('templates/index.html', name='', info=(e))
    ##return template('<b>Hello {{name}}</b>!', name=name)

#@error(404)
#def error404():
    #return template('templates/404.html')

#hostname = "http://192.168.10.101/cgi-bin/pypoll.py"

@route('/poll/<url>')
def poll(url):
    myDB.connect()
    try:
        poll = Poll.select().where(Poll.url == url).get()
        urlparts = request.urlparts
        return template('templates/poll.html', poll=poll, hostname=urlparts.scheme)
    except Exception as e:
        return template('templates/404.html', info=str(e))
    #abort(404, "No such poll")

@post('/vote')
def vote():
    url = request.forms.get("url")
    return redirect("poll/" + url, code=200)

@post('/newpoll')
def newpoll():
    countOfItems = int(request.forms.get('countOfItems'))
    url = idGenerator(20)
    caption = request.forms.get('caption')
    if caption == '':
        return template('templates/403.html')

    myDB.connect()
    poll = Poll(url=url, name=caption)
    poll.save()
    for i in xrange(1, countOfItems + 1):
        caption = request.forms.get('item_' + str(i))
        if caption == "":
            continue

        pollItem = PollItem(owner=poll, position=i, caption=caption)
        pollItem.save()

    return redirect('poll/' + url, code=200)

@route('/')
def index():
    return template('templates/newpoll.html')
    #return template('templates/base.html')

if __name__ == '__main__':
    run(server='cgi')
