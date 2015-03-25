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
from app.models import NotificationPing
from app.users.models import UserProfile
from app.market.models.notification import Notification


logger = logging.getLogger('notifications')


def send_user_notification_email(profile, items, set_last_notification_date=True):
    if set_last_notification_date:
        profile.last_notification_email = timezone.now()
    profile.save()
    if not items:
        return

    notifs_to_include = []
    items_already_mentioned = []
    for notif in items:
        add_to_list = True
        if notif.item is not None and notif.item.closed_date is not None:
            # Post has been closed
            add_to_list = False
        elif notif.comment is not None and notif.comment.deleted:
            # Comment has been deleted
            add_to_list = False
        if add_to_list:
            if notif.item not in items_already_mentioned:
                items_already_mentioned.append(notif.item)
                notifs_to_include.append(notif)

    if not notifs_to_include:
        return

    template_args = {
        'notifications': notifs_to_include,
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
        direct_message_check_seconds = 1
        full_check_seconds = 600
        seconds_since_full_check = full_check_seconds
        while True:
            logger.info('Running the notification process')

            try:
                for ping in NotificationPing.objects.filter(completed=None):
                    email = EmailMessage(
                        'Notification ping',
                        'This is the requested notification ping',
                        constance.config.NO_REPLY_EMAIL,
                        [ping.send_email_to]
                    )
                    email.send()
                    ping.completed = timezone.now()
                    ping.save()
            except Exception as ex:
                logger.exception(ex)

            # For each user, send an email notifying of Direct Messages if there are any (every 1 second).
            try:
                for profile in UserProfile.objects.all():
                    if profile.notification_frequency == UserProfile.NOTIFICATION_FREQUENCY.NEVER:
                        Notification.objects.filter(user=profile.user, emailed=False).update(emailed=True)
                    else:
                        items = Notification.objects.filter(valid_item).filter(user=profile.user, emailed=False, text__contains='''message''')
                        send_user_notification_email(profile, items, set_last_notification_date=False)
                        items.update(emailed=True)
            except Exception as ex:
                logger.exception(ex)

            # Check for all other notifications every 10 minutes.
            if seconds_since_full_check >= full_check_seconds:
                seconds_since_full_check = 0
                notification_delay_time = timezone.now() + relativedelta(minutes=-10)
                a_day_ago = timezone.now() + relativedelta(days=-1)
                a_week_ago = timezone.now() + relativedelta(days=-7)
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
                            items = Notification.objects.filter(valid_item).filter(user=profile.user, emailed=False, pub_date__lt=notification_delay_time)
                            send_user_notification_email(profile, items)
                            items.update(emailed=True)
                except Exception as ex:
                    logger.exception(ex)
            else:
                seconds_since_full_check += direct_message_check_seconds

            time.sleep(direct_message_check_seconds)
