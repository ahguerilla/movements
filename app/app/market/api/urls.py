from django.conf.urls import patterns, include, url
from django.conf import settings


urlpatterns = patterns('',
    url(r'(?P<rtype>\S+)/avatar/get/(?P<obj_id>\d+)$',
        'app.market.api.views.users.getAvatar',
        name="get_avatar"),

    url(r'(?P<rtype>\S+)/userdetail/get/(?P<obj_id>\d+)$',
        'app.market.api.views.users.getDetails',
        name="get_userdetail"),


    url(r'(?P<rtype>\S+)/csrftoken/get$',
        'app.market.api.views.misc.getSCRFToken',
        name="get_csrftoken"),


    url(r'(?P<rtype>\S+)/issues/get$',
        'app.market.api.views.misc.getIssues',
        name="get_issues"),

    url(r'(?P<rtype>\S+)/countries/get$',
        'app.market.api.views.misc.getCountries'
        , name="get_countries"),

    url(r'(?P<rtype>\S+)/nationalities/get$',
        'app.market.api.views.misc.getNationalities',
        name="get_nationalities"),

    url(r'(?P<rtype>\S+)/skills/get$',
        'app.market.api.views.misc.getSkills',
        name="get_skills"),


    url(r'(?P<rtype>\S+)/item/add/(?P<obj_type>offer|request|resource)$',
        'app.market.api.views.market.addMarketItem',
        name="add_marketitem"),

    url(r'(?P<rtype>\S+)/item/get/(?P<obj_id>\d+)$',
        'app.market.api.views.market.getMarketItem',
        name="get_marketitem"),

    url(r'(?P<rtype>\S+)/item/get/last/(?P<count>\d+)$',
        'app.market.api.views.market.getMarketItemLast',
        name="get_marketitems_last"),

    url(r'(?P<rtype>\S+)/item/get/from/(?P<sfrom>\d+)/to/(?P<to>\d+)$',
        'app.market.api.views.market.getMarketItemFromTo',
        name="get_marketitems_fromto"),

    url(r'(?P<rtype>\S+)/item/edit/(?P<obj_id>\d+)$',
        'app.market.api.views.market.editMarketItem',
        name="edit_marketitem"),

    url(r'(?P<rtype>\S+)/item/delete/(?P<obj_id>\d+)$',
        'app.market.api.views.market.deleteMarketItem',
        name="delete_marketitem"),

    url(r'(?P<rtype>\S+)/item/userposts$',
        'app.market.api.views.market.userMarketItems',
        name="user_marketitems"),


    url(r'(?P<rtype>\S+)/comment/add/(?P<obj_id>\d+)$',
        'app.market.api.views.comments.addComment',
        name="add_comment"),

    url(r'(?P<rtype>\S+)/comment/get/(?P<obj_id>\d+)$',
        'app.market.api.views.comments.getComment',
        name="get_comment"),

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
        'app.market.api.views.comments.getComment',
        name="delete_comment"),

)
