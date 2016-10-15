drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null
);
drop table if exists users;
create table users (
  id integer primary key autoincrement,
  name text not null,
  mail text not null,
  'text' text not null
);
drop table if exists products;
create table products (
  id integer primary key autoincrement,
  catego text not null,
  img_file text not null,
  price integer not null,
  description text not null,
  'text' text not null
);

drop table if exists sales;
create table sales (
  id integer primary key autoincrement,
  products text not null,
  'text' text not null
);
