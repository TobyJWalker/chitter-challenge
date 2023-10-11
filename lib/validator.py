import re
from lib.model_definition import User, Peep

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
    
    def validate_signup(self, email, username, password, password_confirmation):
        errors = {'email': [], 'username': [], 'password': [], 'password_confirmation': []}
        valid = True

        if not self.validate_email(email):
            errors['email'].append('Invalid email format')
            valid = False
        
        if not self.validate_username(username):
            errors['username'].append('Username must be at least 3 characters')
            valid = False
        
        if not self.validate_password(password):
            errors['password'].append('Password must be at least 8 characters')
            errors['password'].append('Password must contain at least one number')
            errors['password'].append('Password must contain at least one uppercase letter')
            errors['password'].append('Password must contain at least one special character')
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