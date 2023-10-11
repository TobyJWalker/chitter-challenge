import os, peewee
from flask import Flask, request, render_template, redirect
from datetime import datetime
from lib.model_definition import User, Peep

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==
@app.route('/', methods=['GET'])
def index():
    return redirect('/home')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))

