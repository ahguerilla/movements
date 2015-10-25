import json
import re

from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import constance
from django.http import Http404

from app.market.api.utils import *
from app.market.models import MarketItem, EmailRecommendation, MarketItemCollaborators, MarketItemSalesforceRecord
from app.celerytasks import send_group_message
from app import users


EMAILRE = re.compile("^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")


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
                       body=request.POST['message'], truncate=True)

        if market_item:
            msg.messageext.market_item = market_item
            msg.messageext.save()

            market_collaborator = MarketItemCollaborators()
            market_collaborator.market_item_id = post_id
            market_collaborator.collaborator_id = request.user.id
            market_collaborator.interaction_type = "Message"
            market_collaborator.save()

            # Recalc new number of collaborators and store in market item.
            market_item.collaboratorcount = MarketItemCollaborators.objects.filter(market_item_id=post_id).values(
                "collaborator_id").distinct().count()
            market_item.save()

    except Exception, err:
        message = err.message if err else 'error sending message'
        if err.message == 'value too long for type character varying(120)\n':
            message = "subject is too long (maximum 120 characters)"
        return HttpResponseError(
            json.dumps({'success': 'false', 'message': message}),
            mimetype="application/" + rtype)

    return HttpResponse(
        json.dumps({'success': 'true'}),
        mimetype="application/" + rtype)


@login_required
def send_recommendation(request, obj_id, rtype):
    market_item = MarketItem.objects.get(pk=obj_id)
    MarketItemSalesforceRecord.mark_for_update(obj_id)

    recipients = re.split("\s*[;,]\s*", request.POST['recipients'])
    recipients = [x.strip() for x in recipients]
    bad_recipients = []
    msg_context = {'message': request.POST['message'],
                   'additionals': market_item.title,
                   'obj_id': obj_id,
                   'url': request.build_absolute_uri(reverse('show_post', args=[obj_id]))}

    subject = request.POST['subject']
    if len(subject) > 120:
        subject = subject[:120]
    body = render_to_string('emails/recommendmessage.txt', msg_context)
    email_recipients = []

    for recipient in recipients:
        if len(recipient) > 0:
            if EMAILRE.match(recipient):
                email_recipients.append(recipient)
            else:
                try:
                    msg = pm_write(
                        sender=request.user,
                        recipient=users.models.User.objects.filter(username=recipient)[0],
                        subject=subject,
                        body=body, truncate=True)
                    msg.messageext.is_post_recommendation = True
                    msg.messageext.market_item = market_item
                    msg.messageext.save()
                except:
                    bad_recipients.append(recipient + " (unknown user)")

    if len(email_recipients) > 0:
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
                email_recipients
            )
            email.content_subtype = "html"
            email.send()
            _update_email_recommendations(market_item, email_recipients)
        except:
            bad_recipients.extend(email_recipients)

    if request.user.is_staff:
        groups = re.split("\s*[;,]\s*", request.POST.get('groups', ''))
        groups = [g.strip() for g in groups]
        group_recipients = []
        for g in groups:
            if not g:
                continue
            try:
                group = Group.objects.get(name=g)
                group_recipients.append(group)
            except ObjectDoesNotExist:
                bad_recipients.append(g + " (unknown group)")

        if group_recipients:
            group_context = {
                'message': request.POST['message'],
                'screen_name': request.user.username,
                'post_link': request.build_absolute_uri(reverse('show_post', args=[obj_id])),
                'post_title': market_item.title if market_item else '',
                'post_date': market_item.pub_date if market_item else ''}
            group_filter = request.POST.get('groupFilter')
            group_message = render_to_string('emails/recommendation_group.txt', group_context)
            for g in group_recipients:
                send_group_message(group_message, g, user_type=group_filter, subject=subject)

    if len(bad_recipients) > 0:
        return HttpResponse(
            json.dumps({'success': 'false',
                        'badrecipients': bad_recipients}),
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


@staff_member_required
def get_group_names(request):
    groups = Group.objects.filter(name__icontains=request.GET.get('groupname')).only('name')[:10]
    return HttpResponse(
        json.dumps(
            [g.name for g in groups]
        ),
        mimetype="application/json")


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
