import re

class Validator:
    def __init__(self):
        from lib.model_definition import User, Peep

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