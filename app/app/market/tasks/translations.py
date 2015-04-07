from django.db.models import Count
from app.users.models import Language, UserProfile
from app.market.models.notification import Notification
from app.market.models.translation import (
    get_or_create_user_translation, MarketItemTranslation, get_translatable_items_for_profile,
    get_approvable_items_for_profile
)


def create_translations_for_item(item, model):
    for code in Language.objects.exclude(launguage_code=item.language).values_list('launguage_code'):
        code = code[0]
        if code is not None:
            get_or_create_user_translation(item.id, code, model)


def mark_translations_for_update(item):
    MarketItemTranslation.objects.filter(status=MarketItemTranslation.global_state.GOOGLE,
                                         market_item=item).delete()
    MarketItemTranslation.objects.filter(market_item=item).update(needs_update=True)


def aggregate_translation_notification():
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

