from flask import Flask, render_template, redirect, url_for, request
import sqlite3 as sql
app = Flask(__name__)

@app.route('/login/', methods=['GET', 'POST'])
def login():
	if request.method=='POST':
		username = request.form['username']
		password = request.form['password']
		
		con = sql.connect("users.db")
		cur = con.cursor()
		cur.execute('SELECT username from users WHERE username="%s" AND password="%s"' % (username, password))
		username = cur.fetchone()
		
		con.commit()
		
		if cur.fetchone() is not None:
			return render_template('user.html',username = username)
		else:
			return render_template('login.html')
		con.close()
	else:
		return render_template('login.html')


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
def user(username = None):
	con = sql.connect("books.db")
	cur = con.cursor()
	for book in books:
		cur.execute('SELECT title from books WHERE username="%s"' % (username))
		title = cur.fetchone()
		cur.execute('SELECT author from books WHERE username="%s"' % (username))
		author = cur.fetchone()
		cur.execute('SELECT page from books WHERE username="%s"' % (username))
		page = cur.fetchone()
		cur.execute('SELECT line from books WHERE username="%s"' % (username))
		line = cur.fetchone()
		code = code + '''
				<div class="col-md-4">
					<form>
						Title: {{title}}</br>
						Author: {{author}}</br>
						Page: {{page}}</br>
						Line: {{line}}</br>
					</form>
				</div>
		'''
	return render_template('user.html', username = username)
	con.close()

@app.route('/bookmark', methods=['GET', 'POST'])
def bookmark(username = None):
	if request.method=='POST':
		username = request.form['username']
		password = request.form['password']
		
		con = sql.connect("users.db")
		cur = con.cursor()
		cur.execute('SELECT username from users WHERE username="%s" AND password="%s"' % (username, password))
		user = cur.fetchone()
		con.commit()
		
		if cur.fetchone() is not None:
			title = request.form['title']
			author = request.form['author']
			page = request.form['page']
			line = request.form['line']
			
			conb = sql.connect("books.db")
			curb = conb.cursor()
			curb.execute("INSERT INTO books (username, title, author, page, line) VALUES (?,?,?,?,?)", (username, title, author, page, line))
			conb.close()
			return render_template('user.html', username = user)
		else:
			return render_template('bookmark.html')
		con.close()
		
	else:
		return render_template('bookmark.html')
	
@app.route('/')
def redirects():
	return redirect('login')
	
@app.errorhandler(404)
def handler404(e):
	return render_template('404.html')


if __name__ == ("__main__"):
	app.run(host = '0.0.0.0', debug=True)
