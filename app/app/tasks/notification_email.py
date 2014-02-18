from __future__ import absolute_import
import os
import sys

sys.path.append(os.path.join(os.path.expanduser('~'),'.virtualenvs/mani.ahr/lib/python2.7/sitepackages'))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../','../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../','../','../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../','app')))

from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings.local')

from datetime import timedelta,datetime
from app.users.models import UserProfile
from app.market.models import MarketItem,Notification
from django.db.models import Q
from django.core.mail import send_mail,EmailMessage
from django.core.urlresolvers import reverse
import constance
from django.template.loader import render_to_string
from dateutil.relativedelta import *


def create_notification_message(notifications):
    string = render_to_string('emails/notification_email.html',{'notifications':notifications})    
    return string


def send_notification(notifications):
    messagebody = create_notification_message(notifications)
    mail = EmailMessage('AHR Notification Email',
                        messagebody,
                        constance.config.NO_REPLY_EMAIL,
                        [notifications[0].user.email])
    mail.content_subtype = 'html'
    mail.send()

if __name__ == '__main__': 
    from_date = datetime.now() + relativedelta(weekday=SU(-int(constance.config.EMAIL_NOTIFICATION_INTERVAL)),
                                               hour=0,
                                               minute=0,
                                               second=0,
                                               microsecond=0)
    
    notifications = Notification.objects.\
        filter(user__userprofile__get_newsletter=True,
               pub_date__gte=from_date).\
        order_by('user','pub_date')
    alist = []
    lastid = None
    for notification in notifications:
        if not lastid or notification.user.id == lastid:
            alist.append(notification)
            lastid = notification.user.id
        else:
            lastid = notification.user.id
            send_notification(alist)
            alist = []
            
    if len(alist)>0:
        send_notification(alist)
    