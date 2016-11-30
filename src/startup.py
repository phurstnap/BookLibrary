from flask import Flask, render_template, redirect, url_for, request, json
app = Flask(__name__)

@app.route('/login/', methods=['GET', 'POST'])
def login():
	error = None
	jdata = json.loads(open ('data.json').read())
	for c in jdata['username']
		if request.form['username'] != 'username' or request.form['password'] != c.get('password')
			error = 'Invalid username or password. Please try again.'
		else
			return redirect(url_for('username'))
	
@app.route('username')
def user():
	return render_template('user.html')
	
@app.route('/')
def redirects():
	return redirect('login')
	
@app.route('/')
def redirects():
	return redirect('login')

@app.errorhandler(404)
def handler404(e):
	return render_template('404.html')


if __name__ == ("__main__"):
	app.run(host = '0.0.0.0', debug=True)
