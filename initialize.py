import Model

import MySQLdb as mdb

from datetime import date

if __name__ == '__main__':

    try:
        con = mdb.connect(Model.dbHost, Model.dbUser, Model.dbPassword, Model.dbName);
        cur = con.cursor()
        cur.execute("SELECT VERSION()")

        ver = cur.fetchone()
                        
        print "Database version : %s " % ver

        cur.execute("DROP TABLE pollvote;")
        cur.execute("DROP TABLE pollitem;")
        cur.execute("DROP TABLE POLL;")

    except Exception as e:
        print "Some err on direct connect"
        print e

    Model.myDB.connect()

    try:
        Model.Poll.create_table()
    except Exception as e:
        print 'Cannot create table'
        print e

    try:
        Model.PollItem.create_table()
    except Exception as e:
        print 'Cannot create table'
        print e

    try:
        Model.PollVote.create_table()
    except Exception as e:
        print 'Cannot create table'
        print e

#    grandMa = Model.Person(name='Grand', birthday=date(1970, 1, 1), is_relative=True)
#    grandMa.save()
