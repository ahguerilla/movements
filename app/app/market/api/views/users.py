import json
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from haystack.query import SearchQuerySet
from django.contrib.auth.decorators import login_required
from postman.api import pm_write

from app.market.api.utils import *
import app.users as users


def create_query(request):
    query = Q()

    if request.GET.has_key('skills'):
        query = Q(skills__in=request.GET.getlist('skills'))

    if request.GET.has_key('countries'):
        query = query | Q(countries__in=request.GET.getlist('countries'))

    if request.GET.has_key('issues'):
        query = query | Q(issues__in=request.GET.getlist('issues'))

    if request.GET.has_key('search') and request.GET['search']!='':        
        search_q = request.GET['search']
        
        ids = SearchQuerySet().models(users.models.UserProfile).\
            filter(Q(nationality__contains=search_q)|
                   Q(resident_country__contains=search_q)|
                   Q(tag_ling__contains=search_q)|
                   Q(expertise__contains=search_q)|
                   Q(bio__contains=search_q)|
                   Q(username__contains=search_q)|
                   Q(text__contains=search_q)|
                   Q(occupation__contains=search_q)                                                                        
                   ).values_list('pk', flat=True)                                
        
        if None in ids:
            ids.remove(None)
        
        ids = [int(id) for id in ids]
        
        if request.user.userprofile.id in ids:
            ids.remove(request.user.userprofile.id)
        
        query = query & Q(id__in = ids)

    if request.GET.has_key('types'):
        query = query & Q(user__marketitem__item_type__in=request.GET.getlist('types'))

    return query & ~Q(user__id=request.user.id)


@login_required
def get_avatar(request,obj_id,size, rtype):
    user = get_object_or_404(users.models.User, pk=obj_id)
    obj = user.avatar_set.all()
    #if obj != []:
        #return HttpResponse(value(rtype,obj),mimetype="application"+rtype)
    return HttpResponse( json.dumps({'pk': 0, 'avatar': reverse('avatar_render_primary', args=[user.username,size])}),mimetype="application"+rtype)


@login_required
def get_details(request,obj_id, rtype):
    user = get_object_or_404(users.models.User, pk=obj_id)
    return HttpResponse(
        value(rtype,
              [user],
              fields=('username',)
              ),
        mimetype="application"+rtype)


@login_required
def get_users_fromto(request,sfrom,to,rtype):
    query = create_query(request)
    obj = users.models.UserProfile.get_application_users(query=query,
                                                         distinct='id',
                                                         order='-id',
                                                         start=sfrom,
                                                         finish=to)
    return HttpResponse(
        json.dumps([user.getDict() for user in obj]),
        mimetype="application/"+rtype)


@login_required
def get_user_count(request,rtype):
    query = create_query(request)
    obj = users.models.UserProfile.get_application_users(query=query, distinct='id', order='-id').count()
    return  HttpResponse(json.dumps({ 'success' : True, 'count': obj}),mimetype="application"+rtype)


@login_required
def send_message(request,to_user,rtype):
    try:
        pm_write(sender=request.user,
                 recipient=users.models.User.objects.filter(username=to_user)[0],
                 subject=request.POST['subject'],
                 body=request.POST['message'])
    except Exception,err:
        if err.message== 'value too long for type character varying(120)\n':
            message= "subject is too long (maximum 120 characters)"
        return HttpResponseError(
            json.dumps({'success': 'false','message':message}),
            mimetype="application/"+rtype)

    return HttpResponse(
        json.dumps({'success': 'true'}),
        mimetype="application/"+rtype)


@login_required
def send_recommendation(request,rec_type,to_user,obj_id,rtype):
    if rec_type == 'item':
        href = '<!--item="'+obj_id+'"-->'
    else:
        href = '<!--user="'+obj_id+'"-->'
    try:
        pm_write(sender=request.user,
                 recipient=users.models.User.objects.filter(username=to_user)[0],
                 subject=request.POST['subject'],
                 body=request.POST['message']+'\r\n'+href)
    except:
        return HttpResponseError(
            json.dumps({'success': 'false'}),
            mimetype="application/"+rtype)

    return HttpResponse(
        json.dumps({'success': 'true'}),
        mimetype="application/"+rtype)


@login_required
def set_rate(request,username,rtype):
    if not request.POST.has_key('score'):
        return HttpResponseError()
    user = users.models.User.objects.filter(username=username)[0]
    owner = request.user
    rate = users.models.UserRate.objects.filter(owner=owner).filter(user=user)
    if len(rate) == 0:
        rate = users.models.UserRate(owner=owner,user=user)
    else:
        rate = rate[0]
    rate.score = int(request.POST['score'])
    rate.save()
    rate.save_base()
    return HttpResponse(
        json.dumps({'success': 'true',
                    'score':user.userprofile.score ,
                    'ratecount':user.userprofile.ratecount
                    }),
        mimetype="application/"+rtype)


@login_required
def get_usernames(request,rtype):
    usernames = users.models.User.objects \
                        .filter(is_active=True)\
                        .filter(username__icontains=request.GET['username']) \
                        .filter(~Q(pk=request.user.id)&~Q(username='admin')).only('username')[:10]
    return HttpResponse(
        json.dumps(
            [user.username for user in usernames if hasattr(user, 'userprofile')]
        ),
        mimetype="application/"+rtype)
