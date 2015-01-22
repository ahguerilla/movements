from app.users.models import UserProfile
from app.market.models import Notification, TraslationCandidade
from django.db.models import Q
from django.conf import settings
from django.utils.timezone import timedelta, now

from datetime import datetime
import json

import logging
logger= logging.getLogger(__name__)

if not '_app' in dir():
    from celery import Celery
    from celery.task import periodic_task
    _app = Celery('celerytasks', broker=settings.CELERY_BROKER)

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


@_app.task(name="createNotification", bind=True)
def create_notification(self, obj):
    profiles = find_people_interested_in(obj)
    for profile in profiles:
        notification = Notification()
        notification.user = profile.user
        notification.item = obj
        notification.avatar_user = obj.owner.username
        notification.text = get_notification_text(obj)
        notification.save()


@_app.task(name="createCommentNotification", bind=True)
def create_comment_notification(self, obj, comment, username):
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


@_app.task(name="updateNotifications", bind=True)
def update_notifications(self, obj):
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


@_app.task(name="new_postman_message", bind=True)
def new_postman_message(self, message):
    notification = Notification()
    notification.user_id = message.recipient.id
    notification.text = json.dumps({
        'type': 'message',
        'subject': message.subject,
        'sender': message.sender.username,
    })
    notification.avatar_user = message.sender.username
    notification.save()


# TODO move timings to settings
# defaults days=1 and hours=12
post_translation_time = timedelta(minutes=2)
post_correction_time = timedelta(minutes=1)


# TODO
@periodic_task(run_every=timedelta(minutes=1))
def check_translation_timings():
    translations = None
    translations = TraslationCandidade.objects.filter(
        status=TraslationCandidade.STATUS_CHOICES.ACTIVE,
        edited__lt=now() - post_translation_time/2,
        reminder=False).select_related('owner')
    # for translation in translations:
        # need to create notifications here
    translations.update(reminder=True)

    translations = None
    translations = TraslationCandidade.objects.filter(
        status=TraslationCandidade.STATUS_CHOICES.ACTIVE,
        edited__lt=now() - post_translation_time/2,
        ).select_related('owner', 'translation')
    for translation in translations:
        # need to create notifications here

        # updating translation status
        translation.translation.set_done_or_pending()
    translations.delete()

    corrections = None
    corrections = TraslationCandidade.objects.filter(
        status=TraslationCandidade.STATUS_CHOICES.CORRECTION,
        edited__lt=now() - post_correction_time/2,
        reminder=False).select_related('owner')
    # for correction in corrections:
        # need to create notifications here
    corrections.update(reminder=True)

    corrections = None
    corrections = TraslationCandidade.objects.filter(
        status=TraslationCandidade.STATUS_CHOICES.ACTIVE,
        edited__lt=now() - post_correction_time,
        ).select_related('owner', 'translation')
    for correction in corrections:
        # need to create notifications here

        # updating translation status
        translation.translation.set_done_or_pending()
    corrections.delete()
