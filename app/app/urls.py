from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'app.views.home', name='home'),
    url(r'^terms-and-conditions$', 'app.views.terms_and_conditions', name='terms_and_conditions'),
    url(r'^contact-us$', 'app.views.contact_us', name='contact_us'),
    url(r'^sign-up$', 'app.users.views.signup_from_home', name="sign_up"),
    url(r'^sign-up/process', 'app.users.views.process_signup', name="process_signup"),
    url(r'^', include('app.market.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^user/', include('app.users.urls')),
    url(r'^exchange', 'app.views.exchange', name='exchange'),
    url(r'^avatar/', include('avatar.urls')),
    # Account View Overrides
    url(r'^accounts/social/signup/+$', 'app.users.views.ahr_social_signup', name="social_sign_up"),
    url(r'^accounts/password/reset/+$', 'app.users.views.password_reset', name="password_reset"),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
