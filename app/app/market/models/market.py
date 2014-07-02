from datetime import datetime
import app.users.models as user_models
from django.db import models

from django.utils.translation import ugettext_lazy as _
from tinymce import models as tinymodels

import django.contrib.auth as auth

from django.core.urlresolvers import reverse
from django.utils.timezone import now

from app.utils import EnumChoices


class MarketItem(models.Model):
    STATUS_CHOICES = EnumChoices(
        OPEN=(0, _('Open')),
        WATCH=(1, _('Watch')),
        URGENT=(2, _('Urgent')),
        CLOSED_BY_ADMIN=(3, _('Closed By Admin')),
        CLOSED_BY_USER=(4, _('Closed By User')),
    )
    TYPE_CHOICES = EnumChoices(
        REQUEST=('request', _('Request')),
        OFFER=('offer', _('Offer'))
    )

    item_type = models.CharField(_('item_type'), max_length=50, blank=False)
    owner = models.ForeignKey(auth.models.User, blank=True)
    staff_owner = models.ForeignKey(
        auth.models.User, blank=True, null=True, related_name='marketitems')
    title = models.CharField(_('title'), max_length=200, blank=False)
    details = tinymodels.HTMLField(_('details'), blank=False)
    interests = models.ManyToManyField(user_models.Interest, null=True, blank=True)
    countries = models.ManyToManyField(user_models.Countries, null=True, blank=True)
    specific_skill = models.CharField(_('Specific skill'), max_length=100, blank=True, null=True)
    url = models.CharField(_('URL Link'), max_length=500, blank=True)
    published = models.BooleanField(_('is published?'), default=True)
    pub_date = models.DateTimeField(_('publish date'), default=datetime.now)
    commentcount = models.IntegerField(_('commentcount'), default=0)
    ratecount = models.IntegerField(_('ratecount'), default=0)
    reportcount = models.IntegerField(_('reportcount'), default=0)
    score = models.FloatField(_('score'), default=0)
    deleted = models.BooleanField(_('deleted'), default=False)
    receive_notifications = models.BooleanField(_('receive notifications'), default=True, blank=True)
    status = models.PositiveSmallIntegerField(
        _('status'), max_length=1,
        default=STATUS_CHOICES.OPEN, choices=STATUS_CHOICES)
    closed_date = models.DateTimeField(
        _('closed date'), null=True, blank=True)
    feedback_response = models.TextField(
        _('feedback response'), blank=True, default='')
    is_featured = models.BooleanField(_('is featured'), default=False)

    def __unicode__(self):
        return self.details

    class Meta:
        app_label = "market"

    def save(self, *args, **kwargs):
        if not self.closed_date and (
                self.status == self.STATUS_CHOICES.CLOSED_BY_USER or
                self.status == self.STATUS_CHOICES.CLOSED_BY_ADMIN):
            self.closed_date = now()
        super(MarketItem, self).save(*args, **kwargs)

    @property
    def item_type_display(self):
        return unicode(_(self.item_type[0].upper() + self.item_type[1:].lower()))

    def getdict(self, request=None):
        adict = {'fields': {}, 'pk': self.id}
        adict['fields']['pk'] = self.id
        adict['fields']['item_type'] = self.item_type
        adict['fields']['item_type_display'] = self.item_type_display
        adict['fields']['interests'] = [ob.id for ob in self.interests.all()]
        adict['fields']['title'] = self.title
        adict['fields']['details'] = self.details
        adict['fields']['pub_date'] = str(self.pub_date)
        adict['fields']['owner'] = [self.owner.username]
        adict['fields']['ownerid'] = [self.owner.id]
        adict['fields']['url'] = self.url
        adict['fields']['close_url'] = reverse('close_marketitem', args=[self.id])
        reverse_name = 'edit_request' if self.item_type == MarketItem.TYPE_CHOICES.REQUEST else 'edit_offer'
        adict['fields']['edit_url'] = reverse(reverse_name, args=[self.id])
        adict['fields']['report_url'] = reverse('report_post', args=[self.id])
        adict['fields']['attributes_url'] = reverse('set_item_attributes_for_user', args=[self.id])
        adict['fields']['commentcount'] = self.commentcount
        adict['fields']['usercore'] = self.owner.userprofile.score if hasattr(self.owner, 'userprofile') else 0
        adict['fields']['userratecount'] = self.owner.userprofile.ratecount if hasattr(self.owner, 'userprofile') else 0
        adict['fields']['ratecount'] = self.ratecount
        adict['fields']['score'] = self.score
        if request:
            adict['fields']['hidden'] = self.marketitemhidden_set.filter(viewer_id=request.user.id).exists()
            adict['fields']['stick'] = self.marketitemstick_set.filter(viewer_id=request.user.id,
                                                                       item_id=self.id).exists()
            adict['fields']['avatar'] = reverse('avatar_render_primary', args=[self.owner.username, 80])
            adict['fields']['hasEdit'] = request.user.id == self.owner.id
        else:
            adict['fields']['hidden'] = False
            adict['fields']['stick'] = False
            adict['fields']['avatar'] = False
            adict['fields']['hasEdit'] = False
        return adict


class MarketItemHidden(models.Model):
    item = models.ForeignKey(MarketItem)
    viewer = models.ForeignKey(user_models.User)

    class Meta:
        app_label = "market"


class MarketItemStick(models.Model):
    item = models.ForeignKey(MarketItem)
    viewer = models.ForeignKey(user_models.User)

    class Meta:
        app_label = "market"


class MarketItemActions(models.Model):
    market_item = models.ForeignKey(
        MarketItem, verbose_name=_('market item'))
    action = models.TextField(_('action'))
    date_of_action = models.DateTimeField(_('date of action'), default=now)

    class Meta:
        app_label = 'market'
        verbose_name = _('actions of market item')
        verbose_name_plural = _('actions of market item')

    def __unicode__(self):
        return u'%s / %s' % (self.id or '', self.date_of_action)


class MarketItemNextSteps(models.Model):
    market_item = models.ForeignKey(
        MarketItem, verbose_name=_('market item'))
    next_step = models.TextField(_('next step'))
    date_of_action = models.DateTimeField(_('date of action'), default=now)
    completed = models.BooleanField(_('completed'), default=False)

    class Meta:
        app_label = 'market'
        verbose_name = _('next step of market item')
        verbose_name_plural = _('next steps of market item')

    def __unicode__(self):
        return u'%s / %s' % (self.next_step, self.date_of_action)
