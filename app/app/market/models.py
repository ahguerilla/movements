from datetime import datetime
import app
import app.users as users
from django import forms
from django.db import models
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from json_field import JSONField
import tinymce

import django.contrib.auth as auth
import uuid


def resouse_upload_path_handler(instance, filename):
    return 'resource_files/{file}'.format(file=str(uuid.uuid1())+filename[-4:])


class MarketItem(models.Model):
    item_type = models.CharField(_('item_type'),max_length=200,blank=False)
    owner = models.ForeignKey(auth.models.User,blank=True)
    title = models.CharField(_('title'),max_length=200,blank=False)
    details = tinymce.models.HTMLField(_('details'),blank=False)
    countries = models.ManyToManyField(users.models.Countries)
    issues = models.ManyToManyField(users.models.Issues)
    skills = models.ManyToManyField(users.models.Skills)
    url = models.CharField(_('URL Link'),max_length=500, blank=True)
    published = models.BooleanField(_('is published?'),default=True)
    pub_date = models.DateTimeField(_('publish date'),default=datetime.now)
    exp_date = models.DateTimeField(_('expiry date'))
    commentcount = models.IntegerField(_('commentcount'),default=0)

    def __unicode__(self):
        return self.details

    class Meta:
        ordering = ['pub_date']



class Comment(models.Model):
    title = models.CharField(_('title'),max_length=200,blank=False)
    owner =  models.ForeignKey(auth.models.User,blank=True)
    contents = tinymce.models.HTMLField(_('contents'),blank=False)
    pub_date = models.DateTimeField(_('publish date'),default=datetime.now)
    item = models.ForeignKey(MarketItem,null=True,blank=True,related_name='comments')
    published = models.BooleanField(_('is published?'),default=True)

    def save(self, *args, **kwargs):
        model = self.__class__
        self.item.commentcount = Comment.objects.filter(id=self.item).count()
        super(Comment,self).save(*args,**kwargs)




class File(models.Model):
    filename = models.CharField(_('file name'),max_length=255)
    afile = models.FileField(upload_to=resouse_upload_path_handler, blank=True)
    item = models.ForeignKey(MarketItem,related_name="files")

