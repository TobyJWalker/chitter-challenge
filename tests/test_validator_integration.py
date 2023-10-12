from lib.validator import Validator
from lib.model_definition import User, Peep
from seeds.seed_db import seed_database

def test_validate_signup():
    seed_database()
    vd = Validator()

    attempt_1, _ = vd.validate_signup('twalker@outlook.com', 'twalker120', 'Tom Walker', '1@Password', '1@Password')
    assert attempt_1 == True

    attempt_2, errors = vd.validate_signup('twalkergmail.com', 'hi', '', 'pass', 'password')
    assert attempt_2 == False
    assert 'Invalid email format' in errors['email']
    assert 'Username must be at least 3 characters' in errors['username']
    assert 'Password must be at least 8 characters' in errors['password']
    assert 'Password must contain at least one number' in errors['password']
    assert 'Password must contain at least one uppercase letter' in errors['password']
    assert 'Password must contain at least one special character' in errors['password']
    assert 'Passwords do not match' in errors['password_confirmation']

    attempt_3, errors = vd.validate_signup('twalker@gmail.com', 'twalker', 'Tom Walker', 'Password@1', 'Password@1')
    assert attempt_3 == False
    assert 'Username already taken' in errors['username']
    assert 'Email already taken' in errors['email']

def test_validate_login():
    seed_database()
    vd = Validator()

    attempt_1, _ = vd.validate_login('twalker', 'tobypassword')
    assert attempt_1 == True

    attempt_2, errors = vd.validate_login('twalker', 'wrongpassword')
    assert attempt_2 == False
    assert 'Incorrect password' in errors['password']