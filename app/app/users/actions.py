import re

from django.conf import settings
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse

from models import UserProfile
from app.market.models import MarketItem

import constance


def check_user_notification_settings(user, group):
    profile = UserProfile.objects.get(user=user)
    return profile.receives_group_mail(group.id)


def check_user_type(user, user_type):
    if user_type == 'all':
        return True
    profile = UserProfile.objects.get(user=user)
    if user_type == 'requesters':
        return profile.is_requester()
    if user_type == 'providers':
        return profile.is_provider()
    return False


def construct_email(message, user, group):
    full_name = (user.first_name + u' ' + user.last_name).strip()
    full_name = full_name if full_name else u'Movements.Org user'
    first_name = user.first_name.strip()
    first_name = first_name if first_name else u'Movements.Org user'
    last_name = user.last_name.strip()
    message = message.replace(u'##FULL_NAME##', full_name)
    message = message.replace(u'##FIRST_NAME##', first_name)
    message = message.replace(u'##LAST_NAME##', last_name)
    profile = UserProfile.objects.get(user=user)
    posts_matched = re.findall(r'##POST_ID=\d+##', message)
    for post in posts_matched:
        post_id = post.split(u'=')[1][:-2]
        try:
            MarketItem.objects.get(pk=post_id)
        except ObjectDoesNotExist:
            raise ValueError("Invalid post id specified {0}".format(post_id))
        url = settings.BASE_URL + reverse('show_post', args=[post_id])
        html_url = '<a href="' + url + '">' + url + '</a>'
        message = message.replace(post, html_url)
    template_args = {
        'base_url': settings.BASE_URL,
        'unsub_uuid': profile.get_unsubscribe_uuid(),
        'group_id': group.id,
        'group_name': group.name,
    }
    footer = render_to_string('emails/snippets/_group_email_notification_settings.html', template_args)
    message_parts = message.split(u'##NOTIFICATION_PREFERENCES##')
    message_list = []
    for m in message_parts:
        paragraphs_list = []
        paragraphs = m.split('\n')
        for p in paragraphs:
            p = p.strip()
            if p:
                paragraphs_list.append('<p>' + p + '</p>')
        message_list.append('\n'.join(paragraphs_list))

    message = ''
    first = True
    for i in message_list:
        if not first:
            message += '\n' + footer + '\n'
        first = False
        message += '\n' + i + '\n'
    return message


def send_group_email(message, user, email_to=''):
    to_address = email_to if email_to else user.email
    email = EmailMessage(
        'Group message from Movements.Org',
        message,
        constance.config.NO_REPLY_EMAIL,
        [to_address]
    )
    email.content_subtype = "html"
    email.send()
