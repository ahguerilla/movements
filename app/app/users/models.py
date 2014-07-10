from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from json_field import JSONField
import django.contrib.auth as auth
from datetime import datetime
from django.db.models import Q
from django.core.urlresolvers import reverse

from app.utils import EnumChoices


class Skills(models.Model):
    skills = models.CharField(_('skill set'), max_length=255, null=True)

    def __unicode__(self):
        return self.skills

    class Meta:
        ordering = ['skills']


class Issues(models.Model):
    issues = models.CharField(_('issues of interest'), max_length=255, null=True)

    def __unicode__(self):
        return self.issues

    class Meta:
        ordering = ['issues']


class Countries(models.Model):
    countries = models.CharField(_('countries of interest'), max_length=255, null=True)
    region = models.ForeignKey('Region', null=True)

    def __unicode__(self):
        return self.countries

    class Meta:
        ordering = ['countries']


class Nationality(models.Model):
    nationality = models.CharField(_('nationality'), max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.nationality

    class Meta:
        ordering = ['nationality']


class Residence(models.Model):
    residence = models.CharField(_('country of residence'), max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.residence

    class Meta:
        ordering = ['residence']


class NamedObject(models.Model):
    name = models.CharField(_('name'), max_length=255, default='')

    class Meta:
        abstract = True
        ordering = 'name',

    def __unicode__(self):
        return u'%s' % self.name


class Language(NamedObject):
    launguage_code = models.CharField(_('language code'), max_length=10, blank=True, null=True)
    class Meta:
        verbose_name = _('language')
        verbose_name_plural = _('languages')

    class Meta:
        ordering = ['name']


class Region(NamedObject):
    class Meta:
        verbose_name = _('region')
        verbose_name_plural = _('regions')


class Interest(NamedObject):
    class Meta:
        verbose_name = _('interest')
        verbose_name_plural = _('interests')

    class Meta:
        ordering = ['name']


ahr_rating = [
    (0, '0 star'),
    (1, '1 star'),
    (2, '2 stars'),
    (3, '3 stars'),
    (4, '4 stars'),
    (5, '5 stars'),
]


class UserProfile(models.Model):
    VISIBILITY_CHOICES = EnumChoices(
        HIDDEN=(0, _('Hidden')),
        SECURE=(1, _('Secure')),
        PUBLIC=(2, _('Public')),
    )
    NOTIFICATION_FREQUENCY = EnumChoices(
        NEVER=(0, _('Never')),
        WEEKLY=(1, _('Weekly')),
        DAILY=(2, _('Daily')),
        INSTANTLY=(3, _('Instantly')),
    )

    user = models.OneToOneField(User)
    bio = models.TextField(_('bio'), null=True, blank=True)
    tag_ling = models.CharField(_('tag line'), max_length=255, null=True, blank=True)
    web_url = models.CharField(_('website url'), max_length=255, null=True, blank=True)
    fb_url = models.CharField(_('facebook page'), max_length=255, null=True, blank=True)
    linkedin_url = models.CharField(_('linkedin page'), max_length=255, null=True, blank=True)
    tweet_url = models.CharField(_('twitter page'), max_length=255, null=True, blank=True)
    occupation = models.CharField(_('occupation'), max_length=255, null=True, blank=True)
    expertise = models.CharField(_('area of expertise'), max_length=255, null=True, blank=True)
    privacy_settings = JSONField(_('privacy settings'), null=True, blank=True)
    nationality = models.ForeignKey(Nationality, null=True, blank=True)
    resident_country = models.ForeignKey(Residence, null=True, blank=True)

    skills = models.ManyToManyField(Skills, blank=False, null=True)
    issues = models.ManyToManyField(Issues, blank=False, null=True)
    countries = models.ManyToManyField(Countries, blank=False, null=True)
    languages = models.ManyToManyField(Language, blank=True, null=True)
    regions = models.ManyToManyField(Region, blank=True, null=True)
    interests = models.ManyToManyField(Interest, blank=True, null=True)

    is_organisation = models.BooleanField(_('organisation'), default=False)
    is_individual = models.BooleanField(_('individual'), default=True)
    is_journalist = models.BooleanField(_('journalist'), default=False)
    get_newsletter = models.BooleanField(_('recieves newsletter'), default=True)
    ratecount = models.IntegerField(_('ratecount'), default=0)
    score = models.FloatField(_('score'), default=0)
    interface_lang = models.CharField(_('Interface language'), max_length=3, default='en')
    first_login = models.BooleanField(_('first login'), default=True)
    profile_visibility = models.PositiveSmallIntegerField(
        _('profile visibility'), choices=VISIBILITY_CHOICES,
        default=VISIBILITY_CHOICES.SECURE)
    notification_frequency = models.PositiveSmallIntegerField(
        _('notification frequency'), choices=NOTIFICATION_FREQUENCY,
        default=NOTIFICATION_FREQUENCY.DAILY)
    last_notification_email = models.DateTimeField(null=True)

    @property
    def ahr_rating(self):
        ratings = OrganisationalRating.objects.filter(user=self).all()
        if ratings:
            return ratings[0].rated_by_ahr
        return 0

    def get_twitter_url(self):
        base_twitter = 'https://twitter.com/'
        if self.tweet_url:
            if self.tweet_url.startswith('@'):
                return base_twitter + self.tweet_url[1:]
            else:
                return base_twitter + self.tweet_url
        return None

    def has_full_access(self):
        return not self.userprofile.first_login

    @classmethod
    def get_application_users(cls, **kwargs):
        query = kwargs.get('query', None)
        distinct = kwargs.get('distinct', None)
        order = kwargs.get('order', None)
        start = kwargs.get('start', None)
        finish = kwargs.get('finish', None)
        return cls.objects.filter(query).filter(user__is_active=True).filter(user__is_superuser=False).distinct(distinct).order_by(order)[start:finish]


class OrganisationalRating(models.Model):
    user = models.ForeignKey(auth.models.User, null=False, blank=False)
    rated_by_ahr = models.IntegerField(_('Rated by AHR'), default=0, choices=ahr_rating)


class UserRate(models.Model):
    owner = models.ForeignKey(auth.models.User, blank=True)
    user = models.ForeignKey(auth.models.User, null=True, blank=True, related_name='rates')
    pub_date = models.DateTimeField(_('publish date'), default=datetime.now)
    title = models.CharField(_('title'),max_length=200,blank=False)
    score = models.IntegerField(_('score'),default=0)

    def save(self, *args, **kwargs):
        model = self.__class__
        rates = UserRate.objects.filter(user=self.user).filter(~Q(owner=self.owner))
        if self.id == None:
            self.user.userprofile.ratecount+=1
        if len(rates) == 0:
            self.user.userprofile.score = int(self.score)
        else:
            self.user.userprofile.score = (int(self.score) + sum([rate.score for rate in rates]))/float(self.user.userprofile.ratecount)
        self.user.userprofile.save_base()
        super(UserRate,self).save(*args,**kwargs)
