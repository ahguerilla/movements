from django.db import models
from django.utils.translation import ugettext_lazy as _
from .market import MarketItem
from .comment import Comment
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from json_field import JSONField
from app.utils import EnumChoices


class Notification(models.Model):
    STATUSES = EnumChoices(
        PENDING=(1, _('Needs Translation')),
        TRANSLATION=(2, _('In translation')),
        CORRECTION=(3, _('In correction')),
        REVOKED=(4, _('Translation revoked')),
        APPROVAL=(5, _('Waiting for approval')),
        APPROVED=(6, _('Approved')),
    )

    translation = models.PositiveSmallIntegerField(
        _('Translation status'), max_length=1, default=None, choices=STATUSES, null=True)

    timeto = models.DateTimeField(_('The time to completion'), null=True)
    reminder = models.BooleanField(_('Reminder'), default=False)
    user = models.ForeignKey(User)
    item = models.ForeignKey(MarketItem, null=True, blank=True)
    comment = models.ForeignKey(Comment, null=True, blank=True)
    seen = models.BooleanField(default=False)
    emailed = models.BooleanField(default=False)
    avatar_user = models.CharField(_('avatar user'), max_length=255, null=True, blank=True)
    text = JSONField()
    pub_date = models.DateTimeField(_('publish date'), auto_now_add=True)

    class Meta:
        app_label = "market"
        ordering = ['-pub_date']

    def get_dict(self):
        adict = {
            'seen': self.seen,
            'text': self.text,
            'pub_date': str(self.pub_date)[0:16],
            'user': self.avatar_user,
            'profile_link': reverse('user_profile_for_user', args=[self.avatar_user]),
            'avatar': reverse('avatar_render_primary',
                              args=[
                                  self.avatar_user if self.avatar_user is not None else self.item.owner.username,
                                  30]),
        }
        if self.translation is not None:
            adict.update({
                'translation': self.translation,
                'get_translation_display': self.get_translation_display(),
                'timeto': self.timeto.strftime('%H:%M on %d %b %Y') if self.timeto else False,
                'reminder': self.reminder,
            })
        if self.item:
            adict.update({
                'item_title': self.item.title,
                'item_type': self.item.item_type,
                'item_id': self.item.id,
                'owner': self.item.owner.username,
                'owner_id': self.item.owner.id,
                'language': self.item.language,
            })
        if self.comment:
            adict.update({
                'comment': self.comment.id,
                'comment_user': self.comment.owner.username,
                'comment_user_id': self.comment.owner.id,
                'comment_contents': self.comment.contents,
            })

        return adict
