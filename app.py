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
    return redirect(url_for('/'))




@app.route('/update')
def update():
    return render_template('update.html')


@app.route('/delete')
def delete():
    return render_template('delete.html')


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/viewall')
def viewall():
    return render_template('viewall.html')


if __name__ == '__main__':
    app.run(debug=True)
