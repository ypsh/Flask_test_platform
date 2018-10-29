--drop table if exists User;
CREATE TABLE USER (
  id integer PRIMARY KEY autoincrement,
  USER STRING UNIQUE,
  password STRING NOT NULL,
  ROLE STRING NOT NULL,
  email STRING ,
  mobile STRING ,
  image STRING ,
  is_active STRING default 1,
  creater STRING，
  updater STRING，
  create_time TIMESTAMP  default (DATETIME('now','localtime'))
);
--drop table if exists Service;
CREATE TABLE Service (
  id integer PRIMARY KEY autoincrement,
  service_name STRING UNIQUE,
  path STRING NOT NULL,
  TYPE STRING NOT NULL,
  DATA text ,
  STATUS STRING ,
  creater STRING ,
  updater STRING ,
  create_time TIMESTAMP NOT NULL default (DATETIME('now','localtime'))
);
--drop table if exists api_manger;
CREATE TABLE api_manager (
  id integer PRIMARY KEY autoincrement,
  api_name STRING UNIQUE NOT NULL,
  model STRING,
  TYPE STRING NOT NULL,
  path STRING NOT NULL,
  headers STRING ,
  need_token STRING ,
  STATUS STRING ,
  mark text,
  creater STRING ,
  updater STRING ,
  create_time TIMESTAMP default (DATETIME('now','localtime')),
  update_time TIMESTAMP
);
--drop table if exists test_case;
CREATE TABLE test_case (
  id integer PRIMARY KEY autoincrement,
  case_name STRING NOT NULL,
  api_id integer NOT NULL,
  parameter text ,
  RESULT text ,
  validation_type STRING NOT NULL,
  mark text ,
  creater STRING ,
  updater STRING ,
  executer STRING ,
  execute_time TIMESTAMP ,
  create_time TIMESTAMP default (DATETIME('now','localtime')),
  update_time TIMESTAMP,
  last_result STRING

);
--drop table if exists test_report;
CREATE TABLE test_report (
  id integer PRIMARY KEY autoincrement,
  batch_number STRING ,
  execute_type STRING,
  case_id integer NOT NULL,
  start_time TIMESTAMP ,
  end_time TIMESTAMP ,
  input STRING ,
  api_name STRING ,
  model STRING ,
  case_name STRING ,
  response_headers STRING,
  response_path STRING ,
  response_result text ,
  expect_result text ,
  response_status STRING ,
  use_time integer ,
  creater STRING ,
  validation_result STRING ,
  validation_type STRING ,
  create_time TIMESTAMP default (DATETIME('now','localtime'))
);
--DROP TABLE IF EXISTS task_schedul;
CREATE TABLE task_schedul(
  id integer PRIMARY KEY autoincrement,
  schedul_name STRING,
  model STRING,
  TRIGGER STRING,
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  frequency integer，
     unit STRING,
  creater STRING,
  create_time TIMESTAMP default(DATETIME('now', 'localtime'))
);

CREATE TABLE files_manger (
  id integer PRIMARY KEY autoincrement,
  file_name STRING,
  file_type STRING,
  file_size STRING,
  creater STRING,
  remark STRING ,
  create_time TIMESTAMP default(DATETIME('now', 'localtime')) ,
);