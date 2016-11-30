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
		user = cur.fetchone()
		
		con.commit()
		
		if cur.fetchone() is not None:
			return render_template('user.html',user = user)
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
def user(name = None):
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
	return render_template('user.html' name = name)
	con.close()

@app.route('/bookmark')
def bookmark(name = None):
	if request.method=='POST':
		title = request.form['title']
		author = request.form['author']
		page = request.form['page']
		line = request.form['line']
		
		con = sql.connect("books.db")
		cur = con.cursor()
		cur.execute("INSERT INTO books (title, author, page, line) VALUES (?,?)", (title, author, page, line))
		con.close()
		return render_template('user.html', name = name)
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
