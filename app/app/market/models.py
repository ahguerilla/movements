from datetime import datetime
import app.users as users
from django.db import models
from django.db.models import Q

from django.utils.translation import ugettext_lazy as _
import tinymce

import django.contrib.auth as auth
import uuid

from django.core.urlresolvers import reverse


def resouse_upload_path_handler(instance, filename):
    return 'resource_files/{file}'.format(file=str(uuid.uuid1())+filename[-4:])


class MarketItem(models.Model):
    item_type = models.CharField(_('item_type'), max_length=200, blank=False)
    owner = models.ForeignKey(auth.models.User, blank=True)
    title = models.CharField(_('title'), max_length=200, blank=False)
    details = tinymce.models.HTMLField(_('details'), blank=False)
    countries = models.ManyToManyField(users.models.Countries)
    issues = models.ManyToManyField(users.models.Issues)
    skills = models.ManyToManyField(users.models.Skills)
    url = models.CharField(_('URL Link'), max_length=500, blank=True)
    published = models.BooleanField(_('is published?'), default=True)
    pub_date = models.DateTimeField(_('publish date'), default=datetime.now)
    exp_date = models.DateTimeField(_('expiry date'))
    commentcount = models.IntegerField(_('commentcount'), default=0)
    ratecount = models.IntegerField(_('ratecount'), default=0)
    reportcount = models.IntegerField(_('reportcount'), default=0)
    score = models.FloatField(_('score'),default=0)
    deleted = models.BooleanField(_('deleted'), default=False)

    def __unicode__(self):
        return self.details

    #class Meta:
        #ordering = ['-pub_date']

    def getdict(self):
        adict = {'fields':{}}
        adict['pk'] = self.id
        adict['fields']['item_type'] = self.item_type
        adict['fields']['issues']= [ob.id for ob in self.issues.all()]
        adict['fields']['countries']= [ob.id for ob in self.countries.all()]
        adict['fields']['skills']= [ob.id for ob in self.skills.all()]
        adict['fields']['title']= self.title
        adict['fields']['details']= self.details
        adict['fields']['pub_date']= str(self.pub_date)
        adict['fields']['exp_date']= str(self.exp_date)
        adict['fields']['owner']= [self.owner.username]
        adict['fields']['url']= self.url
        adict['fields']['files']= [afile.url for afile in self.files.all()]
        adict['fields']['commentcount']= self.commentcount
        adict['fields']['usercore']= self.owner.userprofile.score
        adict['fields']['userratecount']= self.owner.userprofile.ratecount
        adict['fields']['ratecount']= self.ratecount
        adict['fields']['score']= self.score
        adict['fields']['avatar'] = '/static/images/male200.png'
        #reverse('avatar_render_primary', args=[obj.owner.username,80])
        return adict


class Comment(models.Model):
    owner = models.ForeignKey(auth.models.User, blank=True)
    contents = tinymce.models.HTMLField(_('contents'), blank=False)
    pub_date = models.DateTimeField(_('publish date'), default=datetime.now)
    item = models.ForeignKey(MarketItem, null=True, blank=True, related_name='comments')
    published = models.BooleanField(_('is published?'), default=True)
    deleted = models.BooleanField(_('deleted'), default=False)


    class Meta:
        ordering = ['-pub_date']

    def save(self, *args, **kwargs):
        model = self.__class__
        self.item.commentcount+=1
        self.item.save()

    def getdict(self):
        adict={'fields':{}}
        adict['fields']['pub_date'] = str(self.pub_date)
        adict['fields']['contents'] = self.contents
        adict['pk'] = self.id
        adict['fields']['owner'] = self.owner.id
        adict['fields']['avatar'] = '/static/images/male200.png'
        #reverse('avatar_render_primary', args=[self.owner.username,80])
        adict['fields']['username'] = self.owner.username
        adict['fields']['profile_url'] = reverse('user_profile_for_user', args=[self.owner.username])
        return adict



class File(models.Model):
    filename = models.CharField(_('file name'),max_length=255)
    afile = models.FileField(upload_to=resouse_upload_path_handler, blank=True)
    item = models.ForeignKey(MarketItem, related_name="files")


class ItemRate(models.Model):
    owner = models.ForeignKey(auth.models.User, blank=True)
    item = models.ForeignKey(MarketItem, null=True, blank=True, related_name='rates')
    pub_date = models.DateTimeField(_('publish date'), default=datetime.now)
    title = models.CharField(_('title'),max_length=200,blank=False)
    score = models.IntegerField(_('score'),default=0)

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


class MarketItemPostReport(models.Model):
    owner = models.ForeignKey(auth.models.User, blank=True)
    item = models.ForeignKey(MarketItem, null=True, blank=True, related_name='repots')
    contents = tinymce.models.HTMLField(_('contents'), blank=False)
    resolved = models.BooleanField(_('is resolved'), default=False)
    pub_date = models.DateTimeField(_('publish date'), default=datetime.now)
    published = models.BooleanField(_('is published?'), default=True)

    class Meta:
        ordering = ['-resolved', '-pub_date']

    def save(self, *args, **kwargs):
        self.item.reportcount += 1
        self.item.save()