from datetime import datetime
from django.db import models

from django.utils.translation import ugettext_lazy as _
import tinymce

import django.contrib.auth as auth

from .market import MarketItem


class MarketItemPostReport(models.Model):
    owner = models.ForeignKey(auth.models.User, blank=True)
    item = models.ForeignKey(MarketItem, null=True, blank=True, related_name='repots')
    contents = tinymce.models.HTMLField(_('contents'), blank=False)
    resolved = models.BooleanField(_('is resolved'), default=False)
    pub_date = models.DateTimeField(_('publish date'), default=datetime.now)
    published = models.BooleanField(_('is published?'), default=True)

    class Meta:
        ordering = ['-resolved', '-pub_date']
        app_label="market"

    def save(self, *args, **kwargs):
        self.item.reportcount += 1
        self.item.save()