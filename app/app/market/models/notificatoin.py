from django.db import models
from django.utils.translation import ugettext_lazy as _
from .market import MarketItem
from django.contrib.auth.models import User
from datetime import datetime
from django.core.urlresolvers import reverse



class Notification(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(MarketItem)
    seen = models.BooleanField()
    text = models.CharField(_('text'),max_length=500)
    pub_date = models.DateTimeField(_('publish date'), default=datetime.now)

    class Meta:
        app_label="market"
        ordering = ['-pub_date']
        
        
    def getDict(self):
        adict={}
        adict['user']=self.user.username
        adict['user_id'] = self.user.id
        adict['item'] = self.item.title
        adict['item_type'] = self.item.item_type
        adict['item_id'] = self.item.id
        adict['owner'] = self.item.owner.username
        adict['owner_id'] = self.item.owner.id
        adict['seen'] = self.seen
        adict['text']= self.text
        adict['pub_date'] = str(self.pub_date)
        adict['avatar'] = reverse('avatar_render_primary', args=[self.item.owner.username,30])
        return adict