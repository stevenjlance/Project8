import os
from app import app
from flask import render_template, request, redirect, session, url_for
from bson.objectid import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv


# events = [
#         {"event":"First Day of Classes", "date":"2019-08-21"},
#         {"event":"Winter Break", "date":"2019-12-20"},
#         {"event":"Finals Begin", "date":"2019-12-01"}
#     ]

from flask_pymongo import PyMongo

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# first load environment variables in .env
load_dotenv()

#IMPORT NAME
USER = os.getenv("MONGO_USERNAME")

#IMPORT PASSWORD
PASS = os.getenv("MONGO_PASSWORD")

# name of database
app.config['MONGO_DBNAME'] = 'database'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://'+USER+':'+PASS+'@cluster0-ggddx.mongodb.net/database?retryWrites=true&w=majority'

#app.config['MONGO_URI'] = 'mongodb+srv://admin:zhmy7dXZGlGPxYnj@cluster0-ggddx.mongodb.net/database?retryWrites=true&w=majority'
mongo = PyMongo(app)

# INDEX

@app.route('/')
@app.route('/index')

def index():
    #connect to db
    collection = mongo.db.events

    #find all data
    events = collection.find({})

    #return message to user
    return render_template('index.html',events = events)


# CONNECT TO DB, ADD DATA
@app.route('/add')

def add():
    # connect to the database
    events = mongo.db.events
    # insert new data
    events.insert({"event":"4th of July", "date":"2019-07-04"})
    # return a message to the user
    return "Events added"

#user to add a new event

@app.route('/events/new', methods = ['GET','POST'])
def new_event():
    if request.method == 'GET':
        return render_template('new_event.html')
    else:
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        user_name = request.form['user_name']
        description = request.form['description']
        #connect to database
        events = mongo.db.events

        #insert new data
        events.insert({'event':event_name,'date':event_date,'user':user_name,'about':description})

        #return message to user_name
        return redirect('/')

#SIGN UP
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name':request.form['username']})

        if existing_user is None:
            users.insert({'name': request.form['username'],'password': request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists! Try logging in!'

    return render_template('signup.html')

#LOGIN

@app.route('/login', methods=['POST'])

def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if request.form['password'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

#LOG OUT

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/name/<name>')
def name(name):
    #connect to db
    collection = mongo.db.events
    #find all data
    events = collection.find({'user':name})
    #return message to user
    return render_template('person.html',events = events)

@app.route('/event/<eventID>')
def event(eventID):
    #connect to db
    collection = mongo.db.events
    #find all data
    event = collection.find_one({'_id':ObjectId(eventID)})
    #return message to user
    return render_template('event.html',event = event)

#SHOW MY EVENTS
@app.route('/myevents/')
def myevents():
    #connect to db
    collection = mongo.db.events
    #find all data
    name = session['username']
    events = collection.find({'user':name})
    #return message to user
    return render_template('person.html',events = events)
