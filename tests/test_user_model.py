import peewee
from lib.model_definition import User
from seeds.seed_db import seed_database

'''
This file isn't really necessary as peewee is already tested by the developers
I use it to test my understanding of peewee
'''

def test_view_users():
    seed_database()

    users = User.select()
    assert len(users) == 3

def test_one_user():
    seed_database()

    user = User.get(User.name=='Toby Walker')
    assert user.username == 'twalker'

def test_create_user():
    seed_database()

    user = User(name='Test User', username='tuser',
                email='tuser@gmail.com', password='testpassword')
    user.save()

    assert len(User.select()) == 4