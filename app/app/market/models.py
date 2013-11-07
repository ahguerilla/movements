import tinymce
from django import forms
from django.db import models
from datetime import datetime
from json_field import JSONField
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
import app.users.models as UserModels


def resouse_upload_path_handler(instance, filename):
    return 'resource_files/{file}'.format(file=str(uuid.uuid1())+filename[-4:])


class MarketItemBase(models.Model):
    details = tinymce.models.HTMLField(_('details'),blank=False)
    ip_address = models.IPAddressField(_('publisher IP address when submited'))
    countries = models.ManyToManyField(UserModels.Countries)
    issues = models.ManyToManyField(UserModels.Issues)
    comments = JSONField()
    published = models.BooleanField(_('is published?'),default=True)
    pub_date = models.DateTimeField(_('publish date'),default=datetime.now())

    def __unicode__(self):
        return self.details

    class Meta:
        ordering = ['pub_date']


class Resource(MarketItemBase):
    skills = models.ManyToManyField(UserModels.Skills)
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
    skills = models.ManyToManyField(UserModels.Skills)


class Request(MarketItemBase):
    pass
