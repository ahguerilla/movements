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

 to restart tomcat
 sudo service tomcat6 restart

 to rebuild index
 python manage.py rebuild_index --setting=app.settings.local


##Config notifications
 pip install celery (already in the requirements)
 sudo apt-get install rabbitmq-server
 celery -A celerytasks worker

## Running test cases
 You need to let the database user create a new database for testing
 The user is the same as the user which is defined in django settings
 For local development testing do the following

 sudo -u postgres psql
 su postgres

 psql database -c "GRANT ALL ON ALL TABLES IN SCHEMA public to user;"
 ALTER USER ahr CREATEDB;
 quit
 \q

 #How to generate test data from the database
 Test data is already created but in case anyone needs to use different data that is how you do it:
  ./manage.py dumpdata --natural --indent=4 -e sessions -e admin -e contenttypes -e auth.Permission > test_data.json --setting=app.settings.local
  ./manage.py test market --liveserver=localhost:8082,8090-8100,9000-9200,7041 --setting=app.settings.local

After you created test_data.json you need to copy it over the same file in fixutures directories that it is present

##Translation

After you applied south migration 0018 on user app run the below command to copy the existing values to the english column:
./manage.py  update_translation_fields --setting=app.settings.foo

Substitude -l no with -l <your language code>
###Creating po files for javascripts
./manage.py makemessages -d djangojs -e js -l nn --setting=app.settings.local
###Creating po files for templates and django apps
manage.py makemessages -l nn --setting=app.settings.local


#Staging release proccess

1- ssh ahr@162.243.119.212 and do a git pull in  /opt/ahr/ahr

2- ssh root@162.243.119.212 and restart apache (ahr is not a sudoer)

#Gotchas
No stylus is setup on staging server (digital ocean). So you need to set:
 ASSETS_DEBUG = False
In your local settings on you dev mahine and restart django and visit the market so the packed.css file gets created. After that you need
to overwrite the /opt/ahr/ahr/app/static/css/packed.css with your local file.

In order to use Stylus @import and global variables I upgraded webassets to 0.9. But its ignorant of any changes in the imported
files. You need to increase the dummy counter in site.styl file every time you change something on one of the other stylus files :(
(Untill you find a way to tell the webassets to watch the other styl files.
It might be possible with the extra argument parameter in the settings file that I commented out)
