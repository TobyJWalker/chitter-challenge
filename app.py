import os, peewee, re, smtplib, ssl
from email.message import EmailMessage
from hashlib import sha256
from flask import Flask, request, render_template, redirect, session
from datetime import datetime
from lib.model_definition import User, Peep
from lib.validator import Validator
from threading import Thread

EMAIL_ADDR = os.environ.get('EMAIL_ADDR')
GMAIL_APP_PW = os.environ.get('GMAIL_APP_PW')

def send_email(receiver, subject, content):
    # stop function if no email or password found
    if EMAIL_ADDR is None or GMAIL_APP_PW is None:
        return None
    
    em = EmailMessage()
    em.set_content(content)
    em['Subject'] = subject
    em['From'] = EMAIL_ADDR
    em['To'] = receiver
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as s:
        s.login(EMAIL_ADDR, GMAIL_APP_PW)
        s.sendmail(EMAIL_ADDR, [receiver], em.as_string())

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==

# redirect user to home page if they go to the root
@app.route('/', methods=['GET'])
def index():
    return redirect('/home')

# show the home page, load the 20 most recent peeps
@app.route('/home', methods=['GET'])
def home():
    peeps = sorted(Peep.select().limit(20), key=lambda p: p.timestamp, reverse=True)

    # get the users of the peeps
    users = {}
    for peep in peeps:
        users[peep.user] = User.get_by_id(peep.user).username
    
    # check session account still exists
    if 'user_id' in session:
        try:
            User.get_by_id(session['user_id'])
        except peewee.DoesNotExist:
            session.pop('user_id')

    return render_template('home.html', peeps=peeps, users=users, logged_in=session['user_id'] if 'user_id' in session else None)

# show the peeps of a specific user
@app.route('/user/<user>', methods=['GET'])
def get_user_peeps(user):
    # get the account of the user
    try:
        account = User.select().where(User.username == user).get()
    
    # return error page if user not found
    except:
        return render_template('error.html', error_title='User not found', error_msg=f'@{user} could not be found.')

    # get a sorted list of peeps from the user
    peeps = sorted(Peep.select().where(Peep.user == account.id), key=lambda p: p.timestamp, reverse=True)

    return render_template('user.html', peeps=peeps, user=account.username)

# search for a specific user
@app.route('/search', methods=['POST'])
def search_for_user():
    username = request.form['username'] # get username from form

    # do some error checking
    if username == '' or username.isspace():
        return redirect('/home')
    else:
        # get user from database
        try:
            user = User.select().where(User.username == username).get()
        
        # return error page if user not found
        except:
            return render_template('error.html', error_title='User not found', error_msg=f'@{username} could not be found.')

        return redirect(f'/user/{user.username}')

# display sign up page
@app.route('/signup', methods=['GET'])
def get_signup_form():
    return render_template('signup.html')

# sign up a new user
@app.route('/signup', methods=['POST'])
def sign_up():
    vd = Validator() # create a validator object

    # get form data
    email = request.form['email']
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']
    password_confirm = request.form['password-confirm']

    # validate the data
    valid_login, errors = vd.validate_signup(email, username, name, password, password_confirm)

    # if valid, create the user and log them in
    if valid_login:
        User(name=name, email=email, username=username, password=sha256(password.encode()).hexdigest()).save()
        session['user_id'] = User.select().where(User.username == username).get().id
        session['username'] = username
        return redirect('/home')
    
    # if not valid, show the errors
    else:
        return render_template('signup.html', errors=errors)

# log out the user
@app.route('/logout', methods=['POST'])
def logout():
    try:
        session.pop('user_id')
        session.pop('username')
    except:
        pass
    return redirect('/home')

# show the login page
@app.route('/login', methods=['GET'])
def show_login_form():
    return render_template('login.html')

# log in the user
@app.route('/login', methods=['POST'])
def login():
    vd = Validator() # create a validator object

    # get form data
    username = request.form['username']
    password = request.form['password']

    # validate the data
    valid_login, errors = vd.validate_login(username, password)

    # if valid, log the user in
    if valid_login:
        session['user_id'] = User.select().where(User.username == username).get().id
        session['username'] = username
        return redirect('/home')
    
    # if not valid, show the errors
    else:
        return render_template('login.html', errors=errors)

# create a new peep
@app.route('/peep', methods=['POST'])
def post_peep():
    # get the peep content
    peep = request.form['peep-input']

    # do some error checking
    if peep == '' or peep.isspace():
        return redirect('/home')
    elif len(peep) > 140:
        return render_template('error.html', error_title='Peep too long', error_msg='Peeps must be 140 characters or less.')
    elif 'user_id' not in session:
        return render_template('error.html', error_title='Not logged in', error_msg='You must be logged in to peep.')
    else:
        # create the peep
        Peep(user=session['user_id'], content=peep, timestamp=datetime.now()).save()

        # get any people tagged in the peep
        tagged = re.findall(r'@(\w+)[\W\D]', peep)

        # remove any possible trailing punctuation from the usernames and remove duplicates
        tagged_users = set(tagged)

        for username in tagged_users:
            try:
                # get the user and send them an email
                user = User.select().where(User.username == username).get()
                subject = f"You've been tagged!"
                content = f'You were tagged in a peep by @{session["username"]}.\n\n{peep}'

                # use multithreading to send the email so the user is not waiting
                Thread(target=send_email, args=(user.email, subject, content)).start()

            # if the user does not exist, do nothing
            except Exception as e:
                print(f'Could not send email to {username}')
                print(e)

        return redirect('/home')

# route for listing logged in users' mentions
@app.route('/mentions', methods=['GET'])
def get_mentions():
    # check if user is logged in
    if 'user_id' not in session or 'username' not in session:
        return render_template('error.html', error_title='Not logged in', error_msg='You must be logged in to view your mentions.')

    try:
        # get a list of peeps that mention the user
        peeps = Peep.select().where(Peep.content.contains(f'@{session["username"]}'))

        # get the users of the peeps
        users = {}
        for peep in peeps:
            users[peep.user] = User.get_by_id(peep.user).username

    except:
        peeps = []
        users = {}

    return render_template('mentions.html', peeps=peeps, users=users)


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.secret_key = 'Security is Crucial'
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))

