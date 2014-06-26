from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'market/api/', include('app.market.api.urls')),
    url(r'^market/$', 'app.market.views.index', name="show_market"),
    url(r'^market/(?P<post_id>\d+)$', 'app.market.views.show_post', name="show_post"),
    url(r'^market/offer$', 'app.market.views.create_offer', name="create_offer"),
    url(r'^market/request$', 'app.market.views.create_request', name="create_request"),
    url(r'^market/offer/(?P<post_id>\d+)$', 'app.market.views.edit_offer', name="edit_offer"),
    url(r'^market/request/(?P<post_id>\d+)$', 'app.market.views.edit_request', name="edit_request"),
    url(r'^market/notifications$', 'app.market.views.notifications', name="show_notifications"),
    url(r'^market/users$', 'app.market.views.users', name="show_users"),
    url(r'^market/view/posts', 'app.market.views.posts', name="posts"),
    url(r'^market/preview/(?P<obj_type>\w+)/(?P<obj_id>\w+)/', 'app.market.views.preview', name='preview'),
    url(r'^market/search/', include('haystack.urls')),
    url('^/messages/inbox/m/$','app.market.views.index'),
    url('^messages/permdelete/', 'app.market.views.permanent_delete_postman', name="permanent_delete_postman"),
    url(r'^messages/', include('postman.urls')),
)

from cust_postman import MarketQuickReplyForm, MyConv, MessageView

urlpatterns += patterns('postman.views',
                        url(r'^view/t/(?P<thread_id>[\d]+)/$', MyConv.as_view(form_class=MarketQuickReplyForm), name='postman_view_conversation'),
                        url(r'^view/(?P<message_id>[\d]+)/$', MessageView.as_view(form_class=MarketQuickReplyForm), name='postman_view'),
)
