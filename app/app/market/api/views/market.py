import json

from app.market.api.utils import *
import app.market as market
from app.market.forms import item_forms, saveMarketItem
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
from tasks.celerytasks import create_notification, update_notifications, mark_read_notifications, add_view
import constance
import requests
from django.conf import settings
from django.utils.cache import get_cache_key, get_cache
from django.db import connection
cache = get_cache('default')
items_cache = get_cache('items')
user_items_cache = get_cache('user_items')


def get_market_json(objs, request=None):
    alist = []
    for obj in objs:
        alist.append(obj.getdict(request))
    return json.dumps(alist)


def return_item_list(obj, rtype, request=None):
    return HttpResponse(
        get_market_json(obj, request),
        mimetype="application/"+rtype)



@login_required
def add_market_item(request, obj_type, rtype):
    form = item_forms[obj_type](request.POST)
    if form.is_valid():
        obj = saveMarketItem(form, obj_type, request.user)
        create_notification.delay(obj)
        items_cache.clear()
        user_items_cache.clear()
    else:
        return HttpResponseError(json.dumps(get_validation_errors(form)), mimetype="application"+rtype)
    return HttpResponse(json.dumps({ 'success' : True, 'pk':obj.id}),mimetype="application"+rtype)


@login_required
def get_market_item(request, obj_id, rtype):
    retval = cache.get('item-' + obj_id)
    if retval:
        mark_read_notifications.delay((obj_id,),request.user.id)
        return retval
    obj = get_object_or_404(market.models.MarketItem.objects.defer('comments'),
                            Q(exp_date__gte=datetime.now())|Q(never_exp=True),
                            pk=obj_id,
                            deleted=False,
                            owner__is_active=True)
    add_view.delay(obj_id, obj.owner.id, request.user.id)
    mark_read_notifications.delay((obj.id,),request.user.id)
    retval = return_item_list([obj], rtype)
    cache.add('item-' + obj_id, retval)
    return retval


def getStikies(request, hiddens, sfrom, to):
    sticky_objs = market.models.MarketItemStick.objects.filter(viewer_id=request.user.id)
    if request.GET.get('showHidden', 'false') == 'false':
        sticky_objs  = sticky_objs .filter(~Q(item_id__in=hiddens))
    if request.GET.has_key('types'):
        sticky_objs  = sticky_objs.filter(Q(item__item_type__in=request.GET.getlist('types')))
    sticky_objs = sticky_objs[sfrom:to]
    obj = [i.item for i in sticky_objs]
    return obj


