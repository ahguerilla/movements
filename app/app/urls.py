from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'app.views.home', name='home'),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^exchange', 'app.views.exchange', name='exchange'),
    url(r'^settings', 'app.users.views.settings', name='settings'),
    url(r'^home-page-sign', 'app.users.views.accountsignup'),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('app.api.urls')),

    url(r'^add/offer', 'app.market.views.addOffer_form',name="form_add_offer"),
    url(r'^view/offer/(?P<obj_id>\d+)$','app.market.views.viewOffer', name="view_offer"),
    url(r'^edit/offer/(?P<obj_id>\d+)$','app.market.views.editOffer_form', name="form_edit_offer"),

    url(r'^add/comment/(?P<obj_id>\d+)$','app.market.views.addComment_form', name="form_add_comment"),
    url(r'^edit/comment/(?P<obj_id>\d+)$','app.market.views.editComment_form', name="form_edit_comment"),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


