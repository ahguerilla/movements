import json

from app.market.api.utils import *
import app.market as market
from app.market.forms import item_forms,saveMarketItem
import app.users as users
from django.core import serializers
from django.db.models import Q,Count,Avg
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404,render_to_response, RequestContext
from django.core.urlresolvers import reverse
from haystack.query import SearchQuerySet
import avatar
from django.contrib.auth.decorators import login_required
from postman.api import pm_write


def getUserDict(userprofile):
    adict= {'fields':{}}
    adict['pk'] = userprofile.user.id
    adict['fields']['avatar'] = '/static/images/male200.png'
    #reverse('avatar_render_primary', args=[userprofile.user.username,80])
    adict['fields']['bio'] = userprofile.bio
    adict['fields']['tag_line'] = userprofile.tag_ling
    adict['fields']['username'] = userprofile.user.username
    adict['fields']['ratecount'] = userprofile.ratecount
    adict['fields']['score'] = userprofile.score
    adict['fields']['profile_url'] = reverse('user_profile_for_user', args=[userprofile.user.username])
    adict['fields']['issues']= [ob.id for ob in userprofile.issues.all()]
    adict['fields']['countries']= [ob.id for ob in userprofile.countries.all()]
    adict['fields']['skills']= [ob.id for ob in userprofile.skills.all()]
    return adict


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
    query = Q()
    if request.GET.has_key('skills'):
        query = Q(skills__in= request.GET.getlist('skills'))

    if request.GET.has_key('countries'):
        query = query | Q(countries__in = request.GET.getlist('countries'))

    if request.GET.has_key('issues'):
        query = query | Q(issues__in=request.GET.getlist('issues'))

    if request.GET.has_key('search') and request.GET['search']!='':
        objs = SearchQuerySet().models(users.models.UserProfile).filter(text=request.GET['search'])
        #ids= [int(obj.pk) for obj in objs]
        ids= [int(obj.pk) if not obj.object.notperm.has_key('bio') else None for obj in objs]
        try:
            ids.remove(None)
        except:
            pass
        query = query & Q(id__in = ids)

    return query


@login_required
def getAvatar(request,obj_id, rtype):
    user = get_object_or_404(users.models.User, pk=obj_id)
    obj = user.avatar_set.all()
    #if obj != []:
        #return HttpResponse(value(rtype,obj),mimetype="application"+rtype)
    return HttpResponse(value(rtype, [{'pk': 0, 'avatar': '/static/images/male200.png' },]),mimetype="application"+rtype)


@login_required
def getDetails(request,obj_id, rtype):
    user = get_object_or_404(users.models.User, pk=obj_id)
    return HttpResponse(
        value(rtype,
              [user],
              fields=('username',)
              ),
        mimetype="application"+rtype)


@login_required
def getUsersFromto(request,sfrom,to,rtype):
    query = createQuery(request)
    obj = users.models.UserProfile.get_application_users(query=query, distinct='id', order='-id', start=sfrom, finish=to)
    return HttpResponse(
        json.dumps([getUserDict(user) for user in obj]),
        mimetype="application/"+rtype)


@login_required
def getUserCount(request,rtype):
    query = createQuery(request)
    obj = users.models.UserProfile.get_application_users(query=query, distinct='id', order='-id').count()
    return  HttpResponse(json.dumps({ 'success' : True, 'count': obj}),mimetype="application"+rtype)


@login_required
def sendMessage(request,to_user,rtype):
    try:
        pm_write(sender=request.user,
                 recipient=users.models.User.objects.filter(username=to_user)[0],
                 subject=request.POST['subject'],
                 body=request.POST['message'])
    except:
        return HttpResponseError(
            json.dumps({'success': 'false'}),
            mimetype="application/"+rtype)

    return HttpResponse(
        json.dumps({'success': 'true'}),
        mimetype="application/"+rtype)


@login_required
def setRate(request,username,rtype):
    if not request.POST.has_key('score'):
        return HttpResponseError()
    user = users.models.User.objects.filter(username=username)[0]
    owner = request.user
    rate = users.models.UserRate.objects.filter(owner=owner).filter(user=user)
    if len(rate)==0:
        rate = users.models.UserRate(owner=owner,user=user)
    else:
        rate = rate[0]
    rate.score =  int(request.POST['score'])
    rate.save()
    rate.save_base()
    return HttpResponse(
        json.dumps({'success': 'true',
                    'score':user.userprofile.score ,
                    'ratecount':user.userprofile.ratecount
                    }),
        mimetype="application/"+rtype)


@login_required
def getUsernames(request,rtype):
    usernames = users.models.User.objects.filter(username__contains=request.GET['username']).filter(~Q(username='admin')).only('username')[:10]
    return HttpResponse(
        json.dumps(
            [user.username for user in usernames]
        ),
        mimetype="application/"+rtype)
