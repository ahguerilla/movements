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
import avatar
from django.utils.html import escape


def getMarketjson(objs):
    alist=[]
    for obj in objs:
        adict = {'fields':{}}
        adict['pk'] = obj.id
        adict['fields']['item_type'] = obj.item_type
        adict['fields']['issues']= [ob.id for ob in obj.issues.all()]
        adict['fields']['countries']= [ob.id for ob in obj.countries.all()]
        adict['fields']['skills']= [ob.id for ob in obj.skills.all()]
        adict['fields']['title']= obj.title
        adict['fields']['details']= obj.details
        adict['fields']['pub_date']= str(obj.pub_date)
        adict['fields']['exp_date']= str(obj.exp_date)
        adict['fields']['owner']= [obj.owner.username]
        adict['fields']['url']= obj.url
        adict['fields']['files']= [afile.url for afile in obj.files.all()]
        adict['fields']['commentcount']= obj.commentcount
        adict['fields']['usercore']= obj.owner.userprofile.score
        adict['fields']['userratecount']= obj.owner.userprofile.ratecount
        adict['fields']['ratecount']= obj.ratecount
        adict['fields']['score']= obj.score
        adict['fields']['avatar'] = '/static/images/male200.png'
        #reverse('avatar_render_primary', args=[obj.owner.username,80])

        alist.append(adict)
    return json.dumps(alist)


def returnItemList(obj, rtype):
    #value(rtype,
          #obj,
          #use_natural_keys=True,
          #fields=('item_type',
                  #'issues',
                  #'countries',
                  #'skills',
                  #'title',
                  #'details',
                  #'pub_date',
                  #'exp_date',
                  #'owner',
                  #'url',
                  #'files',
                  #'commentcount')
          #)
    return HttpResponse(
        getMarketjson(obj),
        mimetype="application/"+rtype)


def createQuery(request):
    query = Q()
    if request.GET.has_key('skills'):
        query = query | Q(skills__in= request.GET.getlist('skills'))

    if request.GET.has_key('countries'):
        query = query | Q(countries__in = request.GET.getlist('countries'))

    if request.GET.has_key('issues'):
        query = query | Q(issues__in=request.GET.getlist('issues'))

    if request.GET.has_key('types'):
        query = query & Q(item_type__in=request.GET.getlist('types'))

    if request.GET.has_key('search') and request.GET['search']!='':
        objs = SearchQuerySet().models(market.models.MarketItem).filter(text=request.GET['search'])
        ids= [int(obj.pk) for obj in objs]
        query = query & Q(id__in = ids)
    query = query & Q(published=True)
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
    if request.user != obj.owner:
        return HttpResponseRedirect('/')
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


@login_required
def setRate(request,obj_id,rtype):
    if not request.POST.has_key('score'):
        return HttpResponseError()
    item = market.models.MarketItem.objects.filter(id=obj_id)[0]
    owner = request.user
    rate = market.models.ItemRate.objects.filter(owner=owner).filter(item=item)
    if len(rate)==0:
        rate = market.models.ItemRate(owner=owner,item=item)
    else:
        rate = rate[0]
    rate.score =  int(request.POST['score'])
    rate.save()
    rate.save_base()
    return HttpResponse(
        json.dumps({'success': 'true',
                    'score':item.score ,
                    'ratecount':item.ratecount
                    }),
        mimetype="application/"+rtype)
