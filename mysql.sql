use sweethome;
create table home ( id int auto_increment, address char(140), address2 char(140), city char(40), state char(40), zipcode char(6), year_built int, zillow_url varchar(2048), home_owner int, date_posted datetime, primary key(id), foreign key(home_owner) references user(id) ON UPDATE CASCADE ON DELETE RESTRICT);
create database mysweethome;
insert into home (address, city, state, zipcode, year_built, zillow_url, home_owner) values ( '41099 Bernie St', 'Fremont', 'CA', '94539',2001, 'www.zillow.com',1);
select * from user;
SELECT home.id AS home_id, home.address AS home_address, home.address2 AS home_address2, home.city AS home_city, home.state AS home_state, home.zipcode AS home_zipcode, home.year_built AS home_year_built, home.zillow_url AS home_zillow_url, home.home_owner AS home_home_owner, home.date_posted AS home_date_posted 
FROM home ORDER BY home.date_posted DESC;
alter table user add column (phone_number char(11));

update  user set user_type = 1 where id >= 1;
create table vendorservices ( id int auto_increment, name char(40), description char(140), vendor_id int,  primary key(id), foreign key(vendor_id) references user(id) ON UPDATE CASCADE ON DELETE RESTRICT);
select * from vendorservices;
SELECT `VendorServices`.id AS `VendorServices_id`, `VendorServices`.name AS `VendorServices_name`, `VendorServices`.description AS `VendorServices_description`, `VendorServices`.vendor_id AS `VendorServices_vendor_id` 
FROM `VendorServices` 
WHERE `VendorServices`.vendor_id = 3

create table user ( id int auto_increment, username char(20), email char(120), image_file char(20), password char(60), primary key (id));
select * from user;
describe home;

describe user;
