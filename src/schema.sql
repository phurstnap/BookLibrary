DROP TABLE if EXISTS user;

CREATE TABLE users (
	id integer primary key autoincrement,
	username text not null,
	password text not null,
);