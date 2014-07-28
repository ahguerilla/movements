import json
import re

from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
import constance
from django.http import Http404

from app.market.api.utils import *
from app.market.models import MarketItem, EmailRecommendation
from app import users


EMAILRE = re.compile("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$")


@login_required
def get_avatar(request, obj_id, size, rtype):
    user = get_object_or_404(users.models.User, pk=obj_id)
    obj = user.avatar_set.all()
    return HttpResponse(json.dumps({'pk': 0, 'avatar': reverse('avatar_render_primary', args=[user.username, size])}),
                        mimetype="application" + rtype)


@login_required
def send_message(request, to_user, rtype):
    try:
        market_item = None
        post_id = request.POST.get("post_id")
        if post_id:
            market_item = MarketItem.objects.get(pk=post_id)

        msg = pm_write(sender=request.user,
                       recipient=users.models.User.objects.filter(username=to_user)[0],
                       subject=request.POST['subject'],
                       body=request.POST['message'])

        if market_item:
            msg.messageext.market_item = market_item
            msg.messageext.save()

    except Exception, err:
        if err.message == 'value too long for type character varying(120)\n':
            message = "subject is too long (maximum 120 characters)"
        return HttpResponseError(
            json.dumps({'success': 'false', 'message': message}),
            mimetype="application/" + rtype)

    return HttpResponse(
        json.dumps({'success': 'true'}),
        mimetype="application/" + rtype)


@login_required
def send_recommendation(request, rec_type, obj_id, rtype):
    market_item = None
    if rec_type == 'item':
        market_item = MarketItem.objects.get(pk=obj_id)
        additionals = market_item.title
    else:
        additionals = obj_id

    recipients = re.split("\s*[;,]\s*", request.POST['recipients'])
    recipients = [x.strip() for x in recipients]
    badrecipients = []
    msgcontext = {'message': request.POST['message'],
                  'additionals': additionals,
                  'rec_type': rec_type,
                  'obj_id': obj_id,
                  'url': request.build_absolute_uri(reverse('show_post', args=[obj_id]))}

    subject = request.POST['subject']
    if len(subject) > 120: subject = subject[:120]
    body = render_to_string('emails/recommendmessage.txt', msgcontext)
    emlrecips = []

    for recipient in recipients:
        if len(recipient) > 0:
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
                    print "Exception sending to %s: %s %s:" % (recipient, type(e), e)
                    badrecipients.append(recipient + " (unknown user)")

    if len(emlrecips) > 0:
        context = {
            'message': request.POST['message'],
            'screen_name': request.user.username,
            'post_link': request.build_absolute_uri(reverse('show_post', args=[obj_id])),
            'post_title': market_item.title if market_item else '',
            'registration_link': request.build_absolute_uri(reverse('sign_up')),
            'post_date': market_item.pub_date if market_item else ''}
        try:
            email = EmailMessage(
                subject,
                render_to_string('emails/recommendation_message.html', context),
                constance.config.NO_REPLY_EMAIL,
                emlrecips
            )
            email.content_subtype = "html"
            email.send()
            _update_email_recommendations(market_item, emlrecips)
        except Exception as e:
            print "Exception sending to %s: %s %s:" % (recipient, type(e), e)
            badrecipients.extend(emlrecips)

    if len(badrecipients) > 0:
        return HttpResponse(
            json.dumps({'success': 'false',
                        'badrecipients': badrecipients}),
            mimetype="application/" + rtype)

    return HttpResponse(
        json.dumps({'success': 'true'}),
        mimetype="application/" + rtype)


def _update_email_recommendations(market_item, emails):
    EmailRecommendation.objects.bulk_create(
        [EmailRecommendation(market_item=market_item, email=email)
         for email in emails]
    )


@login_required
def set_rate(request, username, rtype):
    if not request.POST.has_key('score'):
        return HttpResponseError()
    user = users.models.User.objects.filter(username=username)[0]
    owner = request.user
    rate = users.models.UserRate.objects.filter(owner=owner).filter(user=user)
    if len(rate) == 0:
        rate = users.models.UserRate(owner=owner, user=user)
    else:
        rate = rate[0]
    rate.score = int(request.POST['score'])
    rate.save()
    rate.save_base()
    return HttpResponse(
        json.dumps({'success': 'true',
                    'score': round(user.userprofile.score, 1),
                    'ratecount': user.userprofile.ratecount
        }),
        mimetype="application/" + rtype)


@login_required
def get_usernames(request, rtype):
    usernames = users.models.User.objects \
                    .filter(is_active=True) \
                    .filter(username__icontains=request.GET['username']) \
                    .filter(~Q(pk=request.user.id) & ~Q(username='admin')).only('username')[:10]
    return HttpResponse(
        json.dumps(
            [user.username for user in usernames if hasattr(user, 'userprofile')]
        ),
        mimetype="application/" + rtype)


def get_user_details(username):
    user = get_object_or_404(users.models.User, username=username)
    if not user.is_active:
        raise Http404
    try:
        user_profile = users.models.UserProfile.objects.get(user=user)
    except:
        raise Http404
    orate = users.models.OrganisationalRating.objects.filter(user=user).all()
    return (user, user_profile, orate)
