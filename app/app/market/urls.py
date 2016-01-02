from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
                       url(r'market/api/', include('app.market.api.urls')),
                       url(r'market/test/', include('app.market.test.urls')),
                       url(r'^market/$', 'app.market.views.index', name="show_market"),
                       url(r'^market/translations$', 'app.market.views.translations', name="show_translations"),
                       url(r'^market/requestposted$', 'app.market.views.request_posted', name="request_posted"),
                       url(r'^market/(?P<post_id>\d+)$', 'app.market.views.show_post', name="show_post"),
                       url(r'^market/(?P<post_id>\d+)/edit$', 'app.market.views.edit_post', name="edit_post"),
                       url(r'^market/(?P<post_id>\d+)/([^/]+)$', 'app.market.views.show_post', name="show_post"),
                       url(r'^market/offer$', 'app.market.views.create_offer', name="create_offer"),
                       url(r'^market/request$', 'app.market.views.create_request', name="create_request"),
                       url(r'^market/notifications$', 'app.market.views.notifications', name="show_notifications"),
                       url(r'^market/filter/(?P<type_filter>\w+)$', 'app.market.views.index_filter',
                           name="show_market_filter"),
                       url(r'^market/search/', include('haystack.urls')),
                       url('^/messages/inbox/m/$', 'app.market.views.index'),
                       url('^messages/permdelete/', 'app.market.views.permanent_delete_postman',
                           name="permanent_delete_postman"),
                       url(r'^messages/', include('postman.urls')),)


from postman.views import MessageView, ReplyView
from app.market.forms import MarketQuickReplyForm
from cust_postman import MovementsConversationView, MovementsReplyForm

urlpatterns += patterns('postman.views',
                        url(r'^reply/(?P<message_id>[\d]+)/$', ReplyView.as_view(form_class=MovementsReplyForm),
                            name='postman_reply'),
                        url(r'^view/t/(?P<thread_id>[\d]+)/$',
                            MovementsConversationView.as_view(form_class=MarketQuickReplyForm),
                            name='postman_view_conversation'),
                        url(r'^view/(?P<message_id>[\d]+)/$', MessageView.as_view(form_class=MarketQuickReplyForm),
                            name='postman_view'),)
