from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'app.views.home', name='home'),
    url(r'^exchange', 'app.views.exchange', name='exchange'),
    #url(r'^register$', 'app.users.views.register', name='register'),
    #url(r'^login$', 'app.users.views.login', name='login'),
    #url(r'^dashboard$', 'app.users.views.dashboard', name='dashboard'),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('app.api.urls')),
    url(r'^create/offer/', 'app.market.views.index',name="create_offer"),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


