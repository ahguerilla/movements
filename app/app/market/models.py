from datetime import datetime

import app.users as users
from django import forms
from django.db import models
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from json_field import JSONField
import tinymce

import django.contrib.auth as auth


def resouse_upload_path_handler(instance, filename):
    return 'resource_files/{file}'.format(file=str(uuid.uuid1())+filename[-4:])


class MarketItemBase(models.Model):
    owner = models.ForeignKey(auth.models.User,blank=True)
    title = models.CharField(_('title'),max_length=200,blank=False)
    details = tinymce.models.HTMLField(_('details'),blank=False)
    ip_address = models.GenericIPAddressField(_('publisher IP address when submited'),blank=True)
    countries = models.ManyToManyField(users.models.Countries)
    issues = models.ManyToManyField(users.models.Issues)
    comments = JSONField(blank=True)
    published = models.BooleanField(_('is published?'),default=True)
    pub_date = models.DateTimeField(_('publish date'),default=datetime.now())
    exp_date = models.DateTimeField(_('expiry date'))

    def __unicode__(self):
        return self.details

    class Meta:
        ordering = ['pub_date']
        abstract = True


class Resource(MarketItemBase):
    skills = models.ManyToManyField(users.models.Skills)
    url = models.CharField(_('URL Link'),max_length=500, blank=True)
    afile = models.FileField(upload_to=resouse_upload_path_handler, blank=True)

    def save(self, *args, **kwargs):
        model = self.__class__
        try:
            this = Resource.objects.get(id=self.id)
            if this.afile != self.afile:
                this.afile.delete(save=False)
        except:
            return


class Offer(MarketItemBase):
    skills = models.ManyToManyField(users.models.Skills)


class Request(MarketItemBase):
    pass
