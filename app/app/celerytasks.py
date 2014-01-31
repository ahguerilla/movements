from __future__ import absolute_import
import os
import sys
sys.path.append(os.path.join(os.path.expanduser('~'),'.virtualenvs/ahr/lib/python2.7/site-packages'))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../','../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../')))
sys.path.append(os.path.abspath(os.path.abspath(__file__)))

from celery import Celery, shared_task, task
from threading import Thread
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings.local')
_app = Celery('celerytasks',broker='amqp://guest@localhost//')
_app.config_from_object('django.conf:settings')
_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


from app.users.models import UserProfile
from app.market.models import MarketItem,Notification
from django.db.models import Q
from django.core.mail import send_mail
import constance

#import rpdb2; rpdb2.start_embedded_debugger_interactive_password()
from datetime import timedelta
#from celery.schedules import crontab


def getNotifText(obj):
    return obj.owner.username +' created a '+obj.item_type+ ' that you might be interested in'


def getNotifCommentText(obj,username):
    return username +' commented on your '+obj.item_type


def geSomeoneCommentUrCommentText(obj,username):
    var = 'a request' if obj.item_type=='request' else 'an offer'
    return username +' commented on '+ var +' that you commented on'

    
def findPeopleInterestedIn(obj):
    skills= [skill.id for skill in obj.skills.all()]
    countries = [country.id for country in obj.countries.all()]
    issues = [issue.id for issue in obj.issues.all()]
    query = Q(skills__in=skills) | Q(issues__in=issues) | Q(countries__in=countries)
    query = query & (~Q(user=obj.owner) & Q(get_newsletter=True))
    profiles = UserProfile.objects.filter(query).distinct('id').only('user').all()
    return profiles


@shared_task
@_app.task(name="createNotification",bind=True)
def createNotification(self,obj):
    notifications =[ notif.user for notif in Notification.objects.filter(item=obj.id).only('user').all()]    
    profiles = findPeopleInterestedIn(obj)
    for profile in profiles:
        if profile.user.id in notifications:
            continue
        notification = Notification()
        notification.user = profile.user
        notification.item = obj
        notification.avatar_user = obj.owner.username
        notification.text = getNotifText(obj)
        notification.save()
    return


@shared_task
@_app.task(name="createCommentNotification",bind=True)
def createCommentNotification(self,obj,username):
    if obj.owner.username != username:
        notification = Notification()
        notification.user = obj.owner
        notification.item = obj
        notification.avatar_user = username
        notification.text = getNotifCommentText(obj,username)    
        notification.save()
    notified = []
    for comment in obj.comments.all():        
        if comment.owner.username != username and comment.owner.id not in notified:            
            notification = Notification()
            notification.user = comment.owner
            notification.item = obj
            notification.avatar_user = username
            notification.text = geSomeoneCommentUrCommentText(obj,username)    
            notification.save()
            notified.append(comment.owner.id)
    return


@shared_task
@_app.task(name="updateNotifications",bind=True)
def updateNotifications(self,obj):
    notif_objs = Notification.objects.filter(item=obj.id).only('user','seen').all()
    notif_userids =set([ notif.user.id for notif in notif_objs ])
    profiles = findPeopleInterestedIn(obj)
    user_ids = set([profile.user.id for profile in profiles])

    notifs_todelete = notif_userids.difference(user_ids)
    for notif in notif_objs:
        if notif.user.id in notifs_todelete:
            notif.delete()

    notifs_tocereate=user_ids.difference(notif_userids)
    for user_id in notifs_tocereate:
        notification = Notification()
        notification.user_id = user_id
        notification.item = obj
        notification.avatar_user = obj.owner.username
        notification.text = getNotifText(obj)
        notification.save()

    notifs_toupdate = user_ids.intersection(notif_userids)
    for notif in notif_objs:
        if notif.user.id in notifs_toupdate and notif.text != obj.title:
            notif.text = getNotifText(obj)
            notif.save()
    return


@shared_task
@_app.task(name="markeSeenNotifications",bind=True)
def markeSeenNotifications(self,objs,user_id):
    obj_ids=[obj.id for obj in objs]
    notifications = Notification.objects.filter(user=user_id).filter(item__in=obj_ids).filter(seen=False).all()
    for notification in notifications:
        notification.seen=True
        notification.save()
    return


def createMail(notifications):
    return 'You might be interested in this stuff'

@shared_task
@_app.task(name="sendNotification")
def sendNotification():
    profiles = UserProfile.objects.filter(get_newsletter=True).all()
    for profile in profiles:
        notifications = Notification.objects.filter(user=profile.user.id).filter(seen=False).all()
        msg = createMessage(notifications)
        send_mail('Subject',msg , constance.config.NO_REPLY_EMAIL ,profile.user.email, fail_silently=False)
        for notification in notifications:
            notification.seen=True
            notification.save()

    return

