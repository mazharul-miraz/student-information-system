from flask import Flask, session
from flask import render_template, url_for, request, redirect
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = b'_5kmjiuhygtcuvib2u3biyuv90876rtxfcgvbi'

mongoConnect = MongoClient()
client = MongoClient('localhost', 27017)
db = client.sisdb


# USER LOGIN
@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        return userLogin(request)
    else:
        return render_template('login.html')


def userLogin(request):
    loginEmail = request.form['userLoginEmail']
    loginPsd = request.form['userLoginPsd']

    # check user in database
    newUser = db.user.find_one({"email": loginEmail})

    if newUser == None:  # user doesn't exist
        return 'Sorry This Not Registered A User'
    elif newUser['password'] != loginPsd:  # user exist
        return 'Wrong password'
    else:
        session['user'] = loginEmail
        # return 'volla!'
        return redirect(url_for('user'))


# *******CRUD Add User***********
@app.route('/user', methods=['POST', 'GET'])
def user():

    if request.method == 'POST':
        return newRecord(request)
    else:
        if 'user' in session:
            return render_template('user.html', user_email=session['user'])
        else:
            return redirect(url_for('login'))


def newRecord(request):
    user_firstname = request.form['firstname']
    user_lastname = request.form['lastname']
    user_regno = request.form['regno']
    user_domain = request.form['domain']
    user_year = request.form['year']
    user_bdate = request.form['bdate']
    user_address = request.form['address']

    existingRecord = db.user.find_one({"regno": user_regno})

    if existingRecord != None:
        return ' This Registration Number Already Exist'
    else:
        db.user.insert_one({
            "firstname": user_firstname,
            "lastname": user_lastname,
            "regno": user_regno,
            "domain": user_domain,
            "year": user_year,
            "bdate": user_bdate,
            "bdate": user_bdate,
            "address": user_address,
        })
        return render_template('user.html', user_email=session['user'], notification_text='User Added')
# *******CRUD Add User***********


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# *******CRUD Delete User***********
# USER DELETE
@app.route('/user_del', methods=['POST', 'GET'])
def user_del():
    if request.method == 'POST':
        return uderDel(request)
        # return render_template('user_del.html')
    else:
        return render_template('user_del.html')


def uderDel(request):
    delRegno = request.form['rmvrgno']

    delUser = db.user.find_one({
        'regno': delRegno,
    })

    if delRegno != None:
        db.user.delete_one({
            'regno': delRegno
        })
        return redirect('/user_del')
    else:
        return 'No user Found'


# USER SEARCH
@app.route('/user_src')
def user_src():
    return render_template('user_src.html')

# *********Update User Record************
# USER UPDATE
@app.route('/user_update', methods=['GET', 'POST'])
def user_update():
    if request.method == 'POST':
        return record_search(request)
    else:
        return render_template('user_update.html')


def record_search(request):
    search_key = request.form["request_type"]
    if search_key == 'search':
        search_id = request.form["updateregno"]
        UserExist = db.user.find_one({"regno": search_id})
        if UserExist != None:
            return render_template('user_update.html', user=UserExist)
        else:
            return render_template('user_update.html')
    else:
        return updateUser(request)
        render_template('user_update.html')


def updateUser():
    update_firstname = request.form["firstname"]
    update_lastname = request.form["lastname"]
    update_regno = request.form["regno"]
    update_domain = request.form["domain"]
    update_year = request.form["year"]
    update_date = request.form["date"]

# *********SHOW ALL Record************
@app.route('/all_record', methods=['POST', 'GET'])
def showAllRecord():
    if request.method == 'GET':
        return allrecord()
        print(1)
    else:
        return 'something went worng'


def allrecord():
    allRecordList = []
    recordList = db.user.find()
    for record in recordList:
        print(record)
        allRecordList.append(record)
    return render_template('all_record.html', allRecordList=allRecordList)


# *********SUPER ADMIN************

# SUPER USER
@app.route('/sudo')
def sudo():
    return render_template('sudo.html')


# VIEW ALL USER
@app.route('/all_user', methods=['GET'])
def view_all():
    return ShowallUser()


def ShowallUser():
    userList = []
    allUser = db.user.find()
    for user in allUser:
        userList.append(user)
    return render_template('all_user.html', userList=userList)


# REMOVE USER
@app.route('/removeuser/<user_email>', methods=['POST', 'GET'])
def removeUser(user_email):
    if request.method == 'GET':
        return user_del(user_email, request)
    else:
        return redirect(url_for('all_user'))


def user_del(user_email, request):
    db.user.delete_one({"email": user_email})
    return redirect(url_for('sudo'))
    # ADD A USER

# ADD USER
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        return CreateUser(request)
    else:
        print('something went wrong')
        return render_template('add_user.html')


def CreateUser(request):
    userEmail = request.form['email']
    userPassword = request.form['password']

    UserExist = db.user.find_one({"email": userEmail})

    if UserExist != None:
        print('UserExist')
        return " this user already exist"
    else:
        print('NOT UserExist')
        db.user.insert_one({"email": userEmail, "password": userPassword})
        return redirect(url_for('sudo'))

# *********SUPER ADMIN************


# DEBUGGER
app.run(debug=True)
