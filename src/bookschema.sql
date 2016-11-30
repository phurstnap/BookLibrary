drop table if exists books;
	create table books (
	id integer primary key autoincrement,
	username text not null,
	title text not null,
	author text not null,
	username int not null,
	password int not null
);