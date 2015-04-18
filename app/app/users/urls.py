from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns("",
    url(r'^settings$', views.settings, name='user_settings'),
    url(r'^profile$', views.profile, name='user_profile'),
    url(r'^profile/unsubscribe$', views.one_click_unsubscribe, {'uuid': None}, name='one_click_unsubscribe'),
    url(r'^profile/unsubscribe/(?P<uuid>.+)$', views.one_click_unsubscribe, name='one_click_unsubscribe'),
    url(r'^profile/(?P<user_name>\S+)$', views.profile_for_user, name='user_profile_for_user'),
    url(r'^waitforactivation$', views.waitforactivation, name="waitforactivation"),
    url(r'^thanksforactivation$', views.thanksforactivation, name="thanksforactivation"),
    url(r"^confirm_email/(?P<key>\w+)/$", views.confirm_email, name="users_confirm_email"),
)


