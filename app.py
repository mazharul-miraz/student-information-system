from flask import Flask
from flask import render_template, url_for, request
from pymongo import MongoClient


client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.sisdb
print(db)




app = Flask(__name__)
@app.route('/',methods=['POST', 'GET'])
def main():
	if request.method == 'POST':
		return Insertdata(request)
	else:
		return render_template('index.html')

def Insertdata():
	Firstname = request.form['firstname']
	Lastname = request.form['lastname']
	Regno = request.form['regno']
	Year = request.form['year']
	Date = request.form['date']
	Domain = request.form['domain']
	Address = request.form['address']







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
   return 'all record goes here'










if __name__ == '__main__':
	app.run(debug=True)
