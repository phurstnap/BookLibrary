from flask import Flask, render_template, redirect, url_for, request
import models as dbHandler
app = Flask(__name__)

@app.route('/login/', methods=['GET', 'POST'])
def login():
	if request.method=='POST':
		username = request.form['username']
		password = request.form['password']
		users = dbHandler.retrieveUsers()
		return render_template('user.html', users)
	else:
		return render_template('login.html')

@app.route('/register/', methods=['GET', 'POST'])
def register(error = None):
	if request.method=='POST':
		username = request.form['username']
		password = request.form['password']
		dbHandler.insertUser(username,password)
		return render_template('login.html')
	else:
		return render_template('register.html')
		
@app.route('/user')
def user(name = None):
	return render_template('user.html')
	
@app.route('/db')
def db():
	db.cursor().execute(""" CREATE TABLE user(username text, password text)""")
	return render_template('register.html')
	
@app.route('/')
def redirects():
	return redirect('login')
	
@app.errorhandler(404)
def handler404(e):
	return render_template('404.html')


if __name__ == ("__main__"):
	app.run(host = '0.0.0.0', debug=True)
