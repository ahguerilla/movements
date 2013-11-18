from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
    url(r'api/', include('market.api.urls')),
    url(r'', 'app.market.views.index',name="show_market"),
    url(r'add/(?P<obj_type>offer|request|resource)', 'app.market.views.addItem_form',name="form_add_item"),
    url(r'view/(?P<obj_type>offer|request|resource|item)/(?P<obj_id>\d+)$','app.market.views.viewItem', name="view_item"),
    url(r'edit/(?P<obj_id>\d+)$','app.market.views.editItem_form', name="form_edit_item"),

    url(r'add/comment/(?P<obj_id>\d+)$','app.market.views.addComment_form', name="form_add_comment"),
    url(r'edit/comment/(?P<obj_id>\d+)$','app.market.views.editComment_form', name="form_edit_comment"),

)


