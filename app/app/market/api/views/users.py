import json

from app.market.api.utils import *
import app.market as market
from app.market.forms import item_forms,saveMarketItem
import app.users as users
from django.core import serializers
from django.db.models import Q,Count,Avg
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404,render_to_response, RequestContext


def returnItemList(obj, rtype):
    return HttpResponse(
        value(rtype,
              obj,
              use_natural_keys=True,
              fields=('user',
                      'issues',
                      'countries',
                      'skills',
                      'bio',
                      'tag_ling',
                      'is_organisation',
                      'is_individual',
                      'is_journalist',
                      'occupation',
                      'expertise',
                      'resident_country',
                      'nationality')
              ),
        mimetype="application/"+rtype)


def createQuery(request):    
    if request.GET.has_key('skills'):
        query = Q(skills__in= request.GET.getlist('skills')) 

    if request.GET.has_key('countries'):        
        query = query | Q(countries__in = request.GET.getlist('countries'))

    if request.GET.has_key('issues'):        
        query = query | Q(issues__in=request.GET.getlist('issues'))

    if request.GET.has_key('search') and request.GET['search']!='':
        # objs = SearchQuerySet().filter(text=request.GET['search'])    
        # ids= [int(obj.pk) for obj in objs]
        ids = [1,2] 
        query = query & Q(id__in = ids)

    return query


def getAvatar(request,obj_id, rtype):
    user = get_object_or_404(users.models.User, pk=obj_id)
    obj = user.avatar_set.all()
    if obj != []:
        return HttpResponse(value(rtype,obj),mimetype="application"+rtype)
    return HttpResponse(value(rtype, [{'pk': 0, 'avatar': '/static/images/male200.png' },]),mimetype="application"+rtype)


def getDetails(request,obj_id, rtype):
    user = get_object_or_404(users.models.User, pk=obj_id)
    return HttpResponse(
        value(rtype,
              [user],
              fields=('username',)
              ),
        mimetype="application"+rtype)


def getUsersFromto(request,sfrom,to,rtype):
    query = createQuery(request)    
    obj = users.models.UserProfile.objects.filter(query).distinct('id').order_by('-id')[sfrom:to]    
    return returnItemList(obj, rtype)


def getUserCount(request,rtype):
    query = createQuery(request)
    obj = users.models.UserProfile.objects.filter(query).distinct('id').order_by('-id').count()
    return  HttpResponse(json.dumps({ 'success' : True, 'count': obj}),mimetype="application"+rtype)