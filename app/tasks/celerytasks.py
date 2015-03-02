from app.users.models import UserProfile, Language, LanguageRating
from app.market.models import (
    Notification, MarketItem, Comment,
    MarketItemTranslation, CommentTranslation
)
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
        obj, Notification.STATUSES.PENDING)


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
    create_translators_notifications(
        comment, Notification.STATUSES.PENDING)


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


def find_translators(lang_codes):
    users = set()
    if isinstance(lang_codes, (list, set, tuple)):
        rates = LanguageRating.objects\
            .filter(language__launguage_code__in=lang_codes, rate__gte=1)\
            .values('rate', 'user_id')
        candidate_users = {}
        for rate in rates:
            candidate_users.setdefault(rate['user_id'], []).append(rate['rate'])
            item = candidate_users.get(rate['user_id'])
            if len(item) == 2 and sum(item) / 2 >= 3:
                users.add(rate['user_id'])
        users = set(UserProfile.objects\
            .filter(user_id__in=users,
                    skills__skills_en__iexact='translation')\
            .values_list('user_id', flat=True))
    elif isinstance(lang_codes, (str, unicode)):
        users = set(LanguageRating.objects\
            .filter(language__launguage_code=lang_codes, rate__gt=2)\
            .values_list('user_id', flat=True))
    return users


def find_CMs(lang_code=None):
    params = {'is_cm': True}
    if lang_code is not None:
        if isinstance(lang_code, (str, unicode)):
            params['languages__launguage_code__iexact'] = lang_code
        elif isinstance(lang_code, (list, set, tuple)):
            params['languages__launguage_code__in'] = lang_code
    return set(UserProfile.objects.filter(**params).values_list('user_id', flat=True))


def create_translation_notification(obj, status, user_id=None, reminder=False, save=True):
    notification = Notification()
    if isinstance(obj, MarketItem) and user_id:
        notification.user_id = user_id
        notification.item = obj
        notification.avatar_user = obj.owner.username
        notification.text = get_notification_text(obj)
    elif isinstance(obj, Comment) and user_id:
        notification.user_id = user_id
        notification.item_id = obj.item_id
        notification.comment = obj
        notification.avatar_user = obj.owner.username
        notification.text = get_notification_text(obj.item)
    elif isinstance(obj, MarketItemTranslation):
        notification.user_id = obj.owner_candidate_id
        notification.item_id = obj.market_item_id
        notification.avatar_user = obj.market_item.owner.username
        notification.text = get_notification_text(obj.market_item)
        notification.timeto = obj.get_endtime()
    elif isinstance(obj, CommentTranslation):
        notification.user_id = obj.owner_candidate_id
        notification.comment_id = obj.comment_id
        notification.item_id = obj.comment.item_id
        notification.avatar_user = obj.comment.owner.username
        notification.text = get_notification_text(obj.comment.item)
        notification.timeto = obj.get_endtime()
    notification.translation = status
    notification.reminder = reminder
    if save:
        notification.save()
    return notification


def create_translators_notifications(obj, status, lang_code=None, save=True):
    if lang_code is None:
        lang_code = obj.language

    notifications = []
    for user_id in find_translators(lang_code):
        notifications.append(
            create_translation_notification(
                obj, status, user_id=user_id, save=False))
    if save:
        Notification.objects.bulk_create(notifications)
    return notifications


def create_CMs_notifications(obj, status, lang_code=None, reminder=False, save=True):
    notifications = []
    for user_id in find_CMs(lang_code):
        notifications.append(
            create_translation_notification(
                obj, status, user_id=user_id, reminder=False, save=False))
    if save:
        Notification.objects.bulk_create(notifications)
    return notifications


@_app.task(name="TakeinNotification", bind=True)
def takein_notification(self, obj, correction=False):
    if correction:
        create_translation_notification(obj, Notification.STATUSES.CORRECTION)
    else:
        create_translation_notification(obj, Notification.STATUSES.TRANSLATION)


