from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid
from .market import MarketItem


def resouse_upload_path_handler(instance, filename):
    return 'resource_files/{file}'.format(file=str(uuid.uuid1())+filename[-4:])

class File(models.Model):
    filename = models.CharField(_('file name'),max_length=255)
    afile = models.FileField(upload_to=resouse_upload_path_handler, blank=True)
    item = models.ForeignKey(MarketItem, related_name="files")

    class Meta:
        app_label="market"

