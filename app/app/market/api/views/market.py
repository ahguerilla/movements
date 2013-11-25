import json

from app.market.api.utils import *
import app.market as market
from app.market.forms import item_forms,saveMarketItem
import app.users as users
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404,render_to_response, RequestContext
from django.db.models import Q,Count,Avg


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
    if request.GET.has_key('skills'):        
        query = Q(skills__in= request.GET.getlist('skills')) 

    if request.GET.has_key('countries'):        
        query = query | Q(countries__in = request.GET.getlist('countries'))
    
    if request.GET.has_key('issues'):        
        query = query | Q(issues__in=request.GET.getlist('issues'))
    query = query & Q(published=True)
    return query


def addMarketItem(request, obj_type, rtype):
    form = item_forms[obj_type](request.POST)
    if form.is_valid():
        obj = saveMarketItem(form, obj_type, request.user)
    else:
        return HttpResponseError(json.dumps(get_validation_errors(form)), mimetype="application"+rtype)
    return HttpResponse(json.dumps({ 'success' : True, 'pk':obj.id}),mimetype="application"+rtype)


def getMarketItem(request,obj_id,rtype):
    obj = get_object_or_404(market.models.MarketItem.objects.defer('comments'), pk=obj_id)
    return returnItemList([obj], rtype)


def getMarketItemLast(request,count,rtype):
    obj = market.models.MarketItem.objects.order_by('pub_date').defer('comments')[:count]
    return returnItemList(obj, rtype)


def getMarketItemFromTo(request,sfrom,to,rtype):    
    if request.GET.has_key('skills'):        
        query = Q(skills__in= request.GET.getlist('skills')) 

    if request.GET.has_key('countries'):        
        query = query | Q(countries__in = request.GET.getlist('countries'))
    
    if request.GET.has_key('issues'):        
        query = query | Q(issues__in=request.GET.getlist('issues'))
    query = query & Q(published=True)
        
    #obj = market.models.MarketItem.objects\
        #.filter(query)\
        #.annotate(num_skills=Count('skills'))\
        #.annotate(num_issues=Count('issues'))\
        #.annotate(num_countries=Count('countries'))\
        #.defer('comments')[sfrom:to]
    
    #.extra(select={'numsum':'Count(market_marketitem_skills) + Count(market_marketitem_issues) + Count(market_marketitem_countries)'},
                                   #order_by=('numsum',))\    
                                   
    qset =  market.models.MarketItem.objects.filter(query).distinct('id').order_by('id','pub_date').defer('comments')
    qset.count()
    obj = qset[sfrom:to]
    return returnItemList(obj, rtype)


def getMarketItemCount(request,rtype):
    query = createQuery(request)
    obj = market.models.MarketItem.objects.filter(query).distinct('id').order_by('id','pub_date').count()
    return  HttpResponse(json.dumps({ 'success' : True, 'count': obj}),mimetype="application"+rtype)

    
def editMarketItem(request,obj_id,rtype):
    obj = get_object_or_404(market.models.MarketItem.objects.defer('comments'),pk=obj_id)
    form = item_forms[obj.item_type](request.POST, instance=obj)
    if form.is_valid():
        saveMarketItem(form, obj.item_type, obj.owner)
    else:
        return HttpResponseError(json.dumps(get_validation_errors(form)), mimetype="application/"+rtype)
    return HttpResponse(json.dumps({ 'success' : True}),mimetype="application"+rtype)


def deleteMarketItem(request,obj_id,rtype):
    pass


def userMarketItems(request, rtype):
    obj = market.models.MarketItem.objects.defer('comments').filter(owner=request.user).all()
    return returnItemList(obj, rtype)
