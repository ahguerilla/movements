import logging
import uuid
from io import BytesIO, StringIO

import django.contrib.auth as auth
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from easy_thumbnails.files import get_thumbnailer
from pexif import JpegFile
from PIL import Image
from sorl.thumbnail import ImageField
from tinymce import models as tinymodels

import app.users.models as user_models
from app.utils import EnumChoices
from app.market.utils import fetch_graph_data
from urllib2 import URLError
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

_logger = logging.getLogger('movements-alerts')


class MarketItem(models.Model):
    STATUS_OPEN = 0
    STATUS_WATCH = 1
    STATUS_URGENT = 2
    STATUS_CHOICES = EnumChoices(
        OPEN=(0, _('Open')),
        WATCH=(1, _('Watch')),
        URGENT=(2, _('Urgent')),
        CLOSED_BY_ADMIN=(3, _('Closed By Admin')),
        CLOSED_BY_USER=(4, _('Closed By User')),
    )
    TYPE_CHOICES = EnumChoices(
        REQUEST=('request', _('Request')),
        OFFER=('offer', _('Offer')),
        NEWS=('news', _('News')),
    )

    item_type = models.CharField(_('item_type'), max_length=50, blank=False)
    owner = models.ForeignKey(auth.models.User, blank=True)
    staff_owner = models.ForeignKey(
        auth.models.User, blank=True, null=True, related_name='marketitems', verbose_name='Staff Manager')
    title = models.CharField(_('title'), max_length=200, blank=False)
    details = tinymodels.HTMLField(_('details'), blank=False)
    interests = models.ManyToManyField(user_models.Interest, null=True, blank=True)
    specific_skill = models.CharField(_('Specific skill'), max_length=30, blank=True, null=True)
    countries = models.ManyToManyField(user_models.Countries, null=True, blank=True)
    issues = models.ManyToManyField(user_models.Issues, null=True, blank=True)
    specific_issue = models.CharField(_('Specific issue'), max_length=30, blank=True, null=True)
    url = models.CharField(_('URL Link'), max_length=500, blank=True)
    published = models.BooleanField(_('is published?'), default=True)
    pub_date = models.DateTimeField(_('publish date'), auto_now_add=True)
    pub_date.editable = True
    commentcount = models.IntegerField(_('commentcount'), default=0)
    collaboratorcount = models.IntegerField(_('collaboratorcount'), default=0)
    ratecount = models.IntegerField(_('ratecount'), default=0)
    reportcount = models.IntegerField(_('reportcount'), default=0)
    score = models.FloatField(_('score'), default=0)
    deleted = models.BooleanField(_('deleted'), default=False)
    receive_notifications = models.BooleanField(_('receive notifications'), default=True, blank=True)
    tweet_permission = models.BooleanField(_('Tweet Permission'), default=True, blank=True)
    status = models.PositiveSmallIntegerField(
        _('status'), max_length=1,
        default=STATUS_CHOICES.OPEN, choices=STATUS_CHOICES)
    closed_date = models.DateTimeField(
        _('closed date'), null=True, blank=True)
    feedback_response = models.TextField(
        _('feedback response'), blank=True, default='')
    is_featured = models.BooleanField(_('is featured'), default=False)
    featured_order_hint = models.CharField(max_length=5, default='c')
    language = models.CharField(_('source language'), max_length=10, blank=False, default='en')

    def __unicode__(self):
        return self.details

    class Meta:
        app_label = "market"

    def init_url(self, lang):
        return reverse('translation:market:init', args=(self.pk, lang))

    def is_closed(self):
        if self.status == self.STATUS_CHOICES.CLOSED_BY_USER or self.status == self.STATUS_CHOICES.CLOSED_BY_ADMIN:
            return True
        return False

    def save(self, *args, **kwargs):
        if not self.closed_date and (
                self.status == self.STATUS_CHOICES.CLOSED_BY_USER or
                self.status == self.STATUS_CHOICES.CLOSED_BY_ADMIN):
            self.closed_date = timezone.now()
        super(MarketItem, self).save(*args, **kwargs)

    @property
    def item_type_display(self):
        return unicode(_(self.item_type[0].upper() + self.item_type[1:].lower()))

    def getdict_safe(self):
        adict = {'fields': {}, 'pk': self.id}
        adict['fields']['pk'] = self.id
        adict['fields']['is_safe'] = True
        adict['fields']['item_type'] = self.item_type
        adict['fields']['item_type_display'] = self.item_type_display
        adict['fields']['interests'] = [ob.id for ob in self.interests.all()]
        adict['fields']['title'] = self.title
        adict['fields']['pub_date'] = str(self.pub_date)
        adict['fields']['owner'] = [self.owner.username]
        adict['fields']['ownerid'] = [self.owner.id]
        adict['fields']['url'] = self.url
        adict['fields']['commentcount'] = self.commentcount
        adict['fields']['collaboratorcount'] = self.collaboratorcount
        adict['fields']['hidden'] = False
        adict['fields']['stick'] = False
        adict['fields']['avatar'] = False
        adict['fields']['hasEdit'] = False
        adict['fields']['close_url'] = ""
        adict['fields']['unpublish_url'] = ""
        adict['fields']['edit_url'] = ""
        adict['fields']['report_url'] = ""
        adict['fields']['attributes_url'] = ""
        adict['fields']['translate_language_url'] = ""
        adict['fields']['tweet_permission'] = self.tweet_permission
        if hasattr(self, 'image_url') and self.image_url is not None:
            try:
                thumbnailer = get_thumbnailer(self.image_url)
                adict['fields']['image_url'] = thumbnailer.get_thumbnail({'size': (66, 66),
                                                                          'upscale': True,
                                                                          'crop': '0, 0',
                                                                          'background': '#FFFFFF'}).url
            except Exception as ex:
                _logger.exception(ex)
                adict['fields']['image_url'] = False
        else:
            adict['fields']['image_url'] = False
        return adict

    def getdict(self, request=None):
        adict = self.getdict_safe()
        adict['fields']['is_safe'] = False
        adict['fields']['details'] = self.details
        adict['fields']['close_url'] = reverse('close_marketitem', args=[self.id])
        adict['fields']['unpublish_url'] = reverse('unpublish_marketitem', args=[self.id])
        adict['fields']['edit_url'] = reverse('edit_post', args=[self.id])
        adict['fields']['report_url'] = reverse('report_post', args=[self.id])
        adict['fields']['attributes_url'] = reverse('set_item_attributes_for_user', args=[self.id])
        adict['fields']['translate_language_url'] = \
            reverse('translation:market:translate', args=[self.id])
        adict['fields']['language'] = self.language
        adict['fields']['usercore'] = self.owner.userprofile.score if hasattr(self.owner, 'userprofile') else 0
        adict['fields']['userratecount'] = self.owner.userprofile.ratecount if hasattr(self.owner, 'userprofile') else 0
        adict['fields']['ratecount'] = self.ratecount
        adict['fields']['score'] = self.score
        adict['fields']['tweet_permission'] = self.tweet_permission
        if request:
            adict['fields']['hidden'] = self.marketitemhidden_set.filter(viewer_id=request.user.id).exists()
            adict['fields']['stick'] = self.marketitemstick_set.filter(viewer_id=request.user.id,
                                                                       item_id=self.id).exists()
            adict['fields']['avatar'] = reverse('avatar_render_primary', args=[self.owner.username, 80])
            adict['fields']['hasEdit'] = request.user.id == self.owner.id
        else:
            adict['fields']['hidden'] = False
            adict['fields']['stick'] = False
            adict['fields']['avatar'] = False
            adict['fields']['hasEdit'] = False
        return adict

    def generate_news_item(self, url):
        news_item = MarketNewsItemData.fetch_news_item(url)
        news_item.market_item = self
        news_item.save()


