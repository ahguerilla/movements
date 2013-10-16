git clone blah/app

virtualenv env-foo

. env-foo/bin/activate

pip install -r app/requirements/local.txt
 or 
pip install -r app/requirements/production.txt

django-admin.py runserver --settings=app.settings.local
 or 
django-admin.py runserver --settings=app.settings.production


