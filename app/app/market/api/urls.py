from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'(?P<rtype>\S+)/avatar/get/(?P<obj_id>\d+)/(?P<size>\d+)$',
        'app.market.api.views.users.get_avatar',
        name="get_avatar"),

    url(r'(?P<rtype>\S+)/userdetail/get/(?P<obj_id>\d+)$',
        'app.market.api.views.users.get_details',
        name="get_userdetail"),

    url(r'(?P<rtype>\S+)/users/get/count$',
        'app.market.api.views.users.get_user_count',
        name="get_usercount"),

    url(r'(?P<rtype>\S+)/users/get/from/(?P<sfrom>\d+)/to/(?P<to>\d+)$',
        'app.market.api.views.users.get_users_fromto',
        name="get_user_fromto"),

    url(r'(?P<rtype>\S+)/users/sendmessage/(?P<to_user>\S+)$',
        'app.market.api.views.users.send_message',
        name="send_message"),

    url(r'(?P<rtype>\S+)/users/recommend/(?P<rec_type>item|user)/(?P<to_user>\S+)/(?P<obj_id>\d+|\S+)$',
        'app.market.api.views.users.send_recommendation',
        name="send_recommendation"),

    url(r'(?P<rtype>\S+)/users/set/rate/(?P<username>\S+)$',
        'app.market.api.views.users.set_rate',
        name="user_set_rate"),

    url(r'(?P<rtype>\S+)/users/get/usernames$',
        'app.market.api.views.users.get_usernames',
        name="user_get_usernames"),

    url(r'(?P<rtype>\S+)/csrftoken/get$',
        'app.market.api.views.misc.get_CSRF_token',
        name="get_csrftoken"),

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

    url(r'(?P<rtype>\S+)/item/add/(?P<obj_type>offer|request|resource)$',
        'app.market.api.views.market.add_market_item',
        name="add_marketitem"),

    url(r'(?P<rtype>\S+)/item/get/(?P<obj_id>\d+)$',
        'app.market.api.views.market.get_market_item',
        name="get_marketitem"), 
   
    url(r'(?P<rtype>\S+)/useritem/get/(?P<obj_id>\d+)$',
        'app.market.api.views.market.user_get_marketitem',
        name="user_get_marketitem"),

    url(r'(?P<rtype>\S+)/item/get/from/(?P<sfrom>\d+)/to/(?P<to>\d+)$',
        'app.market.api.views.market.get_marketItem_fromto',
        name="get_marketitems_fromto"),

    url(r'(?P<rtype>\S+)/useritem/get/from/(?P<sfrom>\d+)/to/(?P<to>\d+)$',
        'app.market.api.views.market.get_user_marketitem_fromto',
        name="get_usermarketitems_fromto"),

    url(r'(?P<rtype>\S+)/item/edit/(?P<obj_id>\d+)$',
        'app.market.api.views.market.edit_market_item',
        name="edit_marketitem"),

    url(r'(?P<rtype>\S+)/item/delete/(?P<obj_id>\d+)$',
        'app.market.api.views.market.delete_market_item',
        name="delete_marketitem"),

    url(r'(?P<rtype>\S+)/item/set/rate/(?P<obj_id>\d+)$',
        'app.market.api.views.market.set_rate',
        name="market_set_rate"),

    url(r'(?P<rtype>\S+)/comment/add/(?P<obj_id>\d+)$',
        'app.market.api.views.comments.add_comment',
        name="add_comment"),

    url(r'(?P<rtype>\S+)/comment/get/(?P<obj_id>\d+)$',
        'app.market.api.views.comments.get_comment',
        name="get_comment"),

    url(r'(?P<rtype>\S+)/comment/get/count/(?P<obj_id>\d+)$',
        'app.market.api.views.comments.get_comment_count',
        name="get_comment_count"),

    url(r'(?P<rtype>\S+)/comments/get/(?P<obj_id>\d+)/last/(?P<count>\d+)$',
        'app.market.api.views.comments.get_comments',
        name="get_comments_last"),

    url(r'(?P<rtype>\S+)/comments/get/(?P<obj_id>\d+)/range/(?P<st_date>\S+)/(?P<end_date>\S+)$',
        'app.market.api.views.comments.get_commentids_range',
        name="get_comments_range"),

    url(r'(?P<rtype>\S+)/comment/edit/(?P<obj_id>\d+)$',
        'app.market.api.views.comments.edit_comment',
        name="edit_comment"),

    url(r'(?P<rtype>\S+)/comment/delete/(?P<obj_id>\d+)$',
        'app.market.api.views.comments.delete_comment',
        name="delete_comment"),

    url(r'(?P<rtype>\S+)/report/(?P<obj_id>\d+)$',
        'app.market.api.views.report.reportMarketItem',
        name="report_post"),

    url(r'(?P<rtype>\S+)/notifications/get/(?P<sfrom>\d+)/(?P<to>\d+)$',
        'app.market.api.views.market.get_notifications_fromto',
        name="get_notifications_fromto"),    
    
    url(r'(?P<rtype>\S+)/notifications/get/notseen/(?P<sfrom>\d+)/(?P<to>\d+)$',
        'app.market.api.views.market.get_notseen_notifications',
        name="get_notseen_notif"),        
)
