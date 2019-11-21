from flask import Flask
from flask import render_template, url_for, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://localhost:27017/')
db = client.sisdb
collection = db.sisdb


#USER LOGIN
@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        return
    else:
        return render_template('login.html')


# USER DASHBOARD
@app.route('/user')
def user():
    return render_template('user.html')


# USER DELETE
@app.route('/user_del')
def user_del():
    return render_template('user_del.html')


# USER SEARCH
@app.route('/user_src')
def user_src():
    return render_template('user_src.html')


# USER UPDATE
@app.route('/user_update')
def user_update():
    return render_template('user_update.html')


# SUPER USER
@app.route('/sudo')
def sudo():
    return render_template('sudo.html')


# VIEW ALL USER
@app.route('/all_user')
def view_all():
    return render_template('all_user.html')


# ADD A USER
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        return CreateUser()
    else:
        print('something went wrong')


app.run(debug=True)