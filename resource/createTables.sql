create table if not exists entrancePointInfo
(
	id varchar(100) PRIMARY KEY NOT NULL ,
	methods varchar(2000) not null
);

CREATE TABLE  if not exists recommendResult (
  [ID] VARCHAR,
  [methodName] VARCHAR,
  [islike] BOOLEAN,
  [rounds] INT,
  [precision] FLOAT,
  [recall] FLOAT,
  [fmeasure] FLOAT,
  PRIMARY KEY([ID], [methodName]));

CREATE TABLE if not exists goldSets(
  [ID] VARCHAR,
  [origiMethods] VARCHAR,
  [methods] VARCHAR,
  [updatedMethods] VARCHAR);
