from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

js_info_dict = {
    'packages': ('app',),
}
urlpatterns = patterns('',
    url(r'^$', 'app.views.home', name='home'),
    url(r'^movements/', include('cms.urls')),
    url(r'^terms-and-conditions$', 'app.views.terms_and_conditions', name='terms_and_conditions'),
    url(r'^contact-us$', 'app.views.contact_us', name='contact_us'),
    url(r'^privacy$', 'app.views.privacy', name='privacy'),
    url(r'^how-it-works$', 'app.views.how_it_works_pub', name='how_it_works_pub'),
    url(r'^cl-how-it-works$', 'app.views.how_it_works_priv', name='how_it_works_priv'),
    url(r'^sign-up$', 'app.users.views.signup_from_home', name="sign_up"),
    url(r'^sign-up/process', 'app.users.views.process_signup', name="process_signup"),
    url(r'^', include('app.market.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^user/', include('app.users.urls')),
    url(r'^exchange', 'app.views.exchange', name='exchange'),
    url(r'^avatar/render_primary/(?P<user>[\w\@\d\.\-_]{1,30})/(?P<size>[\d]+)/$', 'avatar.views.render_primary', name='avatar_render_primary'),
    url(r'^avatar/', include('avatar.urls')),
    # Account View Overrides
    url(r'^accounts/social/signup/+$', 'app.users.views.ahr_social_signup', name="social_sign_up"),
    url(r'^accounts/password/reset/+$', 'app.users.views.password_reset', name="password_reset"),
    url(r"^accounts/password/change/$", 'app.users.views.password_change', name="account_change_password"),
    url(r"^accounts/password/change_done$", 'app.users.views.password_change_done', name="account_change_password_success"),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/auth/user/(?P<user_id>\d+)/vet$', 'app.users.views.vet_user', name='vet_user'),
    url(r'^admin/auth/user/(?P<user_id>\d+)/emailvetted$', 'app.users.views.email_vet_user', name='email_vet_user'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rosetta/', include('rosetta.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
