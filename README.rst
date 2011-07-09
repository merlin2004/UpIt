======================
 UpIt - Up your files
======================

:Keywords: python, jquery, django, web, html5, audio, javascript, upit, fileupload, imageupload

UpIt is a simple image and fileupload. This project is a sideproject,
don't expect any support or constant developement.

Deps
====
Django 1.3 (not included in Debian Squeeze(stable))

Python Sqlite

PIL (python-imaging-library)

Apache mod_xsendfile

Apache mod_wsgi

Arch Linux:

    # pacman -S extra/django extra/apache core/sqlite3 extra/python-pysqlite extra/python-imaging extra/mod_wsgi

    $ yaourt -S aur/mod_xsendfile

Debian:
    
    # apt-get install libapache2-mod-xsendfile apache2 python-django python-pysqlite2 sqlite3 python-imaging libapache2-mod-wsgi

Arch Linux requires you to activate the xsendfile and wsgi module by hand.
In order to do this, just uncomment the two LoadModule commands in the upit_apache.conf
    
Installing UpIt
===============

Hints: $ means normal bash, # means root bash

Clone into the repository

    $ git clone git://github.com/Raydiation/UpIt.git

Then change into the newly cloned directory:
    
    $ cd UpIt

Move the upit_apache.conf into your Apache config folder. In Ubuntu it 
would be:

    $ sudo mv upit_apache.conf /etc/apache2/conf.d/

Arch Linux uses:

    # mv upit_apache.conf /etc/httpd/conf/extra/
    
Depending on your Distribution you will have to include the config file
manually in your httpd.conf like in Arch Linux:

    # echo "Include conf/extra/upit_apache.conf" >> /etc/httpd/conf/httpd.conf

Now create the needed directories:

    $ sudo mkdir -p /var/lib/upit/uploads
    
    $ sudo mkdir /usr/share/upit
    
Move the UpIt code to the install directory:

    $ sudo mv upit/ /usr/share/upit

Create the database and adjust the rights:

    $ sudo python2 /usr/share/upit/upit/manage.py syncdb # create a superuser if asked!
    
    $ sudo chown -R www-data:www-data /var/lib/upit # on Arch Linux use http:http instead of www-data:www-data
    
    $ sudo chmod -R 0755 /var/lib/upit/
    
    $ sudo chown -R root:root /usr/share/upit
    
    $ sudo chmod -R 0775 /usr/share/upit
    
Finally restart your Apache Server to read in the new configuration

    $ sudo /etc/init.d/apache2 restart
    
On Arch Linux this would be

    # /etc/rc.d/httpd restart

UpIt is now running on 

    http://127.0.0.1/upit


Alter URL Path
==============
If you want to alter the URL under which upit runs you have to make two
changes. Here for instance we want to let it run on / instead of /upit

upit/settings.py 
----------------
ROOT_URL = '' # default is /upit, dont use a trailing slash!

upit_apache.conf
----------------
Alias /static/ /usr/share/upit/upit/static/


Changing upload files directory
===============================
To change the path where files are uploaded to, first create the folder
and chown it to the apache user and group like:

    $ sudo chown -R www-data:www-data /path/to/folder

Then set the proper rights

    $ sudo chmod -R 0755 /path/to/folder
    
Next, change the MEDIA_ROOT in your settings.py (dont forget trailing slash!)

    MEDIA_ROOT = '/path/to/folder/' # standard is '/var/lib/upit/uploads/'
                                    
At last, change the upit_apache.conf

From:
    XSendFilePath /var/lib/upit/uploads
To:
    XSendFilePath /path/to/folder

Developement Info
=================
Change static files only in upload/static and then sync them with 

    $ python2 manage.py collectstatic

to the static directory



License
=======

This software is licensed under the ``GPLv3``. 
