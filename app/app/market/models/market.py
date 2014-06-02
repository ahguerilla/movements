from datetime import datetime
import app.users.models as user_models
from django.db import models

from django.utils.translation import ugettext_lazy as _
from tinymce import models as tinymodels

import django.contrib.auth as auth

from django.core.urlresolvers import reverse
from django.utils.timezone import now


class MarketItem(models.Model):
    OPEN = 0
    WATCH = 1
    URGENT = 2
    CLOSED_BY_ADMIN = 3
    CLOSED_BY_USER = 4

    STATUS_CHOICES = (
        (OPEN, _('Open')),
        (WATCH, _('Watch')),
        (URGENT, _('Urgent')),
        (CLOSED_BY_ADMIN, _('Closed By Admin')),
        (CLOSED_BY_USER, _('Closed By User')),
    )

    item_type = models.CharField(_('item_type'), max_length=200, blank=False)
    owner = models.ForeignKey(auth.models.User, blank=True)
    title = models.CharField(_('title'), max_length=200, blank=False)
    details = tinymodels.HTMLField(_('details'), blank=False)
    countries = models.ManyToManyField(user_models.Countries)
    issues = models.ManyToManyField(user_models.Issues)
    skills = models.ManyToManyField(user_models.Skills)
    url = models.CharField(_('URL Link'), max_length=500, blank=True)
    published = models.BooleanField(_('is published?'), default=True)
    pub_date = models.DateTimeField(_('publish date'), default=datetime.now)
    exp_date = models.DateTimeField(_('expiry date'),blank=True, null=True)
    commentcount = models.IntegerField(_('commentcount'), default=0)
    ratecount = models.IntegerField(_('ratecount'), default=0)
    reportcount = models.IntegerField(_('reportcount'), default=0)
    score = models.FloatField(_('score'),default=0)
    deleted = models.BooleanField(_('deleted'), default=False)
    never_exp = models.BooleanField(_('never expires'), default=False)
    status = models.PositiveSmallIntegerField(
        _('status'), max_length=1, default=OPEN, choices=STATUS_CHOICES)
    closed_date = models.DateTimeField(
        _('closed date'), null=True, blank=True)

    def __unicode__(self):
        return self.details

    class Meta:
        app_label="market"

    def save(self, *args, **kwargs):
        if not self.closed_date and (self.status == self.CLOSED_BY_USER
                                     or self.status == self.CLOSED_BY_ADMIN):
            self.closed_date = now()
        super(MarketItem, self).save(*args, **kwargs)

    def getdict(self, request=None):
        adict = {'fields':{}}
        adict['pk'] = self.id
        adict['fields']['pk'] = self.id
        adict['fields']['item_type'] = self.item_type
        adict['fields']['issues'] = [ob.id for ob in self.issues.all()]
        adict['fields']['countries'] = [ob.id for ob in self.countries.all()]
        adict['fields']['skills'] = [ob.id for ob in self.skills.all()]
        adict['fields']['title'] = self.title
        adict['fields']['details'] = self.details
        adict['fields']['pub_date'] = str(self.pub_date)
        adict['fields']['exp_date'] = str(self.exp_date) if self.exp_date != None else ''
        adict['fields']['never_exp'] = self.never_exp
        adict['fields']['owner'] = [self.owner.username]
        adict['fields']['ownerid'] = [self.owner.id]
        adict['fields']['url'] = self.url
        adict['fields']['commentcount'] = self.commentcount
        adict['fields']['usercore'] = self.owner.userprofile.score if hasattr(self.owner, 'userprofile') else 0
        adict['fields']['userratecount'] = self.owner.userprofile.ratecount if hasattr(self.owner, 'userprofile') else 0
        adict['fields']['ratecount'] = self.ratecount
        adict['fields']['score'] = self.score
        adict['fields']['views'] = self.marketitemviewconter_set.count()
        adict['fields']['hidden'] = True if request!=None and self.marketitemhidden_set.filter(viewer_id=request.user.id).count()> 0 else False
        adict['fields']['stick'] = True if request!=None and self.marketitemstick_set.filter(viewer_id=request.user.id, item_id=self.id).count()> 0 else False
        adict['fields']['avatar'] = reverse('avatar_render_primary', args=[self.owner.username,80])
        return adict

class MarketItemViewConter(models.Model):
    item = models.ForeignKey(MarketItem)
    viewer = models.ForeignKey(user_models.User)
    counter = models.IntegerField(_('counter'), default=0)

    class Meta:
        app_label="market"



class MarketItemHidden(models.Model):
    item = models.ForeignKey(MarketItem)
    viewer = models.ForeignKey(user_models.User)

    class Meta:
        app_label="market"


class MarketItemStick(models.Model):
    item = models.ForeignKey(MarketItem)
    viewer = models.ForeignKey(user_models.User)

    class Meta:
        app_label="market"


class MarketItemActions(models.Model):
    market_item = models.ForeignKey(
        MarketItem, verbose_name=_('market item'))
    action = models.TextField(_('action'))
    date_of_action = models.DateTimeField(_('date of action'))

    class Meta:
        app_label = 'market'
        verbose_name = _('actions of market item')
        verbose_name_plural = _('actions of market item')

    def __unicode__(self):
        return u'%s / %s' % (self.actions, self.date_of_action)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.date_of_action = now()
        super(MarketItemActions, self).save(*args, **kwargs)


class MarketItemNextSteps(models.Model):
    market_item = models.ForeignKey(
        MarketItem, verbose_name=_('market item'))
    next_step = models.TextField(_('next step'))
    date_of_action = models.DateTimeField(_('date of action'))
    completed = models.BooleanField(_('completed'), default=False)

    class Meta:
        app_label = 'market'
        verbose_name = _('next step of market item')
        verbose_name_plural = _('next steps of market item')

    def __unicode__(self):
        return u'%s / %s' % (self.next_step, self.date_of_action)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.date_of_action = now()
        super(MarketItemNextSteps, self).save(*args, **kwargs)
