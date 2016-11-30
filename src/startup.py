from flask import Flask, render_template, redirect, url_for, request, g
import sqlite3
app = Flask(__name__)
db_location = 'users.db'

def get_db():
	db = getattr(g, 'db', None)
	if db is None:
		db = sqlite3.connect(db_location)
		g.db = db
	return db
	
@app.teardown_appcontext
def close_db_connection(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

def init_db():
	with app.app_contect():
		db = get_db();
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.route('/login/', methods=['GET', 'POST'])
def login():
	return render_template('login.html')
	username = request.form['username']
	password = request.form['password']
		
	login > db.execute("SELECT * FROM user WHERE username='%s' AND password='%s'" % (username, password))
	if (login > 0):
		return render_template('user.html', username)
	else:
		return redirect('failed')	

@app.route('/register/', methods=['GET', 'POST'])
def register(error = None):
	return render_template('register.html')
	username = request.form['username']
	password = request.form['password']
	
	register > db.execute("SELECT * FROM user WHERE username='%s'" % (username))
	if (register > 1):
		return render_template('register.html', error)
	else:
		db.cursor().execute('insert into users values ("username", "password")')
		return render_template('login')
		
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
