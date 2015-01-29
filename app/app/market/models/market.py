from datetime import datetime
from django.utils import translation
from django.utils.timezone import timedelta
import app.users.models as user_models
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
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
    specific_skill = models.CharField(_('Specific skill'), max_length=30, blank=True, null=True)
    url = models.CharField(_('URL Link'), max_length=500, blank=True)
    published = models.BooleanField(_('is published?'), default=True)
    pub_date = models.DateTimeField(_('publish date'), default=datetime.now)
    commentcount = models.IntegerField(_('commentcount'), default=0)
    collaboratorcount = models.IntegerField(_('collaboratorcount'), default=0)
    ratecount = models.IntegerField(_('ratecount'), default=0)
    reportcount = models.IntegerField(_('reportcount'), default=0)
    score = models.FloatField(_('score'), default=0)
    deleted = models.BooleanField(_('deleted'), default=False)
    receive_notifications = models.BooleanField(_('receive notifications'), default=True, blank=True)
    tweet_permission = models.BooleanField(_('Tweet Permission'), default=True, blank=True)
    status = models.PositiveSmallIntegerField(
        _('status'), max_length=1,
        default=STATUS_CHOICES.OPEN, choices=STATUS_CHOICES)
    closed_date = models.DateTimeField(
        _('closed date'), null=True, blank=True)
    feedback_response = models.TextField(
        _('feedback response'), blank=True, default='')
    is_featured = models.BooleanField(_('is featured'), default=False)
    featured_order_hint = models.CharField(max_length=5, default='c')
    language = models.CharField(_('source language'), max_length=10, blank=False, default='en')

    def __unicode__(self):
        return self.details

    class Meta:
        app_label = "market"

    def is_closed(self):
        if self.status == self.STATUS_CHOICES.CLOSED_BY_USER or self.status == self.STATUS_CHOICES.CLOSED_BY_ADMIN:
            return True
        return False

    def save(self, *args, **kwargs):
        if not self.closed_date and (
                self.status == self.STATUS_CHOICES.CLOSED_BY_USER or
                self.status == self.STATUS_CHOICES.CLOSED_BY_ADMIN):
            self.closed_date = now()
        super(MarketItem, self).save(*args, **kwargs)

    @property
    def item_type_display(self):
        return unicode(_(self.item_type[0].upper() + self.item_type[1:].lower()))

    def getdict_safe(self):
        adict = {'fields': {}, 'pk': self.id}
        adict['fields']['pk'] = self.id
        adict['fields']['is_safe'] = True
        adict['fields']['item_type'] = self.item_type
        adict['fields']['item_type_display'] = self.item_type_display
        adict['fields']['interests'] = [ob.id for ob in self.interests.all()]
        adict['fields']['title'] = self.title
        adict['fields']['pub_date'] = str(self.pub_date)
        adict['fields']['owner'] = [self.owner.username]
        adict['fields']['ownerid'] = [self.owner.id]
        adict['fields']['url'] = self.url
        adict['fields']['commentcount'] = self.commentcount
        adict['fields']['collaboratorcount'] = self.collaboratorcount
        adict['fields']['hidden'] = False
        adict['fields']['stick'] = False
        adict['fields']['avatar'] = False
        adict['fields']['hasEdit'] = False
        adict['fields']['close_url'] = ""
        adict['fields']['edit_url'] = ""
        adict['fields']['report_url'] = ""
        adict['fields']['attributes_url'] = ""
        adict['fields']['translate_language_url'] = ""
        adict['fields']['tweet_permission'] = self.tweet_permission
        return adict

    def getdict(self, request=None):
        adict = self.getdict_safe()
        adict['fields']['is_safe'] = False
        adict['fields']['details'] = self.details
        adict['fields']['close_url'] = reverse('close_marketitem', args=[self.id])
        reverse_name = 'edit_request' if self.item_type == MarketItem.TYPE_CHOICES.REQUEST else 'edit_offer'
        adict['fields']['edit_url'] = reverse(reverse_name, args=[self.id])
        adict['fields']['report_url'] = reverse('report_post', args=[self.id])
        adict['fields']['attributes_url'] = reverse('set_item_attributes_for_user', args=[self.id])
        adict['fields']['translate_language_url'] = \
            reverse('translate_market_item', args=[self.id, translation.get_language()])
        adict['fields']['usercore'] = self.owner.userprofile.score if hasattr(self.owner, 'userprofile') else 0
        adict['fields']['userratecount'] = self.owner.userprofile.ratecount if hasattr(self.owner, 'userprofile') else 0
        adict['fields']['ratecount'] = self.ratecount
        adict['fields']['score'] = self.score
        adict['fields']['tweet_permission'] = self.tweet_permission
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


