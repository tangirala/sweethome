#
1. Install PyCharm Community Edition
1a. Install Python3.8 https://www.python.org/downloads/
2. Unzip bsemail.zip file.
3. ../settings.zip file is the pycharm settings.zip file.  If you want you can import this.
	a. In Pycharm, File->Manage IDE Settings->import Settings->pick the above settings.zip file.
	b. This will restart the PyCharm nd it should be ok.
3a. install python packages in requirements.txt file.
	On Unix I used pip3.
		Install pip3 from  https://evansdianga.com/install-pip-osx/
		pip3 install -r requirements.txt
	On Windows, you can install.
		https://vgkits.org/blog/pip3-windows-howto/#:~:text=Download%20the%2064%2Dbit%20installer,the%20checkbox%20%E2%80%9CAdd%20Python%203.
		pip3 install -r requirements.txt
4. open the bsemail directory, the one installed.
5. Run the application in PyCharm
6. Go to http://localhost:5000/



Installing MYSQL on a MAC book:
1. Download Mysql from : https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-8.0.21-macos10.15-x86_64.dmg
2. Double click on the .dmg file installed
3. Right click on the pkg file and try with Open with option( because of security it will not open.)
4. Click Open (for the Installer)
5. Go through the installation process
6. enter root password : car4sale


Install Mysql Workbench

Installing MySQL connector.

Issue explained : https://stackoverflow.com/questions/52261686/issues-with-flask-mysqldb-using-python3-7

export DYLD_LIBRARY_PATH=/usr/local/mysql/lib/:$DYLD_LIBRARY_PATH
python3 run.sh


Database steps:
===============
use bsemail;
create table user ( id int auto_increment,
                    username char(20),
                    email char(120),
                    image_file char(20),
                    password char(60),
                    primary key (id));
create table home ( id int auto_increment,
                    address char(140),
                    address2 char(140),
                    city char(40),
                    state char(40),
                    zipcode char(6),
                    year_built int,
                    zillow_url char(2048),
                    home_owner int,
                    date_posted datetime,
                    primary key(id),
                    foreigh key(home_owner) references user(id) ON UPDATE CASCADE ON DELETE RESTRICT);

create table vendorservices (
                    id int auto_increment,
                    name char(40),
                    description char(140),
                    vendor_id int,
                    primary key(id),
                    foreign key(vendor_id) references user(id) ON UPDATE CASCADE ON DELETE RESTRICT);

create table servicespurchased (
                    id int auto_increment,
                    name char(40),
                    purchase_date datetime,
                    purchase_price float,
                    warranty_enddate datetime,
                    vendor_id int,
                    home_id int,
                    service_id int,
                    primary key(id),
                    foreign key(vendor_id) references user(id) ON UPDATE CASCADE ON DELETE RESTRICT,
                    foreign key(home_id) references home(id) ON UPDATE CASCADE ON DELETE RESTRICT,
                    foreign key(service_id) references vendorservices(id) ON UPDATE CASCADE ON DELETE RESTRICT);

create table documents (
                    id int auto_increment,
                    filename char(40) not null,
                    location char(140) not null,
                    creation_date datetime,
                    home_id int,
                    primary key(id),
                    foreign key(home_id) references home(id) ON UPDATE CASCADE ON DELETE RESTRICT);