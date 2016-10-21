USE group120db;

DROP TABLE IF EXISTS Contain, Photo, Album, User, AlbumAccess;

CREATE TABLE User(
username varchar(20),
firstname varchar(20), 
lastname varchar(20), 
password varchar(256), 
email varchar(40), 
PRIMARY KEY (username));

CREATE TABLE Album(
albumid int AUTO_INCREMENT,
title varchar(50),
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
lastupdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
username varchar(20),
access ENUM('public', 'private'),
PRIMARY KEY (albumid),
FOREIGN KEY(username) REFERENCES User(username));

CREATE TABLE Photo(
picid varchar(40),
format nvarchar(3),
picDate TIMESTAMP,
PRIMARY KEY(picid));

CREATE TABLE Contain(
sequencenum int, 
albumid int,
picid varchar(40),
caption varchar(255),
PRIMARY KEY (sequencenum),
FOREIGN KEY(albumid) REFERENCES Album(albumid),
FOREIGN KEY(picid) REFERENCES Photo(picid));

CREATE TABLE AlbumAccess(
albumid int,
username varchar(20),
PRIMARY KEY (albumid, username));













