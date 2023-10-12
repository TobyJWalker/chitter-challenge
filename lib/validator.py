import re
from lib.model_definition import User, Peep
from hashlib import sha256

class Validator:

    def validate_email(self, email):
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return True
        else:
            return False
    
    def validate_password(self, password):
        if len(password) < 8:
            return False
        
        if not any(char.isdigit() for char in password):
            return False
        
        if not any(char.isupper() for char in password):
            return False
        
        if not any(c in password for c in ['@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=']):
            return False
        
        return True

    def validate_username(self, username):
        if len(username) < 3:
            return False
        
        if username == '' or username.isspace():
            return False
        
        return True
    
    def validate_name(self, name):
        if name == '' or name.isspace():
            return False
        
        return True

    def validate_signup(self, email, username, name, password, password_confirmation):
        errors = {'email': [], 'username': [], 'name': [], 'password': [], 'password_confirmation': []}
        valid = True

        if not self.validate_email(email):
            errors['email'].append('Invalid email format')
            valid = False
        
        if not self.validate_username(username):
            errors['username'].append('Username must be at least 3 characters')
            valid = False
        
        if len(password) < 8:
            errors['password'].append('Password must be at least 8 characters')
            valid = False
        
        if not any(char.isdigit() for char in password):
            errors['password'].append('Password must contain at least one number')
            valid = False
        
        if not any(char.isupper() for char in password):
            errors['password'].append('Password must contain at least one uppercase letter')
            valid = False
        
        if not any(c in password for c in ['@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=']):
            errors['password'].append('Password must contain at least one special character')
            valid = False
        
        
        if not self.validate_name(name):
            errors['name'].append('Name must not be emptys')
            valid = False
        
        if password != password_confirmation:
            errors['password_confirmation'].append('Passwords do not match')
            valid = False
        
        try:
            User.select().where(User.username == username).get()
            errors['username'].append('Username already taken')
            valid = False
        except:
            pass
        
        try:
            User.select().where(User.email == email).get()
            errors['email'].append('Email already taken')
            valid = False
        except:
            pass
        
        return valid, errors

    def validate_login(self, username, password):
        errors = {'username': [], 'password': []}
        valid = True

        try:
            user = User.select().where(User.username == username).get()
        except:
            errors['username'].append('Username not found')
            valid = False
        
        if valid:
            if sha256(password.encode()).hexdigest() != user.password:
                errors['password'].append('Incorrect password')
                valid = False
        
        return valid, errors