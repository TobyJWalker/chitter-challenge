This is a challenge project to make a twitter/X clone.

I will be using what I know about html, databases and flask to make this project.
I will also be experimenting with some basic css such as bootstrap.

## How to use

- Install psql
- Create 'chitter' database
- run 'python3 lib/model_definition.py' to create the tables

- Create an environment variable with an email and password for the email account you want to use to send emails from. Keys are EMAIL_ADDR and GMAIL_APP_PW. 

The last one is the password for the email account. This is needed because gmail requires an app password to be used for sending emails from a python script. This is a security feature. You can find out more about it here: https://support.google.com/accounts/answer/185833?hl=en

I can provide you with an email and password if you want to test the email functionality. Just ask me.

- Comment out the lines in app.py that sets the environment variable if you don't want to use email functionality or do not own a gmail account with two step verification.

- Run pipenv install to install dependencies
- Run pipenv shell to enter the virtual environment and load variables
- Run 'python3 app.py' to start the web server
- Run pytest to run any project tests

## Testing

Pytest is used to test this project.
The database is seeded using the seeds/seed_db.py file
This file uses peewee to seed the database with test data.

Make sure that the database and tables have been created before running tests.

## User Stories

STRAIGHT UP

As a Maker
So that I can let people know what I am doing
I want to post a message (peep) to chitter

As a maker
So that I can see what others are saying
I want to see all peeps in reverse chronological order

As a Maker
So that I can better appreciate the context of a peep
I want to see the time at which it was made

As a Maker
So that I can post messages on Chitter as me
I want to sign up for Chitter

HARDER

As a Maker
So that only I can post messages on Chitter as me
I want to log in to Chitter

As a Maker
So that I can avoid others posting messages on Chitter as me
I want to log out of Chitter

ADVANCED

As a Maker
So that I can stay constantly tapped in to the shouty box of Chitter
I want to receive an email if I am tagged in a Peep