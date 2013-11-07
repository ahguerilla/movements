
# ahr

## setup

- git git@bitbucket.org:guerillasoftware/ahr.git
- create virtualenv

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

## Widget Tweaks Reference
https://pypi.python.org/pypi/django-widget-tweaks