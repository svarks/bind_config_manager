Bind Config Manager
===================

This tool is for managing bind9 DNS server domains and records.
Demo version available here: <http://sav86.selfip.com:5000/>

Before Install
--------------

It will write zone definitions into /etc/named.conf.zones by default.
And you have to include this file into your named.conf.

To make it just add this line at the end of file:

    include "/etc/named.conf.zones";

And remove/comment all zone definitions except root if you want to
manage all zones through this app (it will only read /etc/named.conf.zones file).
All zone files containing information about records will be stored into /var/named/zones.

!!! WARNING !!! You will probably need to run all commands as root.
This is because application will need access to some places like
/var/named/ and /etc/rndc.key (which is not readable by default)

You can edit these locations in development.ini config file.
Default values:
    named.zones_config = /etc/named.conf.zones
    named.zones_dir = /var/named/zones
    named.rndc_bin = rndc
    named.checkconf_bin = named-checkconf
    named.checkzone_bin = named-checkzone
    named.dig_bin = dig
    named.server_addr = 127.0.0.1


Installation
------------

Download source from github repo:

    git clone git://github.com/sav86/bind_config_manager.git

    cd bind_config_manager

From application directory run:

    python bootstrap.py
    
and then
    
    ./bin/buildout
    
It will download all required python packages.

After that you can initialize database with this line:

    ./bin/paster setup-app development.ini

And then start server:

    ./bin/paster serve development.ini

How to use
----------

To access web version just go to <http://localhost:5000/>
You can login using admin/admin credentials.

Command-line is available from application directory by running
    ./bin/bcm

You can make symlink for it to use anywhere
    ln -s <your_application_directory>/bin/bcm /usr/local/bcm

To check available domains run:
    $ bcm domain_list
    master	example.com	
    master	0.0.127.in-addr.arpa

And this will display all records for given domain:
    $ bcm domain_show example.com

    Domain Information:
    -------------------
    master	example.com	ns1.example.com.	hostmaster.example.com.	1279827781	28800	14400	3600000	86400	86400	

    Domain Records:
    ---------------
    1	NS	86400		@	ns1.example.com.	
    2	NS	86400		@	ns2.example.com.	
    3	MX	86400	10	@	mail.example.com.	
    4	MX	86400	20	@	mail2.example.com.	
    5	A	86400		@	192.168.10.10	
    6	A	86400		ns1	192.168.1.10	
    7	A	86400		ns2	192.168.1.20	
    8	A	86400		mail	192.168.2.10	
    9	A	86400		mail2	192.168.2.20	
    10	A	86400		www2	192.168.10.20	
    11	CNAME	86400		www	@	
    12	CNAME	86400		ftp	@	
    13	CNAME	86400		webmail	@	
