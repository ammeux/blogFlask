DROP TABLE if EXISTS user;
DROP TABLE if EXISTS post;

CREATE TABLE user (
id integer primary key autoincrement,
username TEXT UNIQUE NOT NULL,
email TEXT UNIQUE NOT NULL,
password TEXT NOT NULL
);

CREATE TABLE post (
id integer primary key autoincrement,
user_id INTEGER NOT NULL,
title TEXT NOT NULL,
body TEXT NOT NULL,
created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES user (id)
);