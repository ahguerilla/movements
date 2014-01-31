from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'market/api/', include('app.market.api.urls')),
    url(r'^market/$', 'app.market.views.index', name="show_market"),
    url(r'^market/notifications$', 'app.market.views.notifications', name="show_notifications"),    
    url(r'^market/users$', 'app.market.views.users', name="show_users"),
    url(r'^market/add/(?P<obj_type>offer|request|resource)', 'app.market.views.addItem_form', name="form_add_item"),
    url(r'^market/view/(?P<obj_type>offer|request|resource|item)/(?P<obj_id>\d+)$','app.market.views.viewItem', name="view_item"),
    url(r'^market/view/posts', 'app.market.views.posts', name="posts"),
    url(r'^market/edit/(?P<obj_id>\d+)$','app.market.views.editItem_form', name="form_edit_item"),

    url(r'^market/add/comment/(?P<obj_id>\d+)$','app.market.views.addComment_form', name="form_add_comment"),
    url(r'^market/edit/comment/(?P<obj_id>\d+)$','app.market.views.editComment_form', name="form_edit_comment"),
    url(r'^market/search/', include('haystack.urls')),
    url(r'^messages/', include('postman.urls')),
)


from postman.views import WriteView,ReplyView,MessageView,ConversationView
from app.market.forms import MarketWriteForm,MarketFullReplyForm,MarketQuickReplyForm

urlpatterns += patterns('postman.views',
                        #url(r'^write/(?:(?P<recipients>[\w.@+-:]+)/)?$', WriteView.as_view(form_classes=(MarketWriteForm,)), name='postman_write'),
                        #url(r'^reply/(?P<message_id>[\d]+)/$', ReplyView.as_view(form_class=MarketFullReplyForm), name='postman_reply'),
                        url(r'^view/t/(?P<thread_id>[\d]+)/$', ConversationView.as_view(form_class=MarketQuickReplyForm), name='postman_view_conversation'),
                        url(r'^view/(?P<message_id>[\d]+)/$', MessageView.as_view(form_class=MarketQuickReplyForm), name='postman_view'),
)