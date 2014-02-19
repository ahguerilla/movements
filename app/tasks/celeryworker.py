from __future__ import absolute_import
import os
import sys
sys.path.append(os.path.join(os.path.expanduser('~'),'.virtualenvs/mani.ahr/lib/python2.7/site-packages'))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../','../','../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../','../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../','../','app')))

from celery import Celery
from threading import Thread
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings.local')
_app = Celery('celerytasks',broker='amqp://guest@localhost//')
_app.config_from_object('django.conf:settings')
_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from tasks.celerytasks import *