from __future__ import absolute_import

from django.utils import timezone
from dateutil.relativedelta import relativedelta
import logging
import time

from django.db.models import Q
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

import constance
from app.users.models import UserProfile
from app.market.models.notification import Notification


logger = logging.getLogger('notifications')


def send_user_notification_email(profile, items):
    profile.last_notification_email = timezone.now()
    profile.save()
    if not items:
        return
    template_args = {
        'notifications': items,
        'base_url': settings.BASE_URL,
    }
    message = render_to_string('emails/notification_email.html', template_args)
    email = EmailMessage(
        'You have new notifications on Movements.Org',
        message,
        constance.config.NO_REPLY_EMAIL,
        [profile.user.email]
    )
    email.content_subtype = "html"
    email.send()


class Command(BaseCommand):
    args = ''
    help = 'Runs the movements notifications process'

    def handle(self, *args, **options):
        valid_item = Q(item__deleted=False) | Q(item=None)
        a_day_ago = timezone.now() + relativedelta(days=-1)
        a_week_ago = timezone.now() + relativedelta(days=-7)
        while True:
            logger.info('Running the notification process')
            try:
                # Very simple notification implementation, might need to be made more efficient
                # - for each user
                #   - check if it's time to send an email to user
                #   - sends email if it is
                for profile in UserProfile.objects.all():
                    send_email = False
                    if profile.notification_frequency == UserProfile.NOTIFICATION_FREQUENCY.NEVER:
                        Notification.objects.filter(user=profile.user, emailed=False).update(emailed=True)
                    elif profile.notification_frequency == UserProfile.NOTIFICATION_FREQUENCY.INSTANTLY or profile.last_notification_email is None:
                        send_email = True
                    elif profile.notification_frequency == UserProfile.NOTIFICATION_FREQUENCY.DAILY:
                        send_email = profile.last_notification_email < a_day_ago
                    elif profile.notification_frequency == UserProfile.NOTIFICATION_FREQUENCY.WEEKLY:
                        send_email = profile.last_notification_email < a_week_ago
                    if send_email:
                        items = Notification.objects.filter(valid_item).filter(user=profile.user, emailed=False)
                        send_user_notification_email(profile, items)
                        items.update(emailed=True)
            except Exception as ex:
                logger.exception(ex)
            time.sleep(1)
