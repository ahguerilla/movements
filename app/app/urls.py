from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'app.views.home', name='home'),
    url(r'^messages/', include('postman.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^exchange', 'app.views.exchange', name='exchange'),
    url(r'^settings', 'app.users.views.settings', name='settings'),
    url(r'^home-page-sign', 'app.users.views.accountsignup'),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('app.api.urls')),

    url(r'^add/(?P<obj_type>offer|request|resource)', 'app.market.views.addItem_form',name="form_add_item"),
    url(r'^view/(offer|request|resource|item)/(?P<obj_id>\d+)$','app.market.views.viewItem', name="view_item"),
    url(r'^edit/(?P<obj_id>\d+)$','app.market.views.editItem_form', name="form_edit_item"),

    url(r'^add/comment/(?P<obj_id>\d+)$','app.market.views.addComment_form', name="form_add_comment"),
    url(r'^edit/comment/(?P<obj_id>\d+)$','app.market.views.editComment_form', name="form_edit_comment"),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


