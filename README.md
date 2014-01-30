Piclodio2
=========

Raspberry Pi Web Clock Radio.
![alt tag](https://raw.github.com/Sispheor/Piclodio2/master/img/piclodio_home.png)

Installation
==========

Install Django Framework
```
wget https://www.djangoproject.com/download/1.6/tarball/
tar xzf Django-1.6.tar.gz
sudo python setup.py install
```

Install the web radio player, At, the SQLite database, the web server and python module
```
sudo apt-get install mplayer at sqlite3 apache2 libapache2-mod-wsgi
```

Install Crontab module
```
wget https://pypi.python.org/packages/source/p/python-crontab/python-crontab-1.7.0.tar.gz
tar xzf python-crontab-1.7.0.tar.gz
cd python-crontab-1.7.0/
sudo python setup.py install
```

Install Piclodio application from github into apache document root directory
```
cd /var/www
git clone https://github.com/Sispheor/Piclodio2.git
```

Copy vHost from sources folder into apache vHost configuration folder
```
cp /var/www/Piclodio2/apache.piclodio.conf /etc/apache2/sites-available/
```

Enable the vHost
```
a2ensite piclodio
```
And last, we have to allow the Apache user www-data to use mplayer. Edit the sudoers file with the command
```
sudo visudo
```
and add this line at the end of the file
```
www-data ALL=NOPASSWD:/usr/bin/mplayer* ,/usr/bin/pgrep mplayer ,/usr/bin/killall mplayer, /usr/bin/at
```

That's it! Piclodio is now available on it IP adresse.
