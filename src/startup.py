from flask import Flask, render_template, redirect, url_for, request
from logging.handlers import RotatingFileHandler
import sqlite3 as sql
import ConfigParser
import logging
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
						<img src="{{ url_for('static', filename='img/{{title}}.png') }}">
					</form>
				</div>
		'''
	return render_template('user.html', username = username, content = code)
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
			
			f = request.files['datafile']
			f.save('static/uploads/' + title + '.png')
			
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
	
@app.route('/config/')
def config():
	str = []
	str.append('Debug: ' + app.config['DEBUG'])
	str.append('Port: ' + app.config['port'])
	str.append('Url: ' + app.config['url'])
	str.append('IP_address: ' + app.config['ip_address'])
	return '\t'.join(str)

def init(app):
	config = ConfigParser.ConfigParser()
	try:
		config_location = "etc/defaults.cfg"
		config.read(config_location)
		
		app.config['DEBUG'] = config.get("config", "debug")
		app.config['ip_address'] = config.get("config", "ip_address")
		app.config['port'] = config.get("config", "port")
		app.config['url'] = config.get("config", "url")
		
		app.config['log_file'] = config.get("logging", "name")
		app.config['log_location'] = config.get("logging", "location")
		app.config['log_level'] = config.get("logging", "level")

	except:
		print "Could not read from configs at: " + config_location

def logs(app):
	log_pathname = app.config['log_location'] + app.config ['log_file']
	file_handler = RotatingFileHandler(log_pathname, maxBytes=1024 * 1024 * 10, backupCount= 1024)
	file_handler.setlevel(app.config['log_level'])
	formatter = logging.Formatter("%(levelname)s | %(asctime)s | %(module)s | %(funcName)s | %(message)s")
	file_handler.setFormatter(formatter)
	app.logger.setLevel(app.config['log_level'])
	app.logger.addHandler(file_handler)

if __name__ == ("__main__"):
	init(app)
	logs(app)
	app.run(
		host=app.config['ip_address'],
		port=int(app.config['port']))
