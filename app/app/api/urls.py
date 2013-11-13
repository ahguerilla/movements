from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('',
    url(r'(?P<rtype>\S+)/get/csrftoken$',
        'app.api.views.misc.getSCRFToken',
        name="get_issues"),


    url(r'(?P<rtype>\S+)/get/issues$',
        'app.api.views.misc.getIssues',
        name="get_issues"),

    url(r'(?P<rtype>\S+)/get/countries$',
        'app.api.views.misc.getCountries'
        , name="get_countries"),

    url(r'(?P<rtype>\S+)/get/nationalities$',
        'app.api.views.misc.getNationalities',
        name="get_nationalities"),

    url(r'(?P<rtype>\S+)/get/skills$',
        'app.api.views.misc.getSkills',
        name="get_skills"),



    url(r'(?P<rtype>\S+)/add/offer$',
        'app.api.views.offers.addOffer',
        name="add_offer"),

    url(r'(?P<rtype>\S+)/get/offer/(?P<obj_id>\d+)$',
        'app.api.views.offers.getOffer',
        name="get_offer"),

    url(r'(?P<rtype>\S+)/edit/offer/(?P<obj_id>\d+)$',
        'app.api.views.offers.editOffer',
        name="edit_offer"),

    url(r'(?P<rtype>\S+)/delete/offer/(?P<obj_id>\d+)$',
        'app.api.views.offers.deleteOffer',
        name="delete_offer"),



    url(r'(?P<rtype>\S+)/add/comment/(?P<obj_type>\S+)/(?P<obj_id>\d+)$',
        'app.api.views.comments.addComment',
        name="add_comment"),

    url(r'(?P<rtype>\S+)/get/comment/(?P<obj_id>\d+)$',
        'app.api.views.comments.getComment',
        name="get_comment"),

    url(r'(?P<rtype>\S+)/get/comments/(?P<obj_type>\S+)/(?P<obj_id>\d+)/last/(?P<count>\d+)$',
        'app.api.views.comments.getComments',
        name="get_comments"),

    url(r'(?P<rtype>\S+)/get/comments/(?P<obj_type>\S+)/(?P<obj_id>\d+)/range/(?P<st_date>\S+)/(?P<end_date>\S+)$',
        'app.api.views.comments.getCommentIdsRange',
        name="get_comments"),

    url(r'(?P<rtype>\S+)/edit/comment/(?P<obj_id>\d+)$',
        'app.api.views.comments.editComment',
        name="edit_comment"),

    url(r'(?P<rtype>\S+)/delete/comment/(?P<obj_id>\d+)$',
        'app.api.views.comments.getComment',
        name="delete_comment"),

)
