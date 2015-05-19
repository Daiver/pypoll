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

from bottle import route, run, template, request, Bottle, post, redirect, response, error, abort, static_file

#app = Bottle()

def idGenerator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#hostname = "http://192.168.10.101/cgi-bin/pypoll.py"

@route('/info/<var>')
def infoView(var):
    return template('templates/404.html', info=var)


@route('/js/<filename>')
def server_js(filename):
    return static_file(filename, root='js/filename')

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

@route('/results/<url>')
def results(url):
    myDB.connect()
    try:
        poll = Poll.select().where(Poll.url == url).get()
        urlparts = request.urlparts
        hostUrl = '/'.join(urlparts.path.split('/')[:-2])
        labels = ["'%s'" % x for x in poll.items]
        jsData = """{
    labels: ['Italy', 'UK', 'USA', 'Germany', 'France', 'Japan'],
    datasets: [
        {
            label: '2010 customers #',
            fillColor: '#382765',
            data: [2500, 1902, 1041, 610, 1245, 952]
        },
    ]
};"""
        return template('templates/results.html', poll=poll, hostname=hostUrl, info="", jsData=jsData)
    except Exception as e:
        return template('templates/404.html', info=str(e))
 
@post('/vote')
def vote():
    #try:
    url    = request.forms.get("url")
    ip     = request.remote_addr
    token  = str(request.forms.get("token"))
    choice = request.forms.get('choice')
    if choice == None:
        return template('templates/403.html', info='Bad choice number')
    choice = int(choice)

    myDB.connect()
    poll = Poll.select().where(Poll.url == url).get()    
    pollItem = PollItem.select().where(PollItem.owner == poll, PollItem.position == choice).get()

    for item in poll.items:
        for vote in item.votes:
            if vote.addres == str(ip) and not poll.doubleIPAllowed:
                return template('templates/403.html', info='There is vote from your IP')
            if vote.token == token and not poll.doubleTokensAllowed:
                return template('templates/403.html', info='There is vote from your browser')
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
    allowDoubleIP     = request.forms.get('allowDoubleIP')
    allowDoubleTokens = request.forms.get('allowDoubleTokens')
    if caption == '':
        return template('templates/403.html', info='Caption cannot be empty')

    myDB.connect()
    poll = Poll(url=url, name=caption, doubleIPAllowed=(allowDoubleIP != None), doubleTokensAllowed=(allowDoubleTokens != None))
    poll.save()
    for i in xrange(1, countOfItems + 1):
        caption = request.forms.get('item_' + str(i))
        if caption == "":
            continue

        pollItem = PollItem(owner=poll, position=i, caption=caption)
        pollItem.save()

    urlparts = request.urlparts
    hostUrl = '/'.join(urlparts.path.split('/')[:-1])
    return redirect(hostUrl + '/poll/' + url, code=200)

@route('/')
def index():
    urlparts = request.urlparts
    return template('templates/newpoll.html', hostname=urlparts.path[:-1])
    #return template('templates/base.html')

if __name__ == '__main__':
    run(server='cgi')
