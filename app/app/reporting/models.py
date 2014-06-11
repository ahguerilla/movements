# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

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
