from lib.validator import *

def test_validate_email():
    vd = Validator()
    assert vd.validate_email('twalker@example.com')
    assert not vd.validate_email('twalkerexample.com')
    assert not vd.validate_email('twalker@examplecom')
    assert not vd.validate_email('@example.com')
    assert not vd.validate_email('twalker@.com')

def test_validate_password():
    vd = Validator()

    assert vd.validate_password('@1Password')
    assert vd.validate_password('Password@1')
    assert not vd.validate_password('password')
    assert not vd.validate_password('password1')
    assert not vd.validate_password('@password')
    assert not vd.validate_password('password@1')
    assert not vd.validate_password('Pass@1')

def test_validate_username():
    vd = Validator()

    assert vd.validate_username('twalker')
    assert not vd.validate_username('')
    assert not vd.validate_username(' ')