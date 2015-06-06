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
    except Exception as e:
        print "Some err on direct connect"
        print e
        exit(1)

    cur.execute("DROP TABLE pollvote;")
    cur.execute("DROP TABLE pollitem;")
    cur.execute("DROP TABLE poll;")


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

    con.execute("ALTER TABLE pollvote CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;")
    con.execute("ALTER TABLE pollitem CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;")
    con.execute("ALTER TABLE poll CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;")

    #ALTER TABLE tablename CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;


#    grandMa = Model.Person(name='Grand', birthday=date(1970, 1, 1), is_relative=True)
#    grandMa.save()
