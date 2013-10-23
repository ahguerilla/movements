default: runlocal

syncdb:
	cd app && python manage.py syncdb --settings=app.settings.local

m:
	cd app && python manage.py migrate --settings=app.settings.local
ms:
	cd app && python manage.py migrate --settings=app.settings.staging

collectstatic:
	cd app && python manage.py collectstatic --settings=app.settings.staging

sm:
	cd app && python manage.py schemamigration $(app) --auto --settings=app.settings.local

smi:
	cd app && python manage.py schemamigration $(app) --initial --settings=app.settings.local

mf:
	cd app && python manage.py migrate $(app) --fake $(ver) --settings=app.settings.local

mfs:
	cd app && python manage.py migrate $(app) --fake $(ver) --settings=app.settings.staging

loaddata:
	cd app && python manage.py loaddata $(fixture) --settings=app.settings.local

runlocal:
	cd app && python manage.py runserver --settings=app.settings.local

runlocalext:
	cd app && python manage.py runserver 0.0.0.0:8000 --settings=app.settings.local

shelllocal:
	cd app && python manage.py shell --settings=app.settings.local

runprod:
	cd app && python manage.py runserver --settings=app.settings.production

runprodext:
	cd app && python manage.py runserver 0.0.0.0:8000 --settings=app.settings.production

clean:
	rm -rf app/static/.webassets-cache/
