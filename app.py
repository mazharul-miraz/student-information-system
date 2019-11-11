from flask import Flask
from flask import render_template, url_for, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.sisdb


app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        return Insertdata(request)
    else:
        return render_template('index.html')


def Insertdata(request):
    print('data post')
    Firstname = request.form['firstname']
    Lastname = request.form['lastname']
    Regno = request.form['regno']
    Year = request.form['year']
    Date = request.form['date']
    Domain = request.form['domain']
    Address = request.form['address']

    Olduser = db.user.find_one({
        'regno': Regno,
        # fieldName: FieldData
    })

    if Olduser != None:
        return 'This Email ID Already Exist'
    else:
        db.user.insert_one({
            'firstname': Firstname,
            'lastname': Lastname,
            'regno': Regno,
            'year': Year,
            'date': Date,
            'domain': Domain,
            'address': Address,
        })
    return redirect('/')


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        return SearchResult(request)
    else:
        return render_template('update.html')


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        return userdel(request)
    else:
        return render_template('delete.html')


def userdel(request):
    Regno = request.form['regno']

    deluser = db.user.find_one({
        'regno': Regno,
    })
    if deluser != None:
        db.user.delete_one({
            'regno': Regno
        })
        return redirect('/delete')
    else:
        return 'No user found'


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        return SearchResult(request)
    else:
        return render_template('search.html')


def SearchResult(request):

    Regno = request.form['regno']
    searchData = db.user.find_one({
        'regno': Regno,
    })
    if searchData == None:
        return 'no data found'
    else:
        print(searchData)
        return render_template('search.html', user=searchData)


@app.route('/viewall')
def viewall():
    users = db.user.find()
    user_list = []
    for i in users:
        user_list.append(i)
    return render_template('viewall.html', user=user_list)


@app.route('/viewall')
def login():
    return render_template('login.html')


@app.route('/sudo')
def sudo():
    return render_template('sudo.html')


if __name__ == '__main__':
    app.run(debug=True)
