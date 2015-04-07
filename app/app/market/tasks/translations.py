from celery.task import periodic_task, task
from datetime import timedelta

from django.db.models import Count
from app.users.models import Language, UserProfile
from app.market.models.notification import Notification
from app.market.models.translation import (
    get_or_create_user_translation, MarketItemTranslation, get_translatable_items_for_profile,
    get_approvable_items_for_profile,
    CommentTranslation)


def create_translations_for_item(item, model):
    for code in Language.objects.exclude(launguage_code=item.language).values_list('launguage_code'):
        code = code[0]
        if code is not None:
            get_or_create_user_translation(item.id, code, model)


def mark_translations_for_update(item):
    MarketItemTranslation.objects.filter(status=MarketItemTranslation.global_state.GOOGLE,
                                         market_item=item).delete()
    MarketItemTranslation.objects.filter(market_item=item).update(needs_update=True)


@periodic_task(run_every=timedelta(days=1))
def generate_translation_notification():
    """
    We get everyone who has more than one translation language and then generate a notification with the number of
    translations items that exist that we need their help with.
    """
    for up in UserProfile.objects.annotate(ttl_count=Count('translation_languages')).filter(ttl_count__gte=2):
        Notification.objects \
                    .filter(translation__in=[Notification.STATUSES.TRANSLATION_COUNT,
                                             Notification.STATUSES.APPROVAL_COUNT]) \
                    .update(seen=True, emailed=True)
        notification = Notification(user=up.user,
                                    avatar_user=up.user.username,
                                    translation=Notification.STATUSES.TRANSLATION_COUNT,
                                    text={'total': get_translatable_items_for_profile(up).count()})
        notification.save()
        if up.is_cm:
            notification = Notification(user=up.user,
                                        avatar_user=up.user.username,
                                        translation=Notification.STATUSES.APPROVAL_COUNT,
                                        text={'total': get_approvable_items_for_profile(up).count()})
            notification.save()


def _set_notification_item(notification, translation):
    if isinstance(translation, MarketItemTranslation):
        notification.item = translation.market_item
    elif isinstance(translation, CommentTranslation):
        notification.comment = translation.comment
        notification.item = translation.comment.item
    notification.text = {
        'source': translation.source_language,
        'dest': translation.language,
        'translation_id': translation.id,
    }
    ValueError('translation must be a valid translation type')


@task(name="TakeinNotification")
def translation_started_notification(translation):
    pass


@task(name="TranslationSubmitted")
def translation_submitted_notification(translation):
    pass


@task(name="ApprovedNotification")
def translation_approved_notification(translation, cm):
    n = Notification(user=translation.owner,
                     avatar_user=cm.username,
                     translation=Notification.STATUSES.APPROVED)
    _set_notification_item(n, translation)
    n.save()


@task(name="TakeoffNotification")
def translation_cancelled_notification(translation):
    pass


@task(name="RevokeNotification")
def translation_rejected_notification(translation, candidate, cm):
    n = Notification(user=candidate,
                     avatar_user=cm.username,
                     translation=Notification.STATUSES.REVOKED)
    _set_notification_item(n, translation)
    n.save()