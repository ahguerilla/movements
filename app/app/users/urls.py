from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns("",
    url(r'^settings$', views.settings, name='user_settings'),
    url(r'^getting-started$', views.initial_settings, name='getting_started'),
    url(r'^profile$', views.profile, name='user_profile'),
    url(r'^profile/(?P<user_name>\S+)$', views.profile_for_user, name='user_profile_for_user'),
    url(r'^waitforactivation$',views.waitforactivation , name="waitforactivation"),
    url(r'^thanksforactivation$',views.thanksforactivation , name="thanksforactivation")
)