@_app.task(name="ApprovedNotification", bind=True)
def approved_notification(self, obj):
    create_translation_notification(obj, Notification.STATUSES.APPROVED)

    if isinstance(obj, MarketItemTranslation):
        obj = obj.market_item
    elif isinstance(obj, CommentTranslation):
        obj = obj.comment
    create_translation_notification(
        obj, Notification.STATUSES.APPROVED, user_id=obj.owner_id)


@_app.task(name="ApproveNotification", bind=True)
def approve_notification(self, obj):
    create_CMs_notifications(
        obj, Notification.STATUSES.APPROVAL,
        lang_code=[obj.language, obj.source_language])


@_app.task(name="TakeoffNotification", bind=True)
def takeoff_notification(self, translation):
    notifications = []

    # to translators
    if isinstance(translation, MarketItemTranslation):
        obj = translation.market_item
    elif isinstance(translation, CommentTranslation):
        obj = translation.comment
    notifications += create_translators_notifications(
        obj,
        Notification.STATUSES.PENDING,
        lang_code=[translation.language, translation.source_language],
        save=False)

    # to CMs
    notifications += create_CMs_notifications(
        translation,
        Notification.STATUSES.PENDING,
        [translation.language, translation.source_language],
        False, False)

    Notification.objects.bulk_create(notifications)


@_app.task(name="RevokeNotification", bind=True)
def revoke_notification(self, translation):
    notifications = []
    notifications.append(
        create_translation_notification(
            translation, Notification.STATUSES.REVOKED, save=False))

    if isinstance(translation, MarketItemTranslation):
        obj = translation.market_item
    elif isinstance(translation, CommentTranslation):
        obj = translation.comment
    notifications += create_translators_notifications(
        obj,
        Notification.STATUSES.PENDING,
        lang_code=[translation.language, translation.source_language],
        save=False)
    Notification.objects.bulk_create(notifications)


def create_reminder_notifications(model, c_status, time, n_status, save=False):
    notifications = []
    translations = model.objects.filter(
        status__gt=model.global_state.PENDING,
        c_status=c_status,
        timer__lt=time,
        reminder=False).select_related('owner_candidate')
    for translation in translations:
        notifications.append(
            create_translation_notification(
                translation, n_status, reminder=True, save=save))

        notifications += create_CMs_notifications(
            translation,
            n_status,
            [translation.language, translation.source_language],
            False, False)

    translations.update(reminder=True)
    return notifications


def create_revoked_notifications(model, c_status, time, save=False):
    notifications = []
    translations = model.objects.filter(
        status__gt=model.global_state.PENDING,
        c_status=c_status,
        timer__lt=time).select_related('owner_candidate')
    for translation in translations:
        notifications.append(
            create_translation_notification(
                translation, Notification.STATUSES.REVOKED, save=save))
        translation.clear_state()

        if isinstance(translation, MarketItemTranslation):
            obj = translation.market_item
        elif isinstance(translation, CommentTranslation):
            obj = translation.comment
        notifications += create_translators_notifications(
            obj,
            Notification.STATUSES.PENDING,
            lang_code=[translation.language, translation.source_language],
            save=False)

    return notifications


@periodic_task(run_every=timedelta(minutes=1))
def check_translation_timings():
    notifications = []
    translations = None

    for model in [MarketItemTranslation, CommentTranslation]:
        notifications += create_reminder_notifications(
            model,
            model.inner_state.TRANSLATION,
            now() - model._time / 2,
            Notification.STATUSES.TRANSLATION)
        notifications += create_reminder_notifications(
            model,
            model.inner_state.CORRECTION,
            now() - model._time / 4,
            Notification.STATUSES.CORRECTION)

        notifications += create_revoked_notifications(
            model,
            model.inner_state.TRANSLATION,
            now() - model._time)
        notifications += create_revoked_notifications(
            model,
            model.inner_state.CORRECTION,
            now() - model._time / 2)

    # save notifications
    print(notifications)
    Notification.objects.bulk_create(notifications)
