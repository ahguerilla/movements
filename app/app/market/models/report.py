from datetime import datetime
from django.db import models
from django.utils.timezone import now

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
        
        
class UserReport(models.Model):
    owner = models.ForeignKey(auth.models.User, blank=False)
    user = models.ForeignKey(auth.models.User, related_name='user_repots')
    contents = tinymce.models.HTMLField(_('contents'), blank=False)
    resolved = models.BooleanField(_('is resolved'), default=False)
    pub_date = models.DateTimeField(_('publish date'), default=datetime.now)    

    class Meta:
        ordering = ['-resolved', '-pub_date']
        app_label="market"


class EmailRecommendation(models.Model):
    market_item = models.ForeignKey(
        MarketItem, null=True, verbose_name=_('market item'))
    email = models.EmailField(_('e-mail'), default='', blank=True)
    recommendation_date = models.DateTimeField(
        _('date of recommendation'), default=now)

    class Meta:
        app_label = 'market'
        verbose_name = _('email recommendation')
        verbose_name_plural = _('email recommendations')

    def __unicode__(self):
        return u'%s' % self.market_item.title
