from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'app.views.home', name='home'),
    url(r'^market/', include('app.market.urls')),
    url(r'^messages/', include('postman.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^user/', include('app.users.urls')),
    url(r'^exchange', 'app.views.exchange', name='exchange'),
    url(r'^home-page-sign', 'app.users.views.accountsignup'),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^admin/', include(admin.site.urls)),    

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


