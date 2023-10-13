'''

This file is used to reset the database with test data

'''

import peewee
from hashlib import sha256
from lib.model_definition import User, Peep


def seed_database():

    Peep.drop_table()
    User.drop_table()

    User.create_table()
    Peep.create_table()

    User(name='Toby Walker', username='twalker', email='twalker@gmail.com', password=sha256('tobypassword'.encode()).hexdigest()).save()
    User(name='John Doe', username='jdoe',  email='jdoe@outlook.com', password=sha256('johnpassword'.encode()).hexdigest()).save()
    User(name='Bill Gates', username='bgates', email='bgates@hotmail.com', password=sha256('billpassword'.encode()).hexdigest()).save()

    Peep(user=1, content='This is my first peep, I am Toby!').save()
    Peep(user=1, content='This is my second peep, I am Toby!').save()
    Peep(user=2, content='This is my first peep, I am John!').save()
    Peep(user=2, content='This is my second peep, I am John!').save()
    Peep(user=3, content='This is my first peep, I am Bill!').save()
    Peep(user=3, content='This is my second peep, I am Bill!').save()
