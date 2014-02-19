import json

from app.market.api.utils import *
import app.market as market
from app.market.forms import item_forms,saveMarketItem
import app.users as users
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404,render_to_response, RequestContext
from django.db.models import Q,Count,Avg
from haystack.views import SearchView
from haystack.query import SearchQuerySet
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.html import escape
from datetime import datetime
from tasks.celerytasks import create_notification, update_notifications, mark_read_notifications 
from django.utils.cache import get_cache_key, get_cache
cache = get_cache('default')
items_cache = get_cache('items')

def get_market_json(objs):
    alist = []
    for obj in objs:
        alist.append(obj.getdict())
    return json.dumps(alist)


def return_item_list(obj, rtype):
    return HttpResponse(
        get_market_json(obj),
        mimetype="application/"+rtype)


def create_query(request):
    query = Q()
    if request.GET.has_key('skills'):
        query = query | Q(skills__in=request.GET.getlist('skills'))

    if request.GET.has_key('countries'):
        query = query | Q(countries__in=request.GET.getlist('countries'))

    if request.GET.has_key('issues'):
        query = query | Q(issues__in=request.GET.getlist('issues'))

    if request.GET.has_key('types'):
        query = query & Q(item_type__in=request.GET.getlist('types'))

    if request.GET.has_key('search') and request.GET['search']!='':
        objs = SearchQuerySet().models(market.models.MarketItem).filter(text=request.GET['search'])
        ids= [int(obj.pk) for obj in objs]
        query = query & Q(id__in=ids)
    query = query & Q(published=True) & Q(deleted=False) & Q(owner__is_active=True)
    return query


@login_required
def add_market_item(request, obj_type, rtype):
    form = item_forms[obj_type](request.POST)
    if form.is_valid():
        obj = saveMarketItem(form, obj_type, request.user)
        create_notification.delay(obj)
        items_cache.clear()
    else:
        return HttpResponseError(json.dumps(get_validation_errors(form)), mimetype="application"+rtype)
    return HttpResponse(json.dumps({ 'success' : True, 'pk':obj.id}),mimetype="application"+rtype)


@login_required
def get_market_item(request,obj_id,rtype):
    retval = cache.get('item-'+obj_id )
    if retval:
        mark_read_notifications.delay((obj_id,),request.user.id)
        return retval        
    obj = get_object_or_404(market.models.MarketItem.objects.defer('comments'),
                            Q(exp_date__gte=datetime.now())|Q(never_exp=True),
                            pk=obj_id,
                            deleted=False,
                            owner__is_active=True)
    mark_read_notifications.delay((obj.id,),request.user.id)
    retval = return_item_list([obj], rtype)
    cache.add('item-'+obj_id, retval )
    return retval 


@login_required
def get_marketItem_fromto(request,sfrom,to,rtype):
    reqhash = hash(request.path+str(request.GET))
    retval = items_cache.get(reqhash)
    if retval: 
        return retval            
    query = create_query(request)
    obj = market.models.MarketItem.objects.filter(Q(exp_date__gte=datetime.now())|Q(never_exp=True)).filter(query).distinct('id').order_by('-id').defer('comments')[sfrom:to]
    retval = return_item_list(obj, rtype)
    items_cache.add(reqhash, retval)
    return retval


@login_required
def get_marketitem_count(request,rtype):
    query = create_query(request)
    obj = market.models.MarketItem.objects.filter(Q(exp_date__gte=datetime.now())|Q(never_exp=True)).filter(query).distinct('id').order_by('-id').count()
    return  HttpResponse(json.dumps({ 'success' : True, 'count': obj}),mimetype="application"+rtype)


@login_required
@check_perms_and_get(market.models.MarketItem)
def edit_market_item(request,obj_id,rtype):
    cache.delete('item-'+obj_id)
    items_cache.clear()
    obj = request.obj
    form = item_forms[obj.item_type](request.POST, instance=obj)
    if form.is_valid():
        saveMarketItem(form, obj.item_type, obj.owner)
        update_notifications.delay(obj)
    else:
        return HttpResponseError(json.dumps(get_validation_errors(form)), mimetype="application/"+rtype)
    return HttpResponse(json.dumps({ 'success' : True}),
                        mimetype="application"+rtype)


@login_required
@check_perms_and_get(market.models.MarketItem)
def delete_market_item(request,obj_id,rtype):
    cache.delete('item-'+obj_id)
    items_cache.clear()
    obj=request.obj
    obj.deleted = True
    obj.save()
    return HttpResponse(json.dumps({ 'success' : True}),
                        mimetype="application"+rtype)


@login_required
@check_perms_and_get(market.models.MarketItem)
def user_get_marketitem(request,obj_id,rtype):
    return return_item_list([request.obj], rtype)


@login_required
def user_marketitems(request, rtype):
    obj = market.models.MarketItem.objects.filter(deleted=False).defer('comments').filter(owner=request.user).all()
    return return_item_list(obj, rtype)


@login_required
def user_marketitems_count(request,rtype):
    query = create_query(request)
    obj = market.models.MarketItem.objects.filter(owner=request.user).filter(query).distinct('id').order_by('-id').count()
    return  HttpResponse(json.dumps({ 'success' : True, 'count': obj}),
                         mimetype="application"+rtype)


@login_required
def get_user_marketitem_fromto(request,sfrom,to,rtype):
    query = create_query(request)
    obj = market.models.MarketItem.objects.filter(owner=request.user).filter(query).distinct('id').order_by('-id').defer('comments')[sfrom:to]
    return return_item_list(obj, rtype)


@login_required
def set_rate(request,obj_id,rtype):
    if not request.POST.has_key('score'):
        return HttpResponseError()
    item = market.models.MarketItem.filter(Q(exp_date__gte=datetime.now())|Q(never_exp=True)).objects.filter(id=obj_id)[0]
    owner = request.user
    rate = market.models.ItemRate.objects.filter(owner=owner).filter(item=item)
    if len(rate)==0:
        rate = market.models.ItemRate(owner=owner, item=item)
    else:
        rate = rate[0]
    rate.score =  int(request.POST['score'])
    rate.save()
    rate.save_base()
    mark_read_notifications.delay((item.id,),request.user.id)
    return HttpResponse(
        json.dumps({'success': 'true',
                    'score':item.score ,
                    'ratecount':item.ratecount
                    }),
        mimetype="application/"+rtype)


@login_required
def get_notifications_fromto(request,sfrom,to,rtype):
    notifications = market.models.Notification.objects.filter(user=request.user.id,item__deleted=False)[sfrom:to]
    alist=[]
    for notification in notifications:
        alist.append(notification.getDict()) 
        if not notification.seen:
            notification.seen = True        
            notification.save()    
    return  HttpResponse(json.dumps({'notifications':alist}),
                         mimetype="application"+rtype)


@login_required
def get_notseen_notifications(request,sfrom,to,rtype):
    notifications = market.models.Notification.objects.filter(user=request.user.id,item__deleted=False).filter(seen=False).only('seen')
    if len(notifications)>0:
        return  HttpResponse(json.dumps({'result':True}),
                             mimetype="application"+rtype)
    return  HttpResponse(json.dumps({'result':False}),
                         mimetype="application"+rtype)
