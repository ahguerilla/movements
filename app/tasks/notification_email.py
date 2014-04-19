from __future__ import absolute_import
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../','../','../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../','../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../','../','app')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings.local')

from datetime import datetime
from app.market.models import Notification
from django.core.mail import EmailMessage
import constance
from django.template.loader import render_to_string
from dateutil.relativedelta import *
from django.contrib.sites.models import Site


def create_notification_message(notifications, base_url):
    template_args = {
        'notifications': notifications,
        'base_url': base_url
    }
    return render_to_string('emails/notification_email.html', template_args)


def send_notification(notifications, base_url):
    messagebody = create_notification_message(notifications, base_url)
    mail = EmailMessage('Exchangivist Notification Email',
                        messagebody,
                        constance.config.NO_REPLY_EMAIL,
                        [notifications[0].user.email])
    mail.content_subtype = 'html'
    mail.send()


if __name__ == '__main__':
    base_url = 'https://%s' % Site.objects.all()[0]
    #from_date = datetime.now() + relativedelta(weekday=SU(-2), hour=0, minute=0, second=0, microsecond=0)
    #to_date = datetime.now() + relativedelta(weekday=SU(-1), hour=0, minute=0, second=0, microsecond=0)
    from_date = datetime.now() + relativedelta(days=-2, hour=0, minute=0, second=0, microsecond=0)
    to_date = datetime.now() + relativedelta(days=-1, hour=0, minute=0, second=0, microsecond=0)


    notifications = Notification.objects.\
        filter(user__userprofile__get_newsletter=True,
               pub_date__gte=from_date,
               pub_date__lt=to_date).\
        order_by('user','pub_date')
    user_notifications = []
    lastid = None
    for notification in notifications:
        if not lastid or notification.user.id == lastid:
            user_notifications.append(notification)
        else:
            send_notification(user_notifications, base_url)
            user_notifications = [notification]
        lastid = notification.user.id

    if len(user_notifications) > 0:
        send_notification(user_notifications, base_url)
