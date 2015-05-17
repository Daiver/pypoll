import Model

from datetime import date

if __name__ == '__main__':
    Model.myDB.connect()
    try:
        Model.Person.create_table()
    except Exception as e:
        print 'Cannot create table'
        print e
    grandMa = Model.Person(name='Grand', birthday=date(1970, 1, 1), is_relative=True)
    grandMa.save()
