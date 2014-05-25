from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'market/api/', include('app.market.api.urls')),
    url(r'^market/$', 'app.market.views.index', name="show_market"),
    url(r'^market/notifications$', 'app.market.views.notifications', name="show_notifications"),
    url(r'^market/users$', 'app.market.views.users', name="show_users"),
    url(r'^market/view/posts', 'app.market.views.posts', name="posts"),
    url(r'^market/preview/(?P<obj_type>\w+)/(?P<obj_id>\w+)/', 'app.market.views.preview', name='preview'),

    url(r'^market/search/', include('haystack.urls')),
    url('^/messages/inbox/m/$','app.market.views.index'),
    url('^messages/permdelete/', 'app.market.views.permanent_delete_postman', name="permanent_delete_postman"),
    url('^messages/unarchive/', 'app.market.views.postman_unarchive', name="postman_unarchive"),
    url(r'^messages/', include('postman.urls')),
)

from cust_postman import MarketQuickReplyForm, MyConv, MessageView

urlpatterns += patterns('postman.views',
                        #url(r'^write/(?:(?P<recipients>[\w.@+-:]+)/)?$', WriteView.as_view(form_classes=(MarketWriteForm,)), name='postman_write'),
                        #url(r'^reply/(?P<message_id>[\d]+)/$', ReplyView.as_view(form_class=MarketFullReplyForm), name='postman_reply'),
                        url(r'^view/t/(?P<thread_id>[\d]+)/$', MyConv.as_view(form_class=MarketQuickReplyForm), name='postman_view_conversation'),
                        url(r'^view/(?P<message_id>[\d]+)/$', MessageView.as_view(form_class=MarketQuickReplyForm), name='postman_view'),
)
