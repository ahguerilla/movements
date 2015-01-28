from app.users.models import UserProfile, Language
from app.market.models import Notification, TraslationCandidade, MarketItem
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
    create_translators_notifications(
        obj, Notification.STATUSES.PENDING,
        lang_code=Language.objects.exclude(launguage_code__iexact=obj.language))


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


def find_translators(lang_code):
    params = {'skills__skills_en__iexact': 'translation'}
    if isinstance(lang_code, (str, unicode)):
        params['languages__launguage_code__iexact'] = lang_code
    else:
        params['languages__in'] = lang_code
    return UserProfile.objects.filter(**params)


def find_CMs(lang_code=None):
    params = {'is_cm': True}
    if lang_code is not None:
        if isinstance(lang_code, (str, unicode)):
            params['languages__launguage_code__iexact'] = lang_code
        else:
            params['languages__in'] = lang_code
    return UserProfile.objects.filter(**params)


def create_translation_notification(obj, status, user=None, reminder=False, save=True):
    notification = Notification()
    if type(obj) == MarketItem and user:
        notification.user = user
        notification.item = obj
        notification.avatar_user = obj.owner.username
        notification.text = get_notification_text(obj)
    else:
        notification.user = obj.owner
        notification.item = obj.market_item
        notification.avatar_user = obj.market_item.owner.username
        notification.text = get_notification_text(obj.market_item)
        notification.timeto = obj.endtime()
    notification.translation = status
    notification.reminder = reminder
    if save:
        notification.save()
    return notification


def create_translators_notifications(market_item, status, lang_code=None, save=True):
    if lang_code is None:
        lang_code = Language.objects.exclude(launguage_code__iexact=market_item.language)

    notifications = []
    for userprofile in find_translators(lang_code):
        notifications.append(
            create_translation_notification(
                market_item, status, user=userprofile.user, save=False))
    if save:
        Notification.objects.bulk_create(notifications)
    return notifications


def create_CMs_notifications(market_item, status, lang_code=None, save=True):
    notifications = []
    for userprofile in find_CMs(lang_code):
        notifications.append(
            create_translation_notification(
                market_item, status,
                user=userprofile.user, save=False))
    if save:
        Notification.objects.bulk_create(notifications)
    return notifications


@_app.task(name="TakeinNotification", bind=True)
def takein_notification(self, obj, correction=False):
    if correction:
        create_translation_notification(obj, Notification.STATUSES.CORRECTION)
    else:
        create_translation_notification(obj, Notification.STATUSES.TRANSLATION)


@_app.task(name="CorrectionNotification", bind=True)
def correction_notification(self, obj):
    create_translation_notification(obj, Notification.STATUSES.CORRECTION)


@_app.task(name="ApprovedNotification", bind=True)
def approved_notification(self, obj):
    create_translation_notification(obj, Notification.STATUSES.APPROVED)
    create_translation_notification(
        obj.market_item, Notification.STATUSES.APPROVED, user=obj.market_item.owner)


@_app.task(name="ApproveNotification", bind=True)
def approve_notification(self, obj):
    create_CMs_notifications(
        obj.market_item, Notification.STATUSES.APPROVAL, lang_code=obj.language)


@_app.task(name="TakeoffNotification", bind=True)
def takeoff_notification(self, market_item, lang_code):
    notifications = []
    notifications += create_translators_notifications(
        market_item, Notification.STATUSES.PENDING,
        lang_code, save=False)
    notifications += create_CMs_notifications(
        market_item, Notification.STATUSES.PENDING,
        lang_code=lang_code, save=False)
    Notification.objects.bulk_create(notifications)


# TODO move timings to settings
# defaults days=1 and hours=12
post_translation_time = timedelta(minutes=4)
post_correction_time = timedelta(minutes=2)


@periodic_task(run_every=timedelta(minutes=1))
def check_translation_timings():
    notifications = []
    translations = None
    translations = TraslationCandidade.objects.filter(
        status=TraslationCandidade.STATUS_CHOICES.ACTIVE,
        edited__lt=now() - post_translation_time/2,
        reminder=False).select_related('owner')
    # creating notifications
    for translation in translations:
        notifications.append(
            create_translation_notification(
                translation, Notification.STATUSES.TRANSLATION, reminder=True, save=False))
    translations.update(reminder=True)

    translations = None
    translations = TraslationCandidade.objects.filter(
        status=TraslationCandidade.STATUS_CHOICES.ACTIVE,
        edited__lt=now() - post_translation_time,
        ).select_related('owner', 'translation')
    for translation in translations:
        # updating translation status
        translation.translation.set_done_or_pending()

        # creating notifications
        notifications += create_translators_notifications(
            translation.market_item, Notification.STATUSES.PENDING,
            lang_code=translation.language, save=False)
    translations.delete()

    corrections = None
    corrections = TraslationCandidade.objects.filter(
        status=TraslationCandidade.STATUS_CHOICES.CORRECTION,
        edited__lt=now() - post_correction_time/2,
        reminder=False).select_related('owner')
    # creating notifications
    for correction in corrections:
        notifications.append(
            create_translation_notification(
                correction, Notification.STATUSES.CORRECTION, reminder=True, save=False))
    corrections.update(reminder=True)


    corrections = None
    corrections = TraslationCandidade.objects.filter(
        status=TraslationCandidade.STATUS_CHOICES.ACTIVE,
        edited__lt=now() - post_correction_time,
        ).select_related('owner', 'translation')
    for correction in corrections:
        # updating translation status
        correction.translation.set_done_or_pending()
        # creating notifications
        notifications += create_translators_notifications(
            correction.market_item, Notification.STATUSES.PENDING,
            lang_code=correction.language, save=False)
    corrections.delete()

    # save notifications
    print(notifications)
    Notification.objects.bulk_create(notifications)
