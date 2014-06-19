from django.conf.urls import patterns, url, include

market_user_patterns = patterns('',
    # Unsecured entry points
    url(r'(?P<rtype>\S+)/unsecured/userprofile/get/(?P<username>\S+)$',
        'app.market.api.views.users.get_profile_insecure',
        name="get_userprofile_insecure"),

    # Secured entry points
    url(r'(?P<rtype>\S+)/avatar/get/(?P<obj_id>\d+)/(?P<size>\d+)$',
        'app.market.api.views.users.get_avatar',
        name="get_avatar"),

    url(r'(?P<rtype>\S+)/userprofile/get/(?P<username>\S+)$',
        'app.market.api.views.users.get_profile',
        name="get_userprofile"),

    url(r'(?P<rtype>\S+)/users/get/count$',
        'app.market.api.views.users.get_user_count',
        name="get_usercount"),

    url(r'(?P<rtype>\S+)/users/get/from/(?P<sfrom>\d+)/to/(?P<to>\d+)$',
        'app.market.api.views.users.get_users_fromto',
        name="get_user_fromto"),

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

    url(r'(?P<rtype>\S+)/issues/get$',
        'app.market.api.views.misc.get_issues',
        name="get_issues"),

    url(r'(?P<rtype>\S+)/countries/get$',
        'app.market.api.views.misc.get_countries',
        name="get_countries"),

    url(r'(?P<rtype>\S+)/nationalities/get$',
        'app.market.api.views.misc.get_nationalities',
        name="get_nationalities"),

    url(r'(?P<rtype>\S+)/skills/get$',
        'app.market.api.views.misc.get_skills',
        name="get_skills"),

    url(r'(?P<rtype>\S+)/message/get/count$',
        'app.market.api.views.misc.get_unreadCount',
        name="get_messagecount"),
)


market_item_patterns = patterns('',
    url(r'(?P<rtype>\S+)/useritem/get/(?P<obj_id>\d+)$',
        'app.market.api.views.market.user_get_marketitem',
        name="user_get_marketitem"),

    url(r'(?P<rtype>\S+)/item/get/from/(?P<sfrom>\d+)/to/(?P<to>\d+)$',
        'app.market.api.views.market.get_marketItem_fromto',
        name="get_marketitems_fromto"),

    url(r'(?P<rtype>\S+)/useritem/get/from/(?P<sfrom>\d+)/to/(?P<to>\d+)$',
        'app.market.api.views.market.get_user_marketitem_fromto',
        name="get_usermarketitems_fromto"),

    url(r'(?P<rtype>\S+)/item/close/(?P<obj_id>\d+)$',
        'app.market.api.views.market.close_market_item',
        name="close_marketitem"),

    url(r'(?P<rtype>\S+)/item/set/rate/(?P<obj_id>\d+)$',
        'app.market.api.views.market.set_rate',
        name="market_set_rate"),

    url(r'(?P<rtype>\S+)/item/get/count/(?P<obj_id>\d+)$',
        'app.market.api.views.market.get_views_count',
        name="marketitem_views_count"),

    url(r'(?P<rtype>\S+)/item/set/hide/(?P<obj_id>\d+)$',
        'app.market.api.views.market.hide_item',
        name="marketitem_hide"),

    url(r'(?P<rtype>\S+)/item/set/unhide/(?P<obj_id>\d+)$',
        'app.market.api.views.market.unhide_item',
        name="marketitem_unhide"),

    url(r'(?P<rtype>\S+)/item/set/stick/(?P<obj_id>\d+)$',
        'app.market.api.views.market.stick_item',
        name="stick_item"),

    url(r'(?P<rtype>\S+)/item/set/unstick/(?P<obj_id>\d+)$',
            'app.market.api.views.market.unstick_item',
            name="unstick_item"),
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

    url(r'(?P<rtype>\S+)/comment/delete/(?P<obj_id>\d+)$',
        'app.market.api.views.comments.delete_comment',
        name="delete_comment"),
)

report_patterns = patterns('',
    url(r'(?P<rtype>\S+)/report/(?P<obj_id>\d+)$',
        'app.market.api.views.report.report_marketitem',
        name="report_post"),

    url(r'(?P<rtype>\S+)/report/user/(?P<username>\S+)$',
        'app.market.api.views.report.report_user',
        name="report_user"),
)

market_notificatoin_patterns = patterns('',
    url(r'(?P<rtype>\S+)/notifications/get/(?P<sfrom>\d+)/(?P<to>\d+)$',
        'app.market.api.views.market.get_notifications_fromto',
        name="get_notifications_fromto"),

    url(r'(?P<rtype>\S+)/notifications/get/notseen/(?P<sfrom>\d+)/(?P<to>\d+)$',
        'app.market.api.views.market.get_notseen_notifications',
        name="get_notseen_notif"),
)


urlpatterns = patterns('',
    url(r'', include(market_item_patterns)),
    url(r'', include(market_comment_patterns)),
    url(r'', include(market_user_patterns)),
    url(r'', include(market_notificatoin_patterns)),
    url(r'', include(report_patterns)),
    )
