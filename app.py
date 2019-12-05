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
        session['user_type'] = newUser['user_type']

        if newUser['user_type'] == 'sudo':
            return redirect(url_for('sudo'))
        else:
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

    existingRecord = db.user_records.find_one({"regno": user_regno})

    if existingRecord != None:
        return ' This Registration Number Already Exist'
    else:
        db.user_records.insert_one({
            "firstname": user_firstname,
            "lastname": user_lastname,
            "regno": user_regno,
            "domain": user_domain,
            "year": user_year,
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

    delUser = db.user_records.find_one({
        'regno': delRegno,
    })

    if delRegno != None:
        db.user_records.delete_one({
            'regno': delRegno
        })
        return redirect('/user_del')
    else:
        return 'No user Found'


# *********Search User Record************
@app.route('/user_src', methods=['POST', 'GET'])
def user_src():
    if request.method == 'POST':
        return search_user(request)
    else:
        return render_template('user_src.html')


def search_user(request):
    search_id = request.form['search_key']
    search_regno = db.user_records.find_one({
        'regno': search_id,
    })
    if search_regno == None:
        return 'No Reoard Found'
    else:
        return render_template('user_src.html', search_regno=search_regno)


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
        UserExist = db.user_records.find_one({"regno": search_id})
        if UserExist != None:
            return render_template('user_update.html', user=UserExist)
        else:
            return render_template('user_update.html')
    else:
        return updateUser(request)


def updateUser(request):
    update_firstname = request.form["firstname"]
    update_lastname = request.form["lastname"]
    update_regno = request.form["regno"]
    update_domain = request.form["domain"]
    update_year = request.form["year"]
    update_date = request.form["date"]
    update_address = request.form["address"]

    saved = db.user.update_one({
        "regno": update_regno
    }, {
        '$set': {
            "firstname": update_firstname,
            "lastname": update_lastname,
            "domain": update_domain,
            "year": update_year,
            "bdate": update_date,
            "address": update_address
        }
    })
    print(saved)  # for debugging
    return render_template('user_update.html')


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
@app.route('/sudo', methods=['GET', 'POST'])
def sudo():
    if request.method == ['POST']:
        return checkSudo()
    else:
        return render_template('sudo.html')


def checkSudo():
    sudo_useremail = request.form["userLoginEmail"]
    sudo_password = request.form["userLoginPsd"]

    NotExist = db.user.find({
        ""
    })

    #    if 'user' in session:
    #         return render_template('user.html', user_email=session['user'])
    #     else:
    #         return redirect(url_for('login'))


# VIEW ALL USER
@app.route('/all_user', methods=['GET'])
def view_all():
    return ShowallUser()


def ShowallUser():
    userList = []
    allUser = db.user.find({"user_type": "user"})
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
        db.user.insert_one(
            {"email": userEmail, "password": userPassword, "user_type": "user"})
        return redirect(url_for('sudo'))


@app.route('/crt_sudo', methods=['GET', 'POST'])
def createsuper_user():
    if request.method == 'POST':
        return create_sudo(request)
    else:
        return render_template('crt_sudo.html')


def create_sudo(request):
    sudo_email = request.form['semail']
    sudo_password = request.form['spassword']

    old_sudo = db.user.find_one({"email": sudo_email})

    if old_sudo != None:
        return 'this user already exist'
    else:
        db.user.insert_one(
            {"email": sudo_email, "password": sudo_password, "user_type": "sudo"})
        return render_template('crt_sudo.html')


@app.route('/all_sudo', methods=['GET'])
def all_sudo():
    if request.method == 'GET':
        return viewall_sudo(request)
    else:
        return render_template('all_sudo.html')


def viewall_sudo(request):
    superuser_arr = []
    allSudo = db.user.find({"user_type": "sudo"})
    for sudo in allSudo:
        superuser_arr.append(sudo)
    return render_template('all_sudo.html', sudouserList=superuser_arr)


# *********SUPER ADMIN************
# DEBUGGER
app.run(debug=True)
