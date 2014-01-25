from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'(?P<rtype>\S+)/avatar/get/(?P<obj_id>\d+)/(?P<size>\d+)$',
        'app.market.api.views.users.getAvatar',
        name="get_avatar"),

    url(r'(?P<rtype>\S+)/userdetail/get/(?P<obj_id>\d+)$',
        'app.market.api.views.users.getDetails',
        name="get_userdetail"),

    url(r'(?P<rtype>\S+)/users/get/count$',
        'app.market.api.views.users.getUserCount',
        name="get_usercount"),

    url(r'(?P<rtype>\S+)/users/get/from/(?P<sfrom>\d+)/to/(?P<to>\d+)$',
        'app.market.api.views.users.getUsersFromto',
        name="get_user_fromto"),

    url(r'(?P<rtype>\S+)/users/sendmessage/(?P<to_user>\S+)$',
        'app.market.api.views.users.sendMessage',
        name="send_message"),

    url(r'(?P<rtype>\S+)/users/recommend/(?P<rec_type>item|user)/(?P<to_user>\S+)/(?P<obj_id>\d+|\S+)$',
        'app.market.api.views.users.sendRecommendation',
        name="send_recommendation"),

    url(r'(?P<rtype>\S+)/users/set/rate/(?P<username>\S+)$',
        'app.market.api.views.users.setRate',
        name="user_set_rate"),

    url(r'(?P<rtype>\S+)/users/get/usernames$',
        'app.market.api.views.users.getUsernames',
        name="user_get_usernames"),

    url(r'(?P<rtype>\S+)/csrftoken/get$',
        'app.market.api.views.misc.getSCRFToken',
        name="get_csrftoken"),

    url(r'(?P<rtype>\S+)/issues/get$',
        'app.market.api.views.misc.getIssues',
        name="get_issues"),

    url(r'(?P<rtype>\S+)/countries/get$',
        'app.market.api.views.misc.getCountries',
        name="get_countries"),

    url(r'(?P<rtype>\S+)/nationalities/get$',
        'app.market.api.views.misc.getNationalities',
        name="get_nationalities"),

    url(r'(?P<rtype>\S+)/skills/get$',
        'app.market.api.views.misc.getSkills',
        name="get_skills"),

    url(r'(?P<rtype>\S+)/message/get/count$',
        'app.market.api.views.misc.getUnreadCount',
        name="get_messagecount"),

    url(r'(?P<rtype>\S+)/item/add/(?P<obj_type>offer|request|resource)$',
        'app.market.api.views.market.addMarketItem',
        name="add_marketitem"),

    url(r'(?P<rtype>\S+)/item/get/(?P<obj_id>\d+)$',
        'app.market.api.views.market.getMarketItem',
        name="get_marketitem"),

    url(r'(?P<rtype>\S+)/item/get/last/(?P<count>\d+)$',
        'app.market.api.views.market.getMarketItemLast',
        name="get_marketitems_last"),

    url(r'(?P<rtype>\S+)/item/get/count$',
        'app.market.api.views.market.getMarketItemCount',
        name="get_marketitem_count"),

    url(r'(?P<rtype>\S+)/useritem/get/count$',
        'app.market.api.views.market.userMarketItemsCount',
        name="user_items_count"),

    url(r'(?P<rtype>\S+)/useritem/get/(?P<obj_id>\d+)$',
        'app.market.api.views.market.userGetMarketItem',
        name="user_get_marketitem"),

    url(r'(?P<rtype>\S+)/item/get/from/(?P<sfrom>\d+)/to/(?P<to>\d+)$',
        'app.market.api.views.market.getMarketItemFromTo',
        name="get_marketitems_fromto"),

    url(r'(?P<rtype>\S+)/useritem/get/from/(?P<sfrom>\d+)/to/(?P<to>\d+)$',
        'app.market.api.views.market.getUserMarketItemFromTo',
        name="get_usermarketitems_fromto"),

    url(r'(?P<rtype>\S+)/item/edit/(?P<obj_id>\d+)$',
        'app.market.api.views.market.editMarketItem',
        name="edit_marketitem"),

    url(r'(?P<rtype>\S+)/item/delete/(?P<obj_id>\d+)$',
        'app.market.api.views.market.deleteMarketItem',
        name="delete_marketitem"),

    url(r'(?P<rtype>\S+)/item/userposts$',
        'app.market.api.views.market.userMarketItems',
        name="user_marketitems"),

    url(r'(?P<rtype>\S+)/item/set/rate/(?P<obj_id>\d+)$',
        'app.market.api.views.market.setRate',
        name="market_set_rate"),

    url(r'(?P<rtype>\S+)/comment/add/(?P<obj_id>\d+)$',
        'app.market.api.views.comments.addComment',
        name="add_comment"),

    url(r'(?P<rtype>\S+)/comment/get/(?P<obj_id>\d+)$',
        'app.market.api.views.comments.getComment',
        name="get_comment"),

    url(r'(?P<rtype>\S+)/comment/get/count/(?P<obj_id>\d+)$',
        'app.market.api.views.comments.getCommentCount',
        name="get_comment_count"),

    url(r'(?P<rtype>\S+)/comments/get/(?P<obj_id>\d+)/last/(?P<count>\d+)$',
        'app.market.api.views.comments.getComments',
        name="get_comments_last"),

    url(r'(?P<rtype>\S+)/comments/get/(?P<obj_id>\d+)/range/(?P<st_date>\S+)/(?P<end_date>\S+)$',
        'app.market.api.views.comments.getCommentIdsRange',
        name="get_comments_range"),

    url(r'(?P<rtype>\S+)/comment/edit/(?P<obj_id>\d+)$',
        'app.market.api.views.comments.editComment',
        name="edit_comment"),

    url(r'(?P<rtype>\S+)/comment/delete/(?P<obj_id>\d+)$',
        'app.market.api.views.comments.deleteComment',
        name="delete_comment"),

    url(r'(?P<rtype>\S+)/report/(?P<obj_id>\d+)$',
        'app.market.api.views.report.reportMarketItem',
        name="report_post"),

)
