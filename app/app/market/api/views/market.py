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


def returnItemList(obj, rtype):
    return HttpResponse(
        value(rtype,
              obj,
              use_natural_keys=True,
              fields=('item_type',
                      'issues',
                      'countries',
                      'skills',
                      'title',
                      'details',
                      'pub_date',
                      'exp_date',
                      'owner',
                      'url',
                      'files',
                      'commentcount')
              ),
        mimetype="application/"+rtype)


def createQuery(request):
    query = Q(published=True)
    if request.GET.has_key('skills'):
        query = query | Q(skills__in= request.GET.getlist('skills'))

    if request.GET.has_key('countries'):
        query = query | Q(countries__in = request.GET.getlist('countries'))

    if request.GET.has_key('issues'):
        query = query | Q(issues__in=request.GET.getlist('issues'))

    if request.GET.has_key('types'):
        query = query & Q(item_type__in=request.GET.getlist('types'))

    if request.GET.has_key('search') and request.GET['search']!='':
        objs = SearchQuerySet().filter(text=request.GET['search'])
        ids= [int(obj.pk) for obj in objs]
        query = query & Q(id__in = ids)

    return query


@login_required
def addMarketItem(request, obj_type, rtype):
    form = item_forms[obj_type](request.POST)
    if form.is_valid():
        obj = saveMarketItem(form, obj_type, request.user)
    else:
        return HttpResponseError(json.dumps(get_validation_errors(form)), mimetype="application"+rtype)
    return HttpResponse(json.dumps({ 'success' : True, 'pk':obj.id}),mimetype="application"+rtype)


@login_required
def getMarketItem(request,obj_id,rtype):
    obj = get_object_or_404(market.models.MarketItem.objects.defer('comments'), pk=obj_id)
    return returnItemList([obj], rtype)


@login_required
def getMarketItemLast(request,count,rtype):
    obj = market.models.MarketItem.objects.order_by('-pub_date').defer('comments')[:count]
    return returnItemList(obj, rtype)


@login_required
def getMarketItemFromTo(request,sfrom,to,rtype):
    query = createQuery(request)
    obj = market.models.MarketItem.objects.filter(query).distinct('id').order_by('-id').defer('comments')[sfrom:to]
    return returnItemList(obj, rtype)


@login_required
def getMarketItemCount(request,rtype):
    query = createQuery(request)
    obj = market.models.MarketItem.objects.filter(query).distinct('id').order_by('-id').count()
    return  HttpResponse(json.dumps({ 'success' : True, 'count': obj}),mimetype="application"+rtype)


@login_required
def editMarketItem(request,obj_id,rtype):
    obj = get_object_or_404(market.models.MarketItem.objects.defer('comments'),pk=obj_id)
    form = item_forms[obj.item_type](request.POST, instance=obj)
    if form.is_valid():
        saveMarketItem(form, obj.item_type, obj.owner)
    else:
        return HttpResponseError(json.dumps(get_validation_errors(form)), mimetype="application/"+rtype)
    return HttpResponse(json.dumps({ 'success' : True}),mimetype="application"+rtype)


@login_required
def deleteMarketItem(request,obj_id,rtype):
    pass


@login_required
def userMarketItems(request, rtype):
    obj = market.models.MarketItem.objects.defer('comments').filter(owner=request.user).all()
    return returnItemList(obj, rtype)


@login_required
def userMarketItemsCount(request,rtype):
    query = createQuery(request)
    obj = market.models.MarketItem.objects.filter(owner=request.user).filter(query).distinct('id').order_by('-id').count()
    return  HttpResponse(json.dumps({ 'success' : True, 'count': obj}),mimetype="application"+rtype)


@login_required
def getUserMarketItemFromTo(request,sfrom,to,rtype):
    query = createQuery(request)
    obj = market.models.MarketItem.objects.filter(owner=request.user).filter(query).distinct('id').order_by('-id').defer('comments')[sfrom:to]
    return returnItemList(obj, rtype)

