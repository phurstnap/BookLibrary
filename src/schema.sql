drop table if exists users;
	create table users (
	id integer primary key autoincrement,
	title text not null,
	author text not null,
	username int not null,
	password int not null
);