def get_raw(request):
    issues = (0,)
    countries = (0,)
    skills = (0,)
    types = "('offer', 'request')"
    ids= ""
    show_hidden = ""

    if request.GET.has_key('issues'):
        issues = tuple(map(int,request.GET.getlist('issues')))

    if request.GET.has_key('skills'):
        skills = tuple(map(int,request.GET.getlist('skills')))

    if request.GET.has_key('countries'):
        countries = tuple(map(int,request.GET.getlist('countries')))

    if request.GET.has_key('types') and len(request.GET.getlist('types'))>0:
        _req_types = tuple(str(item) for item in request.GET.getlist('types'))
        types = ("%s"%(_req_types,) if len(_req_types)>1 else "('%s')"%(_req_types))

    if request.GET.has_key('search') and request.GET['search']!='':
        objs = SearchQuerySet().models(market.models.MarketItem).filter(text=request.GET['search'])
        _ids= tuple(int(obj.pk) for obj in objs)
        if len(_ids)>0:
            ids = 'AND "market_marketitem"."id" IN '+ ("%s"%(_ids,) if len(_ids)>1 else "(%s)"%(_ids))

    if request.GET.get('showHidden', 'false') == 'false':
        show_hidden = 'AND NOT ("market_marketitem"."id" IN \
                        (SELECT hiddens."item_id" FROM "market_marketitemhidden" hiddens WHERE hiddens."viewer_id" = \
                        '+str(request.user.id)+'))'

    raw = """
       select market_marketitem.*, (counted_matches.i_sum+counted_matches.c_sum+counted_matches.s_sum) as tag_matches
       FROM (select id,
       count(distinct match_countries)as c_sum,
       count(distinct match_issues) as i_sum,
       count(distinct match_skills) as s_sum
       FROM (select market_marketitem.id ,
       market_marketitem_countries.countries_id as match_countries,
       market_marketitem_issues.issues_id as match_issues,
       market_marketitem_skills.skills_id as match_skills
       FROM market_marketitem
       left outer join market_marketitem_skills on market_marketitem_skills.marketitem_id = market_marketitem.id and market_marketitem_skills.skills_id IN
       """+ ("%s"%(skills,) if len(skills)>1 else "(%s)"%(skills)) + """
       left outer join market_marketitem_countries on market_marketitem_countries.marketitem_id = market_marketitem.id and market_marketitem_countries.countries_id IN
       """+ ("%s"%(countries,) if len(countries)>1 else "(%s)"%(countries)) + """
       left outer join market_marketitem_issues on market_marketitem_issues.marketitem_id = market_marketitem.id and market_marketitem_issues.issues_id IN
       """+ ("%s"%(issues,) if len(issues)>1 else "(%s)"%(issues)) + """
       )as item_countries_issues_skills group by id
       ) as counted_matches
       join market_marketitem on market_marketitem.id = counted_matches.id
       INNER JOIN "auth_user" ON ( "market_marketitem"."owner_id" = "auth_user"."id" ) WHERE ("market_marketitem"."item_type" IN
       """+ types + """
       """+ ids +"""
       """+ show_hidden +"""
       AND NOT ("market_marketitem"."id" IN
       (SELECT stickies."item_id" FROM "market_marketitemstick" stickies WHERE stickies."viewer_id" =
       """+str(request.user.id)+"""
       )) AND "market_marketitem"."published" = True  AND "market_marketitem"."deleted" = False  AND "auth_user"."is_active" = True AND ("market_marketitem"."exp_date" >=
       '"""+str(datetime.now())+"""'
       OR "market_marketitem"."never_exp" = True )  )
       order by tag_matches desc, pub_date desc
       """
    return raw


@login_required
def get_marketItem_fromto(request, sfrom, to, rtype):
    reqhash = hash(request.path+str(request.GET))
    retval = items_cache.get(reqhash)
    if retval:
        return retval

    query = market.models.MarketItem.objects.raw(get_raw(request))
    stickys = market.models.MarketItemStick.objects.filter(viewer_id=request.user.id).count()
    hiddens = market.models.MarketItemHidden.objects.values_list('item_id', flat=True).filter(viewer_id=request.user.id)
    if stickys >= int(to):
        obj = getStikies(request, hiddens, sfrom, to)
    elif stickys <= int(sfrom):
        obj = query[int(sfrom)-stickys:int(to)-stickys]
    elif stickys >= int(sfrom) and stickys <= int(to):
        sticky_objs = getStikies(request, hiddens, sfrom, stickys)
        market_objs = query[0:(int(to)-stickys)]
        obj = list(sticky_objs)
        b = list(market_objs)
        obj.extend(b)
    retval = return_item_list(obj, rtype, request)
    items_cache.add(reqhash, retval)
    return retval


@login_required
@check_perms_and_get(market.models.MarketItem)
def edit_market_item(request,obj_id,rtype):
    cache.delete('item-'+obj_id)
    cache.delete('translation-'+obj_id)
    items_cache.clear()
    user_items_cache.clear()
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
    user_items_cache.clear()
    items_cache.clear()
    obj=request.obj
    obj.deleted = True
    obj.save()
    return HttpResponse(json.dumps({ 'success' : True}),
                        mimetype="application"+rtype)


@login_required
@check_perms_and_get(market.models.MarketItem)
def user_get_marketitem(request, obj_id, rtype):
    return return_item_list([request.obj], rtype)


