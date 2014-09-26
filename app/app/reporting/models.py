# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.models import LogEntry
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.utils import translation


from app.utils import EnumChoices
from ..market.models import MarketItem


class IncidentTracking(MarketItem):

    class Meta:
        proxy = True
        verbose_name = _('incident')
        verbose_name_plural = _('incident tracking')


class UserTracking(get_user_model()):
    """
    Proxy model is displayed on the reporting section of admin.
    """
    class Meta:
        proxy = True
        verbose_name = _('user tracking')
        verbose_name_plural = _('user tracking')

    def get_requests(self):
        return self.marketitem_set.filter(item_type='request')

    def get_offers(self):
        return self.marketitem_set.filter(item_type='offer')


class UserActivity(LogEntry):
    ACTION_CHOICES = EnumChoices(
        ADDITION=(ADDITION,  _('addition')),
        CHANGE=(CHANGE, _('change')),
        DELETION=(DELETION, _('deletion')),
        LOGGED_IN=(4, _('user logged in')),
    )

    def get_action_flag(self):
        return dict(zip(dict(self.ACTION_CHOICES).keys(),
                        dict(self.ACTION_CHOICES).values()))[self.action_flag]
    get_action_flag.short_description = _('action flag')
    get_action_flag.admin_order_field = 'action_flag'

    class Meta:
        proxy = True
        verbose_name = _('user activity')
        verbose_name_plural = _('user activity')


@receiver(user_logged_in)
def do_stuff(sender, request, user, **kwargs):
    # set the interface language
    if hasattr(request.user, 'userprofile'):
        translation.activate(request.user.userprofile.interface_lang)
        request.LANGUAGE_CODE = translation.get_language()

    UserActivity.objects.log_action(
        user_id=request.user.pk,
        content_type_id=ContentType.objects.get_for_model(user).pk,
        object_id=user.pk,
        object_repr=force_text(user),
        action_flag=UserActivity.ACTION_CHOICES.LOGGED_IN
    )
