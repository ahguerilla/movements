from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('',
    url(r'issues/(?P<rtype>\S+)','app.api.views.issues', name="issues"),
    url(r'countries/(?P<rtype>\S+)','app.api.views.countries', name="countries"),
    url(r'nationalities/(?P<rtype>\S+)','app.api.views.nationalities', name="nationalities"),
    url(r'skills/(?P<rtype>\S+)','app.api.views.skills', name="skills"),
    url(r'new/offer','app.api.views.newoffer', name="newoffer")

)
