# ahr
## setup

- git git@bitbucket.org:guerillasoftware/ahr.git
- create virtualenv

if you are installing on a 64 bit Ubuntu: 

sudo apt-get install libjpeg-dev libpng12-dev libfreetype6-dev libxml2-dev libxslt1-dev solr-common apache2 nodejs npm postgresql-server-dev-all 

    sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
    sudo ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib
    sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib	
    sudo ln -s /usr/bin/nodejs /usr/bin/node
    sudo npm install stylus -g


pip install -r app/requirements/local.txt

 or 

pip install -r app/requirements/production.txt

django-admin.py runserver --settings=app.settings.local

 or 

django-admin.py runserver --settings=app.settings.production

## Adapting default lists - fixtures:

app.fixtures

FIXTURE_DIR set in base settings

## To load data into db:

 - python manage.py loaddata $(fixture) --settings=app.settings.local

Fixture file names should be unique otherwise django will not know what to run.
Fixture models are built based on the db models.
Run manage.py dumpdata $(app) for a textual view of the db model.

## Example:

To load nationalities list into database run

 - python manage.py loaddata users_nationalityfixtures --settings=app.settings.local


## Configure Social SignIn
Configure site object for domain by going to admin>Sites>Sites. In development should be localhost:8000

To configure social app, goto admin>social account>socialapps and create entries for Facebook, Google and Twitter

Client ID and Secret can be found in settings>local.py

On dev mode you can just use `make dev-social`

## Widget Tweaks Reference
https://pypi.python.org/pypi/django-widget-tweaks



## Configure search

If you are using Ubuntu you can install apache2 , tomcat6 and solr-common with apt-get and start apache service.
If solr is installed correctly http://localhost:8080/solr/ should show the solr welcome page.
Do a "pip install -r requirements/base.txt" too.
Make a backup of /etc/solr/conf/schema.xml and copy ahr/app/schema.xml over it.
You may need to copy ahr/app/stopwords_en.txt /etc/solr/conf/stopwords_en.txt 


