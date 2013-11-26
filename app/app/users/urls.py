from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns("",
    url(r'^settings', views.settings, name='user_settings'),
)