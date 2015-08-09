from __future__ import absolute_import
import json

from celery import Celery
from django.db.models import Q
from django.conf import settings

from app.models import NotificationPing
from app.sforce import add_market_item_to_salesforce, update_market_item_stats
from app.market.models import CommentTranslation, MarketItemSalesforceRecord
from app.users.actions import check_user_notification_settings, construct_email, send_group_email

app = Celery('celerytasks', broker=settings.CELERY_BROKER)
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from djcelery_email.tasks import send_email
from app.market.tasks.translations import *
import logging
logger = logging.getLogger('notifications')


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


@app.task(name='app.celery.on_market_item_creation')
def on_market_item_creation(market_item):
    create_notification(market_item)
    add_market_item_to_salesforce(market_item)
    create_translations_for_item(market_item, MarketItemTranslation)


@app.task(name="createNotification")
def create_notification(market_item):
    profiles = find_people_interested_in(market_item)
    for profile in profiles:
        notification = Notification()
        notification.user = profile.user
        notification.item = market_item
        notification.avatar_user = market_item.owner.username
        notification.text = get_notification_text(market_item)
        notification.save()


@app.task(name="createCommentNotification")
def create_comment_notification(obj, comment, username):
    MarketItemSalesforceRecord.mark_for_update(obj.id)
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
    create_translations_for_item(comment, CommentTranslation)


@app.task(name='app.celery.on_market_item_update')
def on_market_item_update(market_item):
    update_notifications(market_item)
    add_market_item_to_salesforce(market_item)
    mark_translations_for_update(market_item)


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
    update_market_item_stats()


@app.task(name='send_group_message')
def send_group_message(message, group):
    success_count = 0
    skip_count = 0
    error_count = 0
    for u in group.user_set.all():
        try:
            if not check_user_notification_settings(u, group):
                skip_count += 1
                continue
            message = construct_email(message, u, group)
            send_group_email(message, u)
            success_count += 1
        except Exception as ex:
            error_count += 1
            logger.exception(ex.message)
    success_message = 'successfully sent message to {0} users and skipped {1} error count {2}'.format(success_count,
                                                                                                      skip_count,
                                                                                                      error_count)
    logger.debug(success_message)