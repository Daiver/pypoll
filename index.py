#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/mysqldb-clean/build/lib.linux-x86_64-2.7/')
#sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/mysqldb/build/lib.linux-x86_64-2.7/')

from datetime import date
import string
import random

import MySQLdb as mdb

from Model import myDB, Poll, PollItem, PollVote

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


#hostname = "http://192.168.10.101/cgi-bin/pypoll.py"

@route('/poll/<url>')
def poll(url):
    myDB.connect()
    try:
        poll = Poll.select().where(Poll.url == url).get()
        urlparts = request.urlparts
        hostUrl = '/'.join(urlparts.path.split('/')[:-2])
        return template('templates/poll.html', poll=poll, hostname=hostUrl, info="")
    except Exception as e:
        return template('templates/404.html', info=str(e))
    #abort(404, "No such poll")

@post('/vote')
def vote():
    #try:
    url    = request.forms.get("url")
    ip     = request.remote_addr
    token  = str(ip)
    choice = int(request.forms.get('choice'))

    myDB.connect()
    poll = Poll.select().where(Poll.url == url).get()    
    pollItem = PollItem.select().where(PollItem.owner == poll, PollItem.position == choice).get()

    for item in poll.items:
        for vote in item.votes:
            if vote.addres == str(ip) and not poll.doubleIPAllowed:
                return template('templates/403.html', info='There is vote from your IP')
            if vote.token == token and not poll.doubleTokensAllowed:
                return template('templates/403.html', info='There is vote from your IP')
    pollVote = PollVote(pollItem=pollItem, addres=str(ip), token=token)
    pollVote.save()

    urlparts = request.urlparts
    hostUrl = '/'.join(urlparts.path.split('/')[:-1])
    return redirect(hostUrl + "/poll/" + url, code=200)
#    except Exception as e:
#        return template('templates/404.html', info=str(e))

@post('/newpoll')
def newpoll():
    countOfItems = int(request.forms.get('countOfItems'))
    url = idGenerator(20)
    caption = request.forms.get('caption')
    if caption == '':
        return template('templates/403.html', info='Caption cannot be empty')

    myDB.connect()
    poll = Poll(url=url, name=caption)
    poll.save()
    for i in xrange(1, countOfItems + 1):
        caption = request.forms.get('item_' + str(i))
        if caption == "":
            continue

        pollItem = PollItem(owner=poll, position=i, caption=caption)
        pollItem.save()

    urlparts = request.urlparts
    hostUrl = '/'.join(urlparts.path.split('/')[:-1])
    return redirect(hostUrl + 'poll/' + url, code=200)

@route('/')
def index():
    urlparts = request.urlparts
    return template('templates/newpoll.html', hostname=urlparts.path)
    #return template('templates/base.html')

if __name__ == '__main__':
    run(server='cgi')
