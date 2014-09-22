from __future__ import absolute_import

from django.utils import timezone
import logging

from django.db.models import Q
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

import constance
from app.users.models import UserProfile
from postman.models import Message


logger = logging.getLogger('private_message_reminder')


def send_unread_messages_notification_email(profile, number_unread):

    template_args = {
        'number_unread': number_unread,
        'base_url': settings.BASE_URL,
    }
    message = render_to_string('emails/unread_messages_email.html', template_args)
    email = EmailMessage(
        'You have unread messages on Movements.Org',
        message,
        constance.config.NO_REPLY_EMAIL,
        [profile.user.email]
    )
    email.content_subtype = "html"
    email.send()


class Command(BaseCommand):
    args = ''
    help = 'Runs the movements private_message_reminder process'

    def handle(self, *args, **options):

        logger.info('Running the private_message_reminder process')

        # For each user, send an email notifying of unread Messages if there are any.
        try:
            for profile in UserProfile.objects.all():
                number_unread = postman.models.Message.objects.inbox_unread_count(profile.user)
                if number_unread > 0:
                    send_unread_messages_notification_email(profile, number_unread)
        except Exception as ex:
            logger.exception(ex)

