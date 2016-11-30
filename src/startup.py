from flask import Flask, render_template, redirect, url_for, request
import sqlite3 as sql
app = Flask(__name__)

@app.route('/login/', methods=['GET', 'POST'])
def login():
	session = None
	try:
		if(session['name']):
			return render_template('user.html', user = name)
		else:
			if request.method=='POST':
				username = request.form['username']
				password = request.form['password']
				
				con = sql.connect("users.db")
				cur = con.cursor()
				cur.execute('SELECT * from users WHERE username="%s" AND password="%s"' % (username, password))
				user = cur.fetchone()
				
				con.commit()
				con.close()
				if c.fetchone() is not None:
					session['name'] = user
					return render_template('user.html', id=None, user = user, password=None)
				else:
					return render_template('login.html')
			else:
				return render_template('login.html')
	except KeyError:
		pass

@app.route('/register/', methods=['GET', 'POST'])
def register():
	if request.method=='POST':
		username = request.form['username']
		password = request.form['password']
		
		con = sql.connect("users.db")
		cur = con.cursor()
		cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
		con.close()
		return render_template('login.html')
	else:
		return render_template('register.html')
		
@app.route('/user')
def user(name = None):
	return render_template('user.html')

@app.route('/')
def redirects():
	return redirect('login')
	
@app.errorhandler(404)
def handler404(e):
	return render_template('404.html')


if __name__ == ("__main__"):
	app.run(host = '0.0.0.0', debug=True)
