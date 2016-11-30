import sqlite3 as sql

def insertUser(username,password):
	con = sql.connect("users.db")
	cur = con.cursor()
	cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
	con.commit()
	con.close()

def retrieveUsers():
	con = sql.connect("users.db")
	cur = con.cursor()
	cur.execute('SELECT * from users WHERE username="%s" AND password="%s"' % (user, password)
	user = cur.fetchone()
	con.close()
	return user