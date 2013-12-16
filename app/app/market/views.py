from django.shortcuts import render_to_response
from django.template import RequestContext
from .api.utils import *
from app.market.forms import commentForm
from django.contrib.auth.decorators import login_required
from app.market.models import MarketItem
from app.market.api.views.market import getMarketjson


def getUserTags(user):
    return {'skills': [up.pk for up in user.userprofile.skills.all()],
            'countries': [up.pk for up in user.userprofile.countries.all()],
            'issues': [up.pk for up in user.userprofile.issues.all()]}


@login_required
def index(request):
    return render_to_response('market.html',
                              {
                                  'title':'My Exchange',
                                  'init': 'market',
                                  'tags': getUserTags(request.user)
                                  },
                              context_instance=RequestContext(request))


@login_required
def users(request):
    return render_to_response('market.html',
                              {
                                  'title':'Users',
                                  'init': 'users',
                                  'tags': getUserTags(request.user)
                                  },
                              context_instance=RequestContext(request))


@login_required
def posts(request):
    return render_to_response('market.html',
                              {
                                  'title':'My Posts',
                                  'init': 'posts',
                                  'tags': getUserTags(request.user)
                                  },
                              context_instance=RequestContext(request))


@login_required
def addItem_form(request,obj_type):    
    return render_to_response(obj_type+'_form.html',
                              {
                                  'item':'false',                                      
                                  },
                              context_instance=RequestContext(request))
   

@login_required
def editItem_form(request,obj_id):
    obj = MarketItem.objects.get(id=obj_id)
   
    return render_to_response(obj.item_type+'_form.html',
                              {
                                  'item': getMarketjson([obj]),                                      
                                  },
                              context_instance=RequestContext(request))    
    #return render_to_response('item_form.html',
                              #{
                                  #'item': {'id':str(obj_id)},
                                  #'obj_type':'false'
                                  #},
                              #context_instance=RequestContext(request))


@login_required
def viewItem(request,obj_type,obj_id):
    return render_to_response('item_single.html',
                              {
                                  'item': {'id':str(obj_id)},
                                  'obj_type': '"%s"'%obj_type
                                  },
                              context_instance=RequestContext(request))


@login_required
def addComment_form(request,obj_id):
    form = commentForm()
    return render_to_response('comment_form.html',
                              {
                                  'obj_id': str(obj_id),
                                  'form': form,
                                  'coment': 'false'
                                  },
                              context_instance=RequestContext(request))


@login_required
def editComment_form(request,obj_id):
    form = commentForm()
    return render_to_response('comment_form.html',
                              {
                                  'obj_type' : '',
                                  'obj_id': '""',
                                  'form': form,
                                  'coment': {'id':str(obj_id)}
                                  },
                              context_instance=RequestContext(request))
