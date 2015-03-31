from django.conf.urls import patterns, url, include
from app.market.models import Comment, MarketItem, MarketItemTranslation, CommentTranslation


market_user_patterns = patterns('',

    # Secured entry points
    url(r'(?P<rtype>\S+)/avatar/get/(?P<obj_id>\d+)/(?P<size>\d+)$',
        'app.market.api.views.users.get_avatar',
        name="get_avatar"),

    url(r'(?P<rtype>\S+)/users/sendmessage/(?P<to_user>\S+)$',
        'app.market.api.views.users.send_message',
        name="send_message"),

    url(r'(?P<rtype>\S+)/users/recommend/(?P<rec_type>item|user)/(?P<obj_id>\d+|\S+)$',
        'app.market.api.views.users.send_recommendation',
        name="send_recommendation"),

    url(r'(?P<rtype>\S+)/users/set/rate/(?P<username>\S+)$',
        'app.market.api.views.users.set_rate',
        name="user_set_rate"),

    url(r'(?P<rtype>\S+)/users/get/usernames$',
        'app.market.api.views.users.get_usernames',
        name="user_get_usernames"),
)


market_item_patterns = patterns('',
    url(r'^items/get/$',
        'app.market.api.views.market.get_market_items',
        name="get_market_items"),

    url(r'(?P<rtype>\S+)/useritem/get/from/(?P<sfrom>\d+)/to/(?P<to>\d+)$',
        'app.market.api.views.market.get_marketitems_fromto',
        name="get_marketitems_fromto"),

    url(r'^featured-items/get/$',
        'app.market.api.views.market.get_featured_market_items',
        name="get_featured_market_items"),

    url(r'^items/sticky',
        'app.market.api.views.market.get_user_stickies',
        name="get_user_stickies"),

    url(r'items/user/get/$',
        'app.market.api.views.market.get_market_items_user',
        name="get_market_items_user"),

    url(r'items/user/get/(?P<user_id>\d+)$',
        'app.market.api.views.market.get_market_items_user',
        name="get_market_items_user"),

    url(r'(?P<rtype>\S+)/useritem/get/from/(?P<sfrom>\d+)/to/(?P<to>\d+)$',
        'app.market.api.views.market.get_user_marketitem_fromto',
        name="get_usermarketitems_fromto"),

    url(r'(?P<rtype>\S+)/useritem/get/user_id/(?P<user_id>\d+)/from/(?P<sfrom>\d+)/to/(?P<to>\d+)$',
        'app.market.api.views.market.get_user_marketitem_for_user_fromto',
        name="get_usermarketitems_for_user_fromto"),

    url(r'item/close/(?P<obj_id>\d+)$',
        'app.market.api.views.market.close_market_item',
        name="close_marketitem"),

    url(r'(?P<rtype>\S+)/item/set/rate/(?P<obj_id>\d+)$',
        'app.market.api.views.market.set_rate',
        name="market_set_rate"),

    url(r'item/set/user_attributes/(?P<item_id>\d+)$',
        'app.market.api.views.market.set_item_attributes_for_user',
        name="set_item_attributes_for_user"),
)


market_comment_patterns = patterns('',
    url(r'(?P<rtype>\S+)/comment/add/(?P<obj_id>\d+)$',
        'app.market.api.views.comments.add_comment',
        name="add_comment"),

    url(r'(?P<rtype>\S+)/comments/get/(?P<obj_id>\d+)/last/(?P<count>\d+)$',
        'app.market.api.views.comments.get_comments',
        name="get_comments_last"),

    url(r'(?P<rtype>\S+)/comment/edit/(?P<obj_id>\d+)$',
        'app.market.api.views.comments.edit_comment',
        name="edit_comment"),

    url(r'comment/delete$',
        'app.market.api.views.comments.delete_comment',
        name="delete_comment"),
)

report_patterns = patterns('',
    url(r'report/(?P<obj_id>\d+)',
        'app.market.api.views.report.report_marketitem',
        name="report_post"),

    url(r'(?P<rtype>\S+)/report/user/(?P<username>\S+)$',
        'app.market.api.views.report.report_user',
        name="report_user"),
)

market_notification_patterns = patterns('',
    url(r'notifications/get/(?P<sfrom>\d+)/(?P<to>\d+)$',
        'app.market.api.views.market.get_notifications_fromto',
        name="get_notifications_fromto"),

    url(r'notifications/get/notseen$',
        'app.market.api.views.market.get_notseen_notifications',
        name="get_notseen_notif"),
)

market_heartbeat_patters = patterns('',
    url(r'heartbeat/get/counts$',
        'app.market.api.views.heartbeat.get_counts',
        name="heartbeat"),
)

post_translation_patterns = patterns(
    'app.market.api.views.translation',
    url(r'^(?P<object_id>\d+)/take-in/$', 'take_in', {'model': MarketItemTranslation}, name="take_in"),
    url(r'^(?P<object_id>\d+)/take-off/$', 'take_off', {'model': MarketItemTranslation}, name="take_off"),
    url(r'^(?P<object_id>\d+)/save-draft/$', 'save_draft', {'model': MarketItemTranslation}, name="save_draft"),
    url(r'^(?P<object_id>\d+)/mark-done/$', 'done', {'model': MarketItemTranslation}, name="done"),
    url(r'^(?P<object_id>\d+)/approve/$', 'approve', {'model': MarketItemTranslation}, name="approve"),
    url(r'^(?P<object_id>\d+)/revoke/$', 'revoke', {'model': MarketItemTranslation}, name="revoke"),
    url(r'^(?P<object_id>\d+)/correct/$', 'corrections', {'model': MarketItemTranslation}, name="corrections"),
    url(r'^(?P<object_id>\d+)/$', 'translate', {'model': MarketItemTranslation}, name="translate"),
)

comment_translation_patterns = patterns(
    'app.market.api.views.translation',
    url(r'^(?P<object_id>\d+)/take-in/$', 'take_in', {'model': CommentTranslation}, name="take_in"),
    url(r'^(?P<object_id>\d+)/take-off/$', 'take_off', {'model': CommentTranslation}, name="take_off"),
    url(r'^(?P<object_id>\d+)/save-draft/$', 'save_draft', {'model': MarketItemTranslation}, name="save_draft"),
    url(r'^(?P<object_id>\d+)/mark-done/$', 'done', {'model': CommentTranslation}, name="done"),
    url(r'^(?P<object_id>\d+)/approve/$', 'approve', {'model': CommentTranslation}, name="approve"),
    url(r'^(?P<object_id>\d+)/revoke/$', 'revoke', {'model': CommentTranslation}, name="revoke"),
    url(r'^(?P<object_id>\d+)/correct/$', 'corrections', {'model': CommentTranslation}, name="corrections"),
    url(r'^(?P<object_id>\d+)/$', 'translate', {'model': CommentTranslation}, name="translate"),
)

market_translation_patterns = patterns(
    '',
    url(r'^item/translation/', include(post_translation_patterns, namespace='market')),
    url(r'^comment/translation/', include(comment_translation_patterns, namespace='comment')),
)

urlpatterns = patterns(
    '',
    url(r'', include(market_item_patterns)),
    url(r'', include(market_comment_patterns)),
    url(r'', include(market_user_patterns)),
    url(r'', include(market_notification_patterns)),
    url(r'', include(report_patterns)),
    url(r'', include(market_heartbeat_patters)),
    url(r'', include(market_translation_patterns, namespace='translation')),
)
