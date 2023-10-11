import os, peewee
from flask import Flask, request, render_template, redirect
from lib.database_connection import get_flask_database_connection
from datetime import datetime

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==



# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))

