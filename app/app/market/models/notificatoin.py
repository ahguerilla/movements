from django.db import models
from django.utils.translation import ugettext_lazy as _
from .market import MarketItem
from .comment import Comment
from django.contrib.auth.models import User
from datetime import datetime
from django.core.urlresolvers import reverse
from json_field import JSONField



class Notification(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(MarketItem, null=True, blank=True)    
    comment = models.ForeignKey(Comment, null=True, blank=True)    
    seen = models.BooleanField()
    read = models.BooleanField()
    avatar_user = models.CharField(_('avatar user'),max_length=255, null=True, blank=True)
    text = JSONField()
    pub_date = models.DateTimeField(_('publish date'), default=datetime.now)

    class Meta:
        app_label="market"
        ordering = ['-pub_date']
        
        
    def getDict(self):
        adict={}
        adict['user']=self.user.username
        adict['user_id'] = self.user.id
        adict['item'] = self.item.title
        adict['item_type'] = self.item.item_type if self.item else None
        adict['item_title'] = self.item.title if self.item else None
        adict['item_id'] = self.item.id if self.item else None
        adict['owner'] = self.item.owner.username if self.item else None
        adict['owner_id'] = self.item.owner.id if self.item else None
        adict['seen'] = self.seen
        adict['read'] = self.read
        adict['text']= self.text
        adict['pub_date'] = str(self.pub_date)[0:16]
        adict['avatar'] = reverse('avatar_render_primary', args=[self.avatar_user if self.avatar_user!=None else self.item.owner.username,30])
        adict['comment'] = self.comment.id if self.comment else None
        adict['comment_user'] = self.comment.owner.username if self.comment else None
        adict['comment_user_id'] = self.comment.owner.id if self.comment else None
        return adict