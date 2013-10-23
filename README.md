
# ahr

## setup

- git clone blah/app
- virtualenv env-foo
- . env-foo/bin/activate

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

 - python manage.py loaddate users_nationalityfixtures --settings=app.settings.local


