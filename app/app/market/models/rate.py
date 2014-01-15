from datetime import datetime
from django.db import models

from django.utils.translation import ugettext_lazy as _
import django.contrib.auth as auth

from .market import MarketItem


class ItemRate(models.Model):
    owner = models.ForeignKey(auth.models.User, blank=True)
    item = models.ForeignKey(MarketItem, null=True, blank=True, related_name='rates')
    pub_date = models.DateTimeField(_('publish date'), default=datetime.now)
    title = models.CharField(_('title'),max_length=200,blank=False)
    score = models.IntegerField(_('score'),default=0)

    class Meta:
        app_label="market"

    def save(self, *args, **kwargs):
        model = self.__class__
        rates = ItemRate.objects.filter(item=self.item).filter(~Q(owner=self.owner))
        if self.id == None:
            self.item.ratecount+=1
        if len(rates) == 0:
            self.item.score = int(self.score)
        else:
            self.item.score = (int(self.score) + sum([rate.score for rate in rates]))/float(self.item.ratecount)

        self.item.save_base()
        self.item.save()