import json
import re

from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.cache import get_cache
import constance
from haystack.query import SearchQuerySet

from app.market.api.utils import *
from app.market.models import MarketItem, EmailRecommendation
from app import users


cache = get_cache('default')

EMAILRE = re.compile("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$")

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
        if len(request.GET.getlist('types'))<2:
            query = query & Q(user__marketitem__item_type__in=request.GET.getlist('types'))

    return query & ~Q(user__id=request.user.id)


@login_required
def get_avatar(request, obj_id, size, rtype):
    user = get_object_or_404(users.models.User, pk=obj_id)
    obj = user.avatar_set.all()
    return HttpResponse( json.dumps({'pk': 0, 'avatar': reverse('avatar_render_primary', args=[user.username,size])}),mimetype="application"+rtype)



@login_required
def get_users_fromto(request, sfrom, to, rtype):
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
def send_message(request, to_user, rtype):
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
def send_recommendation(request, rec_type, obj_id, rtype):
    market_item = None
    if rec_type == 'item':
        market_item = MarketItem.objects.get(pk=obj_id)
        additionals = market_item.title
    else:
        additionals = obj_id

    recipients = re.split("\s*[ ;,]\s*", request.POST['recipients'])
    badrecipients = []
    msgcontext = { 'message'     : request.POST['message'],
                   'additionals' : additionals,
                   'rec_type'    : rec_type,
                   'obj_id'      : obj_id,
                   'url'         : request.build_absolute_uri(reverse('preview', args=(rec_type,obj_id)))}

    subject = request.POST['subject']
    if len(subject) > 120: subject = subject[:120]
    body    = render_to_string('emails/recommendmessage.txt',  msgcontext)
    emlrecips = []

    for recipient in recipients:
        if EMAILRE.match(recipient):
            emlrecips.append(recipient)
        else:
            try:
                msg = pm_write(
                    sender=request.user,
                    recipient=users.models.User.objects.filter(username=recipient)[0],
                    subject=subject,
                    body=body)
                if rec_type == 'item':
                    msg.messageext.is_post_recommendation = True
                    msg.messageext.market_item = market_item
                else:
                    msg.messageext.is_user_recommendation = True
                msg.messageext.save()
            except Exception as e:
                print "Exception sending to %s: %s %s:"%(recipient, type(e), e)
                badrecipients.append(recipient + " (unknown user)")

    if len(emlrecips) > 0:
        emlbody = render_to_string('emails/recommendmessage.eml', msgcontext)
        try:
            email = EmailMessage(
                subject,
                emlbody,
                constance.config.NO_REPLY_EMAIL,
                emlrecips
            )
            email.content_subtype = "plain"
            email.send()
            _update_email_recommendations(market_item, emlrecips)
        except Exception as e:
            print "Exception sending to %s: %s %s:"%(recipient, type(e), e)
            badrecipients.extend(emlrecips)

    if len(badrecipients) > 0:
        return HttpResponse(
            json.dumps({'success'       : 'false',
                        'badrecipients' : badrecipients}),
            mimetype="application/"+rtype)

    return HttpResponse(
        json.dumps({'success': 'true'}),
        mimetype="application/"+rtype)


def _update_email_recommendations(market_item, emails):
    EmailRecommendation.objects.bulk_create(
        [EmailRecommendation(market_item=market_item, email=email)
         for email in emails]
    )

@login_required
def set_rate(request, username, rtype):
    cache.clear()
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
                    'score':round(user.userprofile.score,1) ,
                    'ratecount':user.userprofile.ratecount
                    }),
        mimetype="application/"+rtype)


@login_required
def get_usernames(request, rtype):
    usernames = users.models.User.objects \
                        .filter(is_active=True)\
                        .filter(username__icontains=request.GET['username']) \
                        .filter(~Q(pk=request.user.id)&~Q(username='admin')).only('username')[:10]
    return HttpResponse(
        json.dumps(
            [user.username for user in usernames if hasattr(user, 'userprofile')]
        ),
        mimetype="application/"+rtype)


@login_required
def get_profile(request, username, rtype):
    user = get_object_or_404(users.models.User, username=username)
    if not user.is_active:
        raise Http404
    try:
        user_profile = users.models.UserProfile.objects.get(user=user)
    except:
        raise Http404
    orate = users.models.OrganisationalRating.objects.filter(user=user).all()
    perms = user_profile.notperm
    return HttpResponse(
        json.dumps(
            {
                'username': user.username,
                'avatar': reverse('avatar_render_primary', args=[user.username,60]),
                'nationality': user_profile.nationality.nationality if not perms.has_key('nationality') else 'hidden',
                'resident_country': user_profile.resident_country.residence if not perms.has_key('resident_country') else 'hidden',
                'score': round(user_profile.score,1),
                'ratecount': user_profile.ratecount,
                'orate': orate[0].rated_by_ahr if len(orate)>0 else 0
            }
            ),
        mimetype="application/"+rtype)

