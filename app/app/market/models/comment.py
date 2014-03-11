from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
import django.contrib.auth as auth
import tinymce
import uuid

from .market import MarketItem


class Comment(models.Model):
    owner = models.ForeignKey(auth.models.User, blank=True)
    contents = tinymce.models.HTMLField(_('contents'), blank=False)
    pub_date = models.DateTimeField(_('publish date'), default=datetime.now)
    item = models.ForeignKey(MarketItem, null=True, blank=True, related_name='comments')
    published = models.BooleanField(_('is published?'), default=True)
    deleted = models.BooleanField(_('deleted'), default=False)


    class Meta:
        ordering = ['-pub_date']
        app_label="market"

    def save(self, *args, **kwargs):
        model = self.__class__
        self.item.commentcount+=1
        self.item.save()

    def getdict(self):
        adict={'fields':{}}
        adict['fields']['pub_date'] = str(self.pub_date)
        adict['fields']['contents'] = self.contents
        adict['pk'] = self.id
        adict['fields']['ownerid'] = self.owner.id
        adict['fields']['avatar'] = reverse('avatar_render_primary', args=[self.owner.username,80])
        adict['fields']['username'] = self.owner.username
        adict['fields']['profile_url'] = reverse('user_profile_for_user', args=[self.owner.username])
        adict['score'] = self.owner.userprofile.score
        adict['ratecount'] = self.owner.userprofile.ratecount

        return adict

