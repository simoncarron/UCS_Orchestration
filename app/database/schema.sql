drop table if exists vm;
create table vm (
  pkID integer primary key autoincrement
  ,product text
  ,is_primary text
  ,name text
  ,ip_address text
  ,ip_mask text
  ,ip_gateway_address text
  ,primary_dns text
  ,secondary_dns text
  ,domain text
  ,region text
  ,time_zone text
  ,fkID_ucs integer
  ,fkID_created_by integer
);
drop table if exists ucs;
create table ucs (
  pkID integer primary key autoincrement
  ,name text
  ,os text
  ,ip_address text
  ,ip_mask text
  ,ip_gateway_address text
  ,cimc_ip_address text
  ,cimc_ip_mask text
  ,cicm_ip_gateway_address text
  ,fkID_created_by integer
);
drop table if exists user;
create table user (
  pkID integer primary key autoincrement
  ,name text
  ,first_name text
  ,userid text
  ,password text
  ,access_group text
  ,fkID_pod integer
  ,fkID_created_by integer
);
drop table if exists pod;
create table pod (
  pkID integer primary key autoincrement
  ,name text
  ,management_ip_address text
  ,status text
  ,username text
  ,password text
  ,fkID_created_by integer
);
INSERT INTO user (name,first_name,userid,password,access_group)VALUES ('admin', 'admin', 'admin', 'admin', 'A' );
INSERT INTO user (name,first_name,userid,password,access_group)VALUES ('simon', 'simon', 'simon', 'simon', 'B' );
INSERT INTO user (name,first_name,userid,password,access_group)VALUES ('carron', 'carron', 'carron', 'carron', 'B' );