class MarketItemViewCounter(models.Model):
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


class MarketItemTranslation(models.Model):
    STATUS_CHOICES = EnumChoices(
        GOOGLE=(1, _('In translation')),
        PENDING=(2, _('Pending a translator')),
        TRANSLATION=(3, _('In correction')),
        DONE=(4, _('Waiting for approval')),
    )

    market_item = models.ForeignKey(
        MarketItem, verbose_name=_('market item'))
    language = models.CharField(_('language'), max_length=10, blank=False)
    source_language = models.CharField(_('source language'), max_length=10, blank=False, default='en')
    title_translated = models.TextField(_('title translated'), blank=False)
    details_translated = models.TextField(_('details translated'), blank=False)
    generated_at = models.DateField(_('date generated'), auto_now_add=True)
    status = models.PositiveSmallIntegerField(
        _('status'), max_length=1,
        default=STATUS_CHOICES.GOOGLE, choices=STATUS_CHOICES)
    owner = models.ForeignKey(
        auth.models.User, blank=True, null=True)

    class Meta:
        app_label = 'market'

    def is_done(self):
        return self.status == self.STATUS_CHOICES.DONE

    def set_done_or_pending(self, save=True):
        if not self.is_done():
            self.status = self.STATUS_CHOICES.PENDING
        if save:
            self.save()

class MarketItemCollaborators(models.Model):
    market_item = models.ForeignKey(
        MarketItem, verbose_name=_('market item'))
    collaborator = models.ForeignKey(
        auth.models.User, blank=True, null=True)
    interaction_type = models.CharField(_('item_type'), max_length=50, blank=False)
    interaction_date = models.DateTimeField(_('interaction date'), auto_now_add=True)

    class Meta:
        app_label = 'market'


class TranslationMixin(models.Model):
    STATUS_CHOICES = EnumChoices(
        ACTIVE=(1, _('In translation')),
        CORRECTION=(2, _('In correction')),
        APPROVAL=(3, _('Waiting for approval')),
    )

    class Meta:
        app_label = 'market'
        abstract = True

    details_translated = models.TextField(_('details translated'), blank=False)
    language = models.CharField(_('language'), max_length=10, blank=False)
    status = models.PositiveSmallIntegerField(
        _('status'), max_length=1,
        default=STATUS_CHOICES.ACTIVE, choices=STATUS_CHOICES)
    created = models.DateTimeField(_('date generated'), auto_now_add=True)
    edited = models.DateTimeField(_('date edited'), auto_now=True)
    owner = models.ForeignKey(
        auth.models.User, blank=True, null=True)
    reminder = models.BooleanField(_('Reminder status'), default=False)

    def __unicode__(self):
        return u'%s' % self.created.strftime('%H:%M on %d %b %Y')

    def is_active(self, user):
        return user == self.owner and self.status != self.STATUS_CHOICES.APPROVAL

    def mark_to_approval(self, save=True):
        self.status = self.STATUS_CHOICES.APPROVAL
        if save:
            self.save()

    def endtime(self):
        # TODO need to move timings to settings
        if self.status == self.STATUS_CHOICES.ACTIVE:
            return self.edited + timedelta(minutes=2)
        elif self.status == self.STATUS_CHOICES.CORRECTION:
            return self.edited + timedelta(minutes=1)
        return None


class TraslationCandidade(TranslationMixin):
    translation = models.ForeignKey(
        MarketItemTranslation, verbose_name=_('translation'), null=True)
    market_item = models.ForeignKey(
        MarketItem, verbose_name=_('market item'))
    title_translated = models.TextField(_('title translated'), blank=False)

    def take_off_url(self):
        return reverse('take_off_translate_item', args=(self.market_item_id, self.language))

    def done_url(self):
        return reverse('mark_as_done', args=(self.market_item_id, self.language))

    def approval_url(self):
        return reverse('approve_translation', args=(self.market_item_id, self.language))

    def revoke_url(self):
        return reverse('revoke_translation', args=(self.market_item_id, self.language))

    def correction_url(self):
        return reverse('request_corrections', args=(self.market_item_id, self.language))

    def cm_urls_dict(self):
        return {'approval_url': self.approval_url(),
                'revoke_url': self.revoke_url(),
                'correction_url': self.correction_url(),
                }
