import uuid
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields.json import JSONField
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
        verbose_name_plural = 'Skills'
        ordering = ['skills']


class Issues(models.Model):
    issues = models.CharField(_('issues of interest'), max_length=255, null=True)

    def __unicode__(self):
        return self.issues

    class Meta:
        verbose_name_plural = 'Issues'
        ordering = ['issues']


class Countries(models.Model):
    countries = models.CharField(_('countries of interest'), max_length=255, null=True)
    region = models.ForeignKey('Region', null=True)

    def __unicode__(self):
        return self.countries

    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ['countries']


class Nationality(models.Model):
    nationality = models.CharField(_('nationality'), max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.nationality

    class Meta:
        verbose_name_plural = 'Nationalities'
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

    @property
    def language_code(self):
        return self.launguage_code

    class Meta:
        verbose_name = _('language')
        verbose_name_plural = _('languages')
        ordering = ['name']


class Region(NamedObject):
    class Meta:
        verbose_name = _('region')
        verbose_name_plural = _('regions')


class Interest(NamedObject):
    class Meta:
        verbose_name = _('interest')
        verbose_name_plural = _('interests')
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
        HIDDEN=(0, _('Hidden - only your screen name and avatar is shared')),
        SECURE=(1, _('Secure - only your screen name, skills and country is shared')),
        PUBLIC=(2, _('Public - all your profile information is shared')),
    )

    NOTIFICATION_FREQUENCY = EnumChoices(
        NEVER=(0, _('Never')),
        WEEKLY=(1, _('Weekly')),
        DAILY=(2, _('Daily')),
        INSTANTLY=(3, _('Instantly')),
    )

    REFERRAL_CHOICES = EnumChoices(
        UNKNOWN=(0, _('Unknown')),
        SOCIAL_MEDIA=(1, _('Social Media')),
        STAFF_CONTACT=(2, _('Staff Contact')),
        GENERAL_MEDIA=(3, _('General Media')),
        REFERRED_BY_MOVEMENTS_USER=(4, _('Referred by Movements User')),
        EVENT=(5, _('Event')),
        OTHER=(6, _('Other')),
        PREFER_NOT_TO_SAY=(7, _('Prefer not to say')),
    )

    INTERFACE_LANGUAGE = (
        ('en', 'English'),
        ('ar', 'Arabic'),
        ('zh-cn', 'Chinese'),
        ('uk', 'Ukrainian'),
        ('ru', 'Russian'),
        ('fa', 'Persian'),
        ('fr', 'French'),
    )

    USER_TYPE_PREFERENCE = EnumChoices(
        UNKNOWN=(0, _('Unknown')),
        REQUEST=(1, _('Request User')),
        OFFER=(2, _('Offer User')),
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
    nationality = models.ForeignKey(Nationality, null=True, blank=True)
    resident_country = models.ForeignKey(Residence, null=True, blank=True)
    referred_by = models.PositiveSmallIntegerField(choices=REFERRAL_CHOICES,
                                                   default=REFERRAL_CHOICES.UNKNOWN)

    skills = models.ManyToManyField(Skills, blank=True, null=True)
    issues = models.ManyToManyField(Issues, blank=True, null=True)
    countries = models.ManyToManyField(Countries, blank=True, null=True)
    languages = models.ManyToManyField(Language, blank=True, null=True)
    translation_languages = models.ManyToManyField(Language,
                                                   verbose_name=_('Trusted translation language'),
                                                   help_text='Marks a user as being trusted to provide translations in a given language. At least two languages should be marked if any.',
                                                   blank=True,
                                                   null=True,
                                                   related_name='translators')
    regions = models.ManyToManyField(Region, blank=True, null=True)
    interests = models.ManyToManyField(Interest, blank=True, null=True)

    is_cm = models.BooleanField(_('community manager'), default=False)
    is_organisation = models.BooleanField(_('organisation'), default=False)
    is_individual = models.BooleanField(_('individual'), default=True)
    is_journalist = models.BooleanField(_('journalist'), default=False)
    get_newsletter = models.BooleanField(_('recieves newsletter'), default=True)
    ratecount = models.IntegerField(_('ratecount'), default=0)
    score = models.FloatField(_('score'), default=0)
    interface_lang = models.CharField(_('Interface language'), max_length=6,
                                      default='en', choices=INTERFACE_LANGUAGE,)
    first_login = models.BooleanField(_('first login'), default=True)
    profile_visibility = models.PositiveSmallIntegerField(
        _('profile visibility'), choices=VISIBILITY_CHOICES,
        default=VISIBILITY_CHOICES.SECURE)
    notification_frequency = models.PositiveSmallIntegerField(
        _('notification frequency'), choices=NOTIFICATION_FREQUENCY,
        default=NOTIFICATION_FREQUENCY.DAILY)
    last_notification_email = models.DateTimeField(null=True, blank=True)
    unsubscribe_uuid = models.CharField(max_length=50, null=True, blank=True)
    user_preference_type = models.PositiveSmallIntegerField(choices=USER_TYPE_PREFERENCE,
                                                            default=USER_TYPE_PREFERENCE.UNKNOWN)
    group_notification_preference = JSONField(blank=True)

    def get_unsubscribe_uuid(self):
        if not self.unsubscribe_uuid:
            self.unsubscribe_uuid = str(uuid.uuid4())
            self.save(update_fields=['unsubscribe_uuid'])
        return self.unsubscribe_uuid

    @property
    def ahr_rating(self):
        ratings = OrganisationalRating.objects.filter(user=self.user).all()
        if ratings:
            return ratings[0].rated_by_ahr
        return 0

    @property
    def is_first_login(self):
        if self.user.is_superuser or self.user.is_staff:
            return False
        return self.first_login

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

    def receives_group_mail(self, group_id):
        if self.notification_frequency == self.NOTIFICATION_FREQUENCY.NEVER:
            return False
        return self.get_group_notification_preference(group_id)

    def is_provider(self):
        return self.user.marketitem_set.filter(item_type='offer').count() > 0

    def is_requester(self):
        return self.user.marketitem_set.filter(item_type='request').count() > 0

    def add_to_providers(self):
        try:
            pg = Group.objects.get(name='Provider')
            self.user.groups.add(pg)
            self.user.save()
        except ObjectDoesNotExist:
            pass

    def add_to_requesters(self):
        try:
            pg = Group.objects.get(name='Requester')
            self.user.groups.add(pg)
            self.user.save()
        except ObjectDoesNotExist:
            pass

    def set_group_notification_preference(self, key, value):
        self.group_notification_preference[str(key)] = value
        self.save()

    def get_group_notification_preference(self, key):
        return self.group_notification_preference.get(str(key), True)

    def assign_group_based_on_skills(self, is_provider, is_requester):
        skill_group_match = (
            (u'NGO Employee', 'NGO'),
            (u'Policy Expert', 'Policy Experts'),
            (u'Student', 'Students'),
            (u'Artist', 'Arts-Media'),
            (u'Public Relations', 'Public Relations'),
            (u'Social Media', 'Social Media'),
            (u'Writer/Editor', 'Editors'),
            (u'Technology', 'Technical Experts'),
            (u'Translator', 'Translators'),
            (u'Lawyer', 'Lawyers'),
            (u'Journalist', 'Journalists'),
        )
        user_interests = [i[0] for i in self.interests.values_list('name')]
        for s in skill_group_match:
            if s[0] in user_interests:
                try:
                    g = Group.objects.get(name=s[1])
                    self.user.groups.add(g)
                    self.user.save()
                except:
                    pass
        if is_provider:
            try:
                pg = Group.objects.get(name='Provider')
                self.user.groups.add(pg)
                self.user.save()
            except:
                pass
        if is_requester:
            try:
                rg = Group.objects.get(name='Requester')
                self.user.groups.add(rg)
                self.user.save()
            except:
                pass

    @classmethod
    def get_application_users(cls, **kwargs):
        query = kwargs.get('query', None)
        distinct = kwargs.get('distinct', None)
        order = kwargs.get('order', None)
        start = kwargs.get('start', None)
        finish = kwargs.get('finish', None)
        return cls.objects.filter(query).filter(user__is_active=True).filter(user__is_superuser=False).distinct(distinct).order_by(order)[start:finish]

    @property
    def is_translator(self):
        if hasattr(self, '_is_translator'):
            return self._is_translator
        self._is_translator = self.is_cm or self.translation_languages.exists()
        return self._is_translator


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
        rates = UserRate.objects.filter(user=self.user).exclude(owner=self.owner)
        if self.id is None:
            self.user.userprofile.ratecount += 1
        if len(rates) == 0:
            self.user.userprofile.score = int(self.score)
        else:
            self.user.userprofile.score = (int(self.score) + sum([rate.score for rate in rates]))/float(self.user.userprofile.ratecount)
        self.user.userprofile.save_base()
        super(UserRate, self).save(*args, **kwargs)
