from django.shortcuts import render_to_response
from django.template import RequestContext
from .api.utils import *
from app.market.forms import commentForm
from django.contrib.auth.decorators import login_required
from app.market.models import MarketItem, Notification
from app.market.api.views.market import getMarketjson


def getUserTags(user):
    all_skills = []
    all_countris = []
    all_issues = []
    if hasattr (user, 'userprofile'):
      all_skills = user.userprofile.skills.all()
      all_countris = user.userprofile.countries.all()
      all_issues = user.userprofile.issues.all()

    return {'skills': [up.pk for up in all_skills],
            'countries': [up.pk for up in all_countris],
            'issues': [up.pk for up in all_issues]}


@login_required
def index(request):
    return render_to_response('market/market.html',
                              {
                                  'title':'My Exchange',
                                  'help_text_template': 'market/copy/market_help.html',
                                  'init': 'market',
                                  'tags': getUserTags(request.user)
                                  },
                              context_instance=RequestContext(request))


@login_required
def users(request):
    return render_to_response('market/market.html',
                              {
                                  'title':'Exchangivists',
                                  'help_text_template': 'market/copy/user_help.html',
                                  'init': 'users',
                                  'tags': getUserTags(request.user)
                                  },
                              context_instance=RequestContext(request))


@login_required
def posts(request):
    return render_to_response('market/market.html',
                              {
                                  'title':'My Posts',
                                  'help_text_template': 'market/copy/myposts_help.html',
                                  'init': 'posts',
                                  'tags': getUserTags(request.user)
                                  },
                              context_instance=RequestContext(request))


@login_required
def addItem_form(request, obj_type):
    return render_to_response('market/%s_form.html' % obj_type,
                              {
                                  'item':'false',
                                  },
                              context_instance=RequestContext(request))


@login_required
def editItem_form(request,obj_id):
    obj = MarketItem.objects.get(id=obj_id)

    return render_to_response('market/%s_form.html' % obj.item_type,
                              {
                                  'item': getMarketjson([obj]),
                                  },
                              context_instance=RequestContext(request))

@login_required
def viewItem(request,obj_type,obj_id):
    return render_to_response('market/item_single.html',
                              {
                                  'item': {'id':str(obj_id)},
                                  'obj_type': '"%s"'%obj_type
                                  },
                              context_instance=RequestContext(request))


@login_required
def addComment_form(request,obj_id):
    form = commentForm()
    return render_to_response('market/comment_form.html',
                              {
                                  'obj_id': str(obj_id),
                                  'form': form,
                                  'coment': 'false'
                                  },
                              context_instance=RequestContext(request))


@login_required
def editComment_form(request,obj_id):
    form = commentForm()
    return render_to_response('market/comment_form.html',
                              {
                                  'obj_type' : '',
                                  'obj_id': '""',
                                  'form': form,
                                  'coment': {'id':str(obj_id)}
                                  },
                              context_instance=RequestContext(request))
