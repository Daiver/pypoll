import Model

from datetime import date

if __name__ == '__main__':
    Model.myDB.connect()
    Model.Person.create_table()
    grandMa = Person(name='Grand', birthday=date(1970, 1, 1), is_relative=True)
    grandMa.save()
