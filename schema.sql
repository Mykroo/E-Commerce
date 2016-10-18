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
  lastname text not null,
  mail text not null,
  street text,
  num text,
  edo text,
  municipio text,
  cp integer
);
drop table if exists products;
create table products (
  id integer primary key autoincrement,
  name text not null,
  catego text not null,
  img_file text not null,
  price integer not null,
  description text not null,
  quantity integer default 100
);

drop table if exists sales;
create table sales (
  id integer primary key autoincrement,
  products text not null,
  'text' text not null
);
CREATE TABLE if not exists sales (
CREATE TABLE sales (
    id      INTEGER NOT NULL,
    id_usr  INTEGER NOT NULL,
    id_prod INTEGER NOT NULL,
    qty     INTEGER,
    price   INTEGER,
    total   INTEGER,
    PRIMARY KEY (
        id,
        id_usr,
        id_prod
    )
);
