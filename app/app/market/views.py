from django.contrib.auth.decorators import permission_required
from django.db.models import Q,Max,F
from django.http import HttpResponse
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext, loader
from .api.utils import *
from app.market.forms import item_forms,commentForm


def getUserTags(user):
    return {'skills': [up.pk for up in user.userprofile.skills.all()],
            'countries': [up.pk for up in user.userprofile.countries.all()],
            'issues': [up.pk for up in user.userprofile.issues.all()]}


def index(request):
    return render_to_response('market.html',
                              {
                                  'title':'My Exchange',
                                  'init': 'market',
                                  'tags': getUserTags(request.user)
                                  },
                              context_instance=RequestContext(request))


def users(request):
    return render_to_response('market.html',
                              {
                                  'title':'Users',
                                  'init': 'users',
                                  'tags': getUserTags(request.user)
                                  },
                              context_instance=RequestContext(request))


def addItem_form(request,obj_type):
    return render_to_response('item_form.html',
                              {
                                  'item':'false',
                                  'obj_type':'"%s"'%obj_type
                                  },
                              context_instance=RequestContext(request))


def editItem_form(request,obj_id):
    return render_to_response('item_form.html',
                              {
                                  'item': {'id':str(obj_id)},
                                  'obj_type':'false'
                                  },
                              context_instance=RequestContext(request))


def viewItem(request,obj_type,obj_id):
    return render_to_response('item_single.html',
                              {
                                  'item': {'id':str(obj_id)},
                                  'obj_type': '"%s"'%obj_type
                                  },
                              context_instance=RequestContext(request))


def addComment_form(request,obj_id):
    form = commentForm()
    return render_to_response('comment_form.html',
                              {
                                  'obj_id': str(obj_id),
                                  'form': form,
                                  'coment': 'false'
                                  },
                              context_instance=RequestContext(request))



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


def posts(request):
    return render_to_response('market.html',
                              {
                                  'title':'My Posts',
                                  'init': 'posts',
                                  'tags': getUserTags(request.user)
                                  },
                              context_instance=RequestContext(request))
