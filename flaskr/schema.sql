drop table if exists entries;
drop table if exists passwords;
drop table if exists lost;
drop table if exists found;

create table lost (
  id integer primary key autoincrement,
  name text not null,
  item text not null,
  description text not null,
  number integer not null,
  email text not null
);


create table found (
  id integer primary key autoincrement,
  name text not null,
  item text not null,
  description text not null,
  number integer not null,
  email text not null
);



