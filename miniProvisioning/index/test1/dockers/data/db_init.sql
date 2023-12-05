create database cloud_op_manager;

use cloud_op_manager;

create table userInfo ( uid int, uname varchar(20), pass varchar(128), profile varchar(200), priority int );

insert into userInfo (uid, uname, pass, profile, priority)values(0, "admin", password("1234"), "관리자", 0);

insert into userInfo (uid, uname, pass, profile, priority)values(1, "user1", password("user1"), "user-1", 1);

insert into userInfo (uid, uname, pass, profile, priority)values(2, "user2", password("user2"), "user-2", 1);

insert into userInfo (uid, uname, pass, profile, priority)values(3, "user3", password("user3"), "user-3", 1);
