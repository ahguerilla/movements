from datetime import datetime

from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.contrib import auth
from django.db.models.signals import post_save
from django.dispatch import receiver
import tinymce
from postman.models import Message

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


class MessageExt(Message):
    """
    - 'is_post_recommendation' (gets set to true if the message was created via
      a market item recommendation);
    - 'is_user_recommendation' as with market item recommendations, it is
      possible to recommend a user via their profile (gets set to true if the
      message was created via a user recommendation);
    - 'market_item_id' (should be null if the conversation is initiated via a
      to user private message or user recommendation)
    """
    is_post_recommendation = models.BooleanField(
        _('is post recommendation'), default=False)
    is_user_recommendation = models.BooleanField(
        _('is user recommendation'), default=False)
    market_item = models.ForeignKey(
        MarketItem, null=True, verbose_name=_('market item'), blank=True)

    class Meta:
        app_label = 'market'
        verbose_name = _('message')
        verbose_name_plural = _('messages')
        ordering = ('-sent_at', '-id')


@receiver(post_save, sender=Message)
def create_child_msg(sender, instance, **kwargs):
    # Required because the child extended model (MessageExt) displays in admin
    # instead of standard postman model. So we manually add child model.
    # FIXME: perhaps is there a standard way to do this?
    msg = MessageExt(message_ptr=instance)
    msg.__dict__.update(instance.__dict__)
    msg.is_post_recommendation = False
    msg.is_user_recommendation = False
    msg.save()


class MessagePresentation(MessageExt):
    """
    MessageExt model should be used in postman admin area.
    This is possible when set app_label = 'postman'.
    However, migrations need stored in project, not in postman app.
    So we used proxy model for this.
    """
    class Meta:
        proxy = True
        app_label = 'postman'
        verbose_name = _('message')
        verbose_name_plural = _('messages')
        ordering = ('-sent_at', '-id')
