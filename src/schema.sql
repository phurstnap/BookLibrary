DROP TABLE if EXISTS users;

CREATE TABLE users (
	id integer primary key autoincrement,
	username text not null,
	password text not null,
);