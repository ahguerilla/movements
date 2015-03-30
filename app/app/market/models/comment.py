from datetime import datetime
from django.db import models
from django.db.models import F
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
import django.contrib.auth as auth
import tinymce

from .market import MarketItem
# from app.utils import EnumChoices


class Comment(models.Model):
    owner = models.ForeignKey(auth.models.User, blank=True)
    contents = tinymce.models.HTMLField(_('contents'), blank=False)
    pub_date = models.DateTimeField(_('publish date'), default=datetime.now)
    item = models.ForeignKey(MarketItem, null=True, blank=True, related_name='comments')
    published = models.BooleanField(_('is published?'), default=True)
    deleted = models.BooleanField(_('deleted'), default=False)
    language = models.CharField(_('source language'), max_length=10, blank=False, default='en')

    class Meta:
        ordering = ['-pub_date']
        app_label = "market"

    def save(self, *args, **kwargs):
        self.item.commentcount = F('commentcount') + 1
        self.item.save()
        return super(Comment, self).save(*args, **kwargs)

    def getdict(self):
        adict = {'fields': {}}
        adict['fields']['pub_date'] = str(self.pub_date)
        adict['fields']['pub_date_formatted'] = self.pub_date.strftime('%H:%M on %d %b %Y')
        adict['fields']['contents'] = self.contents
        adict['pk'] = self.id
        adict['fields']['pk'] = self.id
        adict['fields']['ownerid'] = self.owner.id
        adict['fields']['avatar'] = reverse('avatar_render_primary', args=[self.owner.username, 60])
        adict['fields']['username'] = self.owner.username
        adict['fields']['profile_url'] = reverse('user_profile_for_user', args=[self.owner.username])
        adict['fields']['delete_url'] = reverse('delete_comment')
        adict['fields']['take_in_url'] = reverse('translation:comment:take_in', args=[self.id])
        adict['fields']['translate_language_url'] = reverse('translation:comment:translate', args=[self.id])
        adict['fields']['source_lang'] = self.language
        adict['score'] = self.owner.userprofile.score
        adict['ratecount'] = self.owner.userprofile.ratecount
        return adict

    def init_url(self, lang):
        return reverse('translation:comment:init', args=(self.pk, lang))