@login_required
def get_user_marketitem_fromto(request, sfrom, to, rtype):
    reqhash = hash(request.path+str(request.GET))
    retval = user_items_cache.get(reqhash)
    if retval:
        return retval
    query = create_query(request)
    obj = market.models.MarketItem.objects.filter(owner=request.user).filter(query).distinct('id').order_by('-id').defer('comments')[sfrom:to]
    retval = return_item_list(obj, rtype)
    user_items_cache.add(reqhash, retval)
    return retval


@login_required
def get_item_translation(request, obj_id, rtype):
    retval = cache.get('translation-' + obj_id)
    if retval:
        return retval
    obj = get_object_or_404(market.models.MarketItem.objects.defer('comments'),
                            Q(exp_date__gte=datetime.now())|Q(never_exp=True),
                            pk=obj_id,
                            deleted=False,
                            owner__is_active=True)
    resp = requests.get(settings.GOOGLE_TRANS_URL+'key='+constance.config.GOOGLE_API_KEY+'&source=ar&target='+'en'+'&q='+obj.details)
    retval = return_item_list([obj], rtype)
    cache.add('translation-' + obj_id, retval)
    return retval


@login_required
def set_rate(request, obj_id, rtype):
    if not request.POST.has_key('score'):
        return HttpResponseError()
    cache.delete('item-'+obj_id)
    items_cache.clear()
    user_items_cache.clear()
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
def get_notifications_fromto(request, sfrom, to, rtype):
    notifications = market.models.Notification.objects.filter(user=request.user.id, item__deleted=False)[sfrom:to]
    alist=[]
    notification_ids=[]
    for notification in notifications:
        alist.append(notification.getDict())
        notification_ids.append(notification.id)
    market.models.Notification.objects.filter(id__in=notification_ids).update(seen=True)
    return HttpResponse(json.dumps({'notifications':alist}),
                        mimetype="application"+rtype)


@login_required
def get_notseen_notifications(request, sfrom, to, rtype):
    notifications = market.models.Notification.objects.filter(user=request.user.id,item__deleted=False).filter(seen=False).only('seen')
    if len(notifications)>0:
        return HttpResponse(json.dumps({'result':True}),
                            mimetype="application"+rtype)
    return  HttpResponse(json.dumps({'result':False}),
                         mimetype="application"+rtype)


@login_required
def get_views_count(request, obj_id, rtype):
    views = market.models.MarketItemViewConter.objects.filter(item_id=obj_id).count()
    return  HttpResponse(json.dumps({'result': views}),
                         mimetype="application"+rtype)


@login_required
def hide_item(request, obj_id, rtype):
    new_hidden = market.models.MarketItemHidden.objects.get_or_create(viewer_id=request.user.id, item_id=obj_id)[0]
    new_hidden.save()
    return  HttpResponse(json.dumps({'result': True}),
                         mimetype="application"+rtype)


@login_required
def unhide_item(request, obj_id, rtype):
    result = False
    hidden = market.models.MarketItemHidden.objects.get(viewer_id=request.user.id, item_id=obj_id)
    if hidden:
        hidden.delete()
        result = True
    return  HttpResponse(json.dumps({'result': result}),
                         mimetype="application"+rtype)


@login_required
def stick_item(request, obj_id, rtype):
    new_sticky = market.models.MarketItemStick.objects.get_or_create(viewer_id=request.user.id, item_id=obj_id)[0]
    new_sticky.save()
    return  HttpResponse(json.dumps({'result': True}),
                         mimetype="application"+rtype)


@login_required
def unstick_item(request, obj_id, rtype):
    result = False
    sticky = market.models.MarketItemStick.objects.get(viewer_id=request.user.id, item_id=obj_id)
    if sticky:
        sticky.delete()
        result = True
    return  HttpResponse(json.dumps({'result': result}),
                         mimetype="application"+rtype)