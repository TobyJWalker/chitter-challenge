'''

This file contains the model definitions for the database
It will let peewee know what tables to create

'''

import peewee
from datetime import datetime

db = peewee.PostgresqlDatabase('chitter')

class User(peewee.Model):

    name = peewee.CharField()
    username = peewee.CharField()
    email = peewee.CharField()
    password = peewee.CharField()

    class Meta:
        database = db
        table_name = 'users'
    

class Peep(peewee.Model):

    user = peewee.ForeignKeyField(User, backref='peeps')
    content = peewee.CharField()
    timestamp = peewee.DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = 'peeps'


def create_tables():
    db.connect()
    db.create_tables([User, Peep], safe=True)
    db.close()


if __name__ == '__main__':
    create_tables()