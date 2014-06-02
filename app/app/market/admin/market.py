# -*- coding: utf-8 -*-
from django.contrib import admin

from ..models import MarketItemActions


class MarketItemActionsAdmin(admin.ModelAdmin):
    readonly_fields = ('date_of_action',)


admin.site.register(MarketItemActions, MarketItemActionsAdmin)