class MarketItemHowCanYouHelp(models.Model):
    item = models.ForeignKey(MarketItem)
    title = models.CharField(max_length=50)
    text = models.TextField()

    class Meta:
        app_label = "market"
        verbose_name_plural = "Extra how you can help entries"
        verbose_name = "How you can help entry"


def market_image_upload_handler(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return "post/{0}/images/{1}".format(instance.item.id, filename)


class MarketItemImage(models.Model):
    VALID_EXTENSIONS = ['jpg', 'jpeg', 'png']
    MAX_SIZE = 5000000

    item = models.ForeignKey(MarketItem)
    image = ImageField(upload_to=market_image_upload_handler)
    original = ImageField(upload_to=market_image_upload_handler)
    original_metadata = models.TextField()

    class Meta:
        app_label = "market"

    def _set_thumbnail(self, filename, data):
        pil_image = Image.open(data)
        with BytesIO() as thumb:
            if pil_image.mode != "RGB":
                pil_image.convert('RGB')
            pil_image.thumbnail(pil_image.size)
            pil_image.save(thumb, 'JPEG')
            thumb.seek(0)
            self.image = SimpleUploadedFile(filename, thumb.getvalue(), content_type='image/jpeg')

    @staticmethod
    def validate_image(image_data):
        try:
            if image_data.size > MarketItemImage.MAX_SIZE:
                raise ValueError(u'Uploaded image greater than max size of 5MB, size uploaded was: ' +
                                 unicode(image_data.size))
            ext = image_data.name.split('.')[-1]
            if ext.lower() not in MarketItemImage.VALID_EXTENSIONS:
                raise ValueError(u'Image upload with invalid extension: ' + ext)
        except Exception as ex:
            _logger.exception(ex)
            return False
        return True

    @staticmethod
    def save_image(market_item, image_data):
        if not MarketItemImage.validate_image(image_data):
            return False
        image = MarketItemImage(item=market_item)
        try:
            with BytesIO() as data:
                data.write(image_data.read())
                data.seek(0)
                ext = image_data.name.split('.')[-1]
                if ext.lower() in ['jpg', 'jpeg']:
                    with BytesIO() as output:
                        ef = JpegFile(data, "posted_file")
                        ef.dump(output)
                        image.original_metadata = output.getvalue()
                        ef.remove_metadata(paranoid=True)
                    with BytesIO() as sanitised:
                        ef.writeFd(sanitised)
                        sanitised.seek(0)
                        image._set_thumbnail(image_data.name, sanitised)
                else:
                    image._set_thumbnail(image_data.name, data)
            image.original = image_data
            image.save()
        except Exception as ex:
            _logger.exception(ex)
            return False


class MarketItemSalesforceRecord(models.Model):
    item = models.OneToOneField(MarketItem, related_name='salesforce')
    salesforce_record_id = models.CharField(max_length=64)
    last_updated = models.DateTimeField()
    needs_updating = models.BooleanField()

    class Meta:
        app_label = "market"

    @classmethod
    def mark_for_update(cls, market_id):
        MarketItemSalesforceRecord.objects \
            .filter(item_id=market_id) \
            .update(needs_updating=True)


class MarketItemHidden(models.Model):
    item = models.ForeignKey(MarketItem)
    viewer = models.ForeignKey(user_models.User)

    class Meta:
        app_label = "market"


class MarketItemStick(models.Model):
    item = models.ForeignKey(MarketItem)
    viewer = models.ForeignKey(user_models.User)

    class Meta:
        app_label = "market"


class MarketItemViewCounter(models.Model):
    item = models.ForeignKey(MarketItem)
    viewer = models.ForeignKey(user_models.User)

    class Meta:
        app_label = "market"


class MarketItemActions(models.Model):
    market_item = models.ForeignKey(
        MarketItem, verbose_name=_('market item'))
    action = models.TextField(_('action'))
    date_of_action = models.DateTimeField(_('date of action'), auto_now_add=True)

    class Meta:
        app_label = 'market'
        verbose_name = _('actions of market item')
        verbose_name_plural = _('actions of market item')

    def __unicode__(self):
        return u'%s / %s' % (self.id or '', self.date_of_action)


class MarketItemNextSteps(models.Model):
    market_item = models.ForeignKey(
        MarketItem, verbose_name=_('market item'))
    next_step = models.TextField(_('next step'))
    date_of_action = models.DateTimeField(_('date of action'), auto_now_add=True)
    completed = models.BooleanField(_('completed'), default=False)

    class Meta:
        app_label = 'market'
        verbose_name = _('next step of market item')
        verbose_name_plural = _('next steps of market item')

    def __unicode__(self):
        return u'%s / %s' % (self.next_step, self.date_of_action)


class MarketItemCollaborators(models.Model):
    market_item = models.ForeignKey(
        MarketItem, verbose_name=_('market item'))
    collaborator = models.ForeignKey(
        auth.models.User, blank=True, null=True)
    interaction_type = models.CharField(_('item_type'), max_length=50, blank=False)
    interaction_date = models.DateTimeField(_('interaction date'), auto_now_add=True)

    class Meta:
        app_label = 'market'


class MarketNewsItemData(models.Model):
    market_item = models.OneToOneField(MarketItem, verbose_name=_('market item'))
    original_url = models.URLField(max_length=500)
    last_scraped = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=500)
    url = models.URLField(max_length=500)
    type = models.CharField(max_length=50)
    image = models.URLField(max_length=500, null=True, blank=True)
    description = models.TextField()
    site_name = models.CharField(max_length=100)
    published = models.CharField(max_length=50, null=True, blank=True)
    author_url = models.URLField(max_length=500, null=True, blank=True)
    author_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        app_label = 'market'

    def __unicode__(self):
        return u'%s - %s' % (self.site_name, self.title)

    @classmethod
    def fetch_news_item(cls, url):
        try:
            validate = URLValidator()
            validate(url)
            graph_data = fetch_graph_data(url)
        except ValidationError:
            raise ValueError
        except URLError:
            raise ValueError
        if not graph_data.is_valid():
            raise ValueError

        obj = cls(original_url=url,
                  title=graph_data.title,
                  url=graph_data.url,
                  type=graph_data.type,
                  image=graph_data.image,
                  description=graph_data.description,
                  site_name=graph_data.site_name)
        if hasattr(graph_data, 'published'):
            obj.published = graph_data.published
        elif hasattr(graph_data, 'published_time'):
            obj.published = graph_data.published_time
        elif hasattr(graph_data, 'published_date'):
            obj.published = graph_data.published_date

        if hasattr(graph_data, 'author'):
            obj.author_url = graph_data.author
            try:
                validate = URLValidator()
                validate(graph_data.author)
                author_graph_data = fetch_graph_data(graph_data.author)
                if hasattr(author_graph_data, 'title'):
                    obj.author_name = author_graph_data.title
            except ValidationError:
                obj.author_url = None
                obj.author_name = graph_data.author
            except URLError:
                pass
        return obj