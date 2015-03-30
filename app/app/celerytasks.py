from __future__ import absolute_import

import json


from celery import Celery
from django.db.models import Q
from django.conf import settings
from django.utils.timezone import timedelta, now


from app.models import NotificationPing
from app.sforce import add_market_item_to_salesforce, update_market_item_stats
from app.users.models import UserProfile
from app.market.models import (
    Notification, MarketItem, Comment,
    MarketItemTranslation, CommentTranslation,
    MarketItemSalesforceRecord
)


app = Celery('celerytasks', broker=settings.CELERY_BROKER)
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from celery.task import periodic_task
from djcelery_email.tasks import send_email


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
    _create_translators_notifications(
        obj, Notification.STATUSES.PENDING)


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
    _create_translators_notifications(
        comment, Notification.STATUSES.PENDING)


@app.task(name='app.celery.on_market_item_update')
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
    update_market_item_stats()


def _find_translators(lang_codes):
    if isinstance(lang_codes, (list, set, tuple)):
        users = UserProfile.objects
        for lang_code in lang_codes:
            users = users.filter(translation_languages__launguage_code=lang_code)
        return users.values_list('user_id', flat=True)
    else:
        return UserProfile.objects \
            .filter(translation_languages__launguage_code=lang_codes) \
            .values_list('user_id', flat=True)


def _find_cms(lang_code=None):
    params = {'is_cm': True}
    if lang_code is not None:
        if isinstance(lang_code, (str, unicode)):
            params['languages__launguage_code__iexact'] = lang_code
        elif isinstance(lang_code, (list, set, tuple)):
            params['languages__launguage_code__in'] = lang_code
    return set(UserProfile.objects.filter(**params).values_list('user_id', flat=True))


def _get_item_from_translation(translation):
    if isinstance(translation, MarketItemTranslation):
        return translation.market_item
    elif isinstance(translation, CommentTranslation):
        return translation.comment
    ValueError('translation must be a valid translation type')


def _create_translation_notification(obj, status, user_id=None, reminder=False, save=True):
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


def _create_translators_notifications(obj, status, lang_code=None, save=True):
    if lang_code is None:
        lang_code = obj.language
    notifications = []
    for user_id in _find_translators(lang_code):
        notifications.append(_create_translation_notification(obj, status, user_id=user_id, save=False))
    if save:
        Notification.objects.bulk_create(notifications)
    return notifications


def _create_cm_notifications(obj, status, lang_code=None, reminder=False, save=True):
    notifications = []
    for user_id in _find_cms(lang_code):
        notifications.append(
            _create_translation_notification(
                obj, status, user_id=user_id, reminder=False, save=False))
    if save:
        Notification.objects.bulk_create(notifications)
    return notifications


@app.task(name="TakeinNotification")
def takein_notification(obj, correction=False):
    if correction:
        _create_translation_notification(obj, Notification.STATUSES.CORRECTION)
    else:
        _create_translation_notification(obj, Notification.STATUSES.TRANSLATION)


@app.task(name="ApprovedNotification")
def approved_notification(obj):
    _create_translation_notification(obj, Notification.STATUSES.APPROVED)
    item = _get_item_from_translation(obj)
    _create_translation_notification(item, Notification.STATUSES.APPROVED, user_id=obj.owner_id)


@app.task(name="ApproveNotification")
def approve_notification(obj):
    _create_cm_notifications(obj, Notification.STATUSES.APPROVAL, lang_code=[obj.language, obj.source_language])


@app.task(name="TakeoffNotification")
def takeoff_notification(translation):
    item = _get_item_from_translation(translation)
    notifications = _create_translators_notifications(
        item,
        Notification.STATUSES.PENDING,
        lang_code=[translation.language, translation.source_language],
        save=False)

    notifications += _create_cm_notifications(
        translation,
        Notification.STATUSES.PENDING,
        [translation.language, translation.source_language],
        False, False)

    Notification.objects.bulk_create(notifications)


@app.task(name="RevokeNotification")
def revoke_notification(translation):
    notifications = [
        _create_translation_notification(translation, Notification.STATUSES.REVOKED, save=False)
    ]

    item = _get_item_from_translation(translation)
    notifications += _create_translators_notifications(
        item,
        Notification.STATUSES.PENDING,
        lang_code=[translation.language, translation.source_language],
        save=False)
    Notification.objects.bulk_create(notifications)


def _create_reminder_notifications(model, c_status, time, n_status, save=False):
    notifications = []
    translations = model.objects.filter(
        status__gt=model.global_state.PENDING,
        c_status=c_status,
        timer__lt=time,
        reminder=False).select_related('owner_candidate')
    for translation in translations:
        notifications.append(
            _create_translation_notification(
                translation, n_status, reminder=True, save=save))

        notifications += _create_cm_notifications(
            translation,
            n_status,
            [translation.language, translation.source_language],
            False, False)

    translations.update(reminder=True)
    return notifications


def _create_revoked_notifications(model, c_status, time, save=False):
    notifications = []
    translations = model.objects.filter(
        status__gt=model.global_state.PENDING,
        c_status=c_status,
        timer__lt=time).select_related('owner_candidate')
    for translation in translations:
        notifications.append(
            _create_translation_notification(
                translation, Notification.STATUSES.REVOKED, save=save))
        translation.clear_state()
        item = _get_item_from_translation(translation)
        notifications += _create_translators_notifications(
            item,
            Notification.STATUSES.PENDING,
            lang_code=[translation.language, translation.source_language],
            save=False)

    return notifications


@periodic_task(run_every=timedelta(minutes=1))
def check_translation_timings():
    notifications = []

    for model in [MarketItemTranslation, CommentTranslation]:
        notifications += _create_reminder_notifications(
            model,
            model.inner_state.TRANSLATION,
            now() - model._time / 2,
            Notification.STATUSES.TRANSLATION)
        notifications += _create_reminder_notifications(
            model,
            model.inner_state.CORRECTION,
            now() - model._time / 4,
            Notification.STATUSES.CORRECTION)
        notifications += _create_revoked_notifications(
            model,
            model.inner_state.TRANSLATION,
            now() - model._time)
        notifications += _create_revoked_notifications(
            model,
            model.inner_state.CORRECTION,
            now() - model._time / 2)
    Notification.objects.bulk_create(notifications)
