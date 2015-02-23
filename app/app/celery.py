from __future__ import absolute_import

import json

from celery import Celery
from django.db.models import Q
from django.conf import settings

from app.models import NotificationPing
from app.sforce import add_market_item_to_salesforce
from app.users.models import UserProfile
from app.market.models import Notification


app = Celery('celerytasks', broker=settings.CELERY_BROKER)
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


def get_notification_text(obj, update=False):
    return json.dumps({
        'update': update,
        'title': obj.title
    })


def get_notification_comment_text(obj, username, comment):
    return json.dumps({
        'username': username,
        'title': obj.title,
        'comment': comment.id,
    })


def find_people_interested_in(obj):
    interests = [interest.id for interest in obj.interests.all()]
    query = Q(interests__in=interests)
    query = query & ~Q(user=obj.owner)
    profiles = UserProfile.objects.filter(query).distinct('id').only('user').all()
    return profiles


@app.task()
def on_market_item_creation(market_item):
    create_notification(market_item)
    add_market_item_to_salesforce(market_item)


@app.task(name="createNotification")
def create_notification(obj):
    profiles = find_people_interested_in(obj)
    for profile in profiles:
        notification = Notification()
        notification.user = profile.user
        notification.item = obj
        notification.avatar_user = obj.owner.username
        notification.text = get_notification_text(obj)
        notification.save()


@app.task(name="createCommentNotification")
def create_comment_notification(obj, comment, username):
    created = set()
    if obj.owner.username != username:
        notification = Notification()
        notification.user = obj.owner
        notification.item = obj
        notification.avatar_user = username
        notification.comment_id = comment.id
        notification.text = get_notification_comment_text(obj, username, comment)
        notification.save()
        created.add(obj.owner.id)
    for cmnt in obj.comments.all():
        if cmnt.owner.username != username and cmnt.owner.id not in created and not cmnt.deleted:
            notification = Notification()
            notification.user = cmnt.owner
            notification.item = obj
            notification.avatar_user = username
            notification.comment_id = comment.id
            notification.text = get_notification_comment_text(obj, username, comment)
            notification.save()
            created.add(cmnt.owner.id)


@app.task()
def on_market_item_update(market_item):
    update_notifications(market_item)
    add_market_item_to_salesforce(market_item)


@app.task(name="updateNotifications")
def update_notifications(obj):
    notification_objs = Notification.objects.filter(item=obj.id).only('user').all()
    notification_userids = set(notification.user.id for notification in notification_objs)
    profiles = find_people_interested_in(obj)
    user_ids = set(profile.user.id for profile in profiles)

    notifications_to_create = user_ids.difference(notification_userids)
    for user_id in notifications_to_create:
        notification = Notification()
        notification.user_id = user_id
        notification.item = obj
        notification.avatar_user = obj.owner.username
        notification.text = get_notification_text(obj)
        notification.save()

    notifications_to_update = user_ids.intersection(notification_userids)
    for user_id in notifications_to_update:
        notification = Notification()
        notification.user_id = user_id
        notification.item = obj
        notification.avatar_user = obj.owner.username
        notification.text = get_notification_text(obj, update=True)
        notification.save()


@app.task(name="new_postman_message")
def new_postman_message(message):
    notification = Notification()
    notification.user_id = message.recipient.id
    notification.text = json.dumps({
        'type': 'message',
        'subject': message.subject,
        'sender': message.sender.username,
    })
    notification.avatar_user = message.sender.username
    notification.save()


@app.task(name="notification_ping")
def notification_ping(email_to):
    ping = NotificationPing(send_email_to=email_to)
    ping.save()


@app.task(name='update_salesforce')
def update_salesforce():
    print 'updating salesforce'
