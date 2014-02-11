from __future__ import absolute_import
import os
import sys

sys.path.append(os.path.join(os.path.expanduser('~'),'.virtualenvs/mani.ahr/lib/python2.7/site-packages'))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../','../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../','app')))

from celery import Celery
from threading import Thread
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings.local')

from datetime import timedelta,datetime
from app.users.models import UserProfile
from app.market.models import MarketItem,Notification
from django.db.models import Q
from django.core.mail import send_mail,EmailMessage
from django.core.urlresolvers import reverse
import constance


def createNotifMessage(notifications):
    string = '<h4>Hello dear Exchangivist</h4>'
    string += '<h5>Here are your last week notifications:</h5><p>'
    for notification in notifications:
        if notification.comment:
            string += notification.comment.owner.username+ ' commented on '
            string += notification.item.title+ ' at '+ str(notification.pub_date)[0:16]
            string += ' <a href ="http://ahr.guerillasoftware.net/market/#item/'+str(notification.item.id)+'"> click here to view this '+notification.item.item_type+'</a>'
            string += '<br/><br/>'
        else:
            string += notification.item.owner.username+ ' created '
            string += notification.item.title+ ' at '+ str(notification.pub_date)[0:16]
            string += ' <a href ="http://ahr.guerillasoftware.net/market/#item/'+str(notification.item.id)+'"> click here to view this '+notification.item.item_type+'</a>'
            string += '<br/><br/>'
            
    string += '</p> <p>Regards <br/>AHR team</p>'
    return string

def sendNotification(notifications):
    messagebody = createNotifMessage(notifications)
    mail = EmailMessage('AHR notifications',
                        messagebody,
                        constance.config.NO_REPLY_EMAIL,
                        [notifications[0].user.email])
    mail.content_subtype = 'html'
    mail.send()

if __name__ == '__main__':    
    notifications = Notification.objects.filter(user__userprofile__get_newsletter=True,
        pub_date__gte=datetime.now()-timedelta(int(constance.config.EMAIL_NOTIFICATION_INTERVAL))).\
        order_by('user','-pub_date')        
    alist=[]
    lastid=None
    for notification in notifications:
        if not lastid or notification.user.id == lastid:
            alist.append(notification)
            lastid = notification.user.id
        else:
            lastid = notification.user.id
            sendNotification(alist)
            alist=[]
            
    if len(alist)>0:
        sendNotification(alist)
    

