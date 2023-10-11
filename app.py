import os, peewee
from hashlib import sha256
from flask import Flask, request, render_template, redirect
from datetime import datetime
from lib.model_definition import User, Peep
from lib.validator import Validator

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==
@app.route('/', methods=['GET'])
def index():
    return redirect('/home')

@app.route('/home', methods=['GET'])
def home():
    peeps = sorted(Peep.select().limit(20), key=lambda p: p.timestamp, reverse=True)

    # get the users of the peeps
    users = {}
    for peep in peeps:
        users[peep.user] = User.get_by_id(peep.user).username

    return render_template('home.html', peeps=peeps, users=users)

@app.route('/<user>', methods=['GET'])
def get_user_peeps(user):
    account = User.select().where(User.username == user).get()

    peeps = sorted(Peep.select().where(Peep.user == account.id), key=lambda p: p.timestamp, reverse=True)

    return render_template('user.html', peeps=peeps, user=account.username)

@app.route('/search', methods=['POST'])
def search_for_user():
    username = request.form['username']

    if username == '' or username.isspace():
        return redirect('/home')
    else:
        try:
            user = User.select().where(User.username == username).get()
        except:
            return render_template('error.html', error_title='User not found', error_msg=f'@{username} could not be found.')

        return redirect(f'/{user.username}')

@app.route('/signup', methods=['GET'])
def get_signup_form():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def sign_up():
    vd = Validator()

    email = request.form['email']
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']
    password_confirm = request.form['password-confirm']

    valid_login, errors = vd.validate_signup(email, username, name, password, password_confirm)

    if valid_login:
        User(name=name, email=email, username=username, password=sha256(password.encode()).hexdigest()).save()
        return redirect('/home')
    else:
        return render_template('signup.html', errors=errors)


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))

