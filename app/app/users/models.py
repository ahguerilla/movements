from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from json_field import JSONField


class Skills(models.Model):
    skills = models.CharField(_('skill set'), max_length=255, null=True)

    def __unicode__(self):
        return self.skills


class Issues(models.Model):
    issues = models.CharField(_('issues of interest'), max_length=255, null=True)

    def __unicode__(self):
        return self.issues


class Countries(models.Model):
    countries = models.CharField(_('countries of interest'), max_length=255, null=True)

    def __unicode__(self):
        return self.countries


class Nationality(models.Model):
    nationality = models.CharField(_('nationality'), max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.nationality


class Residence(models.Model):
    residence = models.CharField(_('country of residence'), max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.residence


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    bio = models.TextField(_('bio'), null=True, blank=True)
    tag_ling = models.CharField(_('tag line'), max_length=255, null=True, blank=True)
    web_url = models.CharField(_('website url'), max_length=255, null=True, blank=True)
    fb_url = models.CharField(_('facebook page'), max_length=255, null=True, blank=True)
    tweet_url = models.CharField(_('twitter page'), max_length=255, null=True, blank=True)
    occupation = models.CharField(_('occupation'), max_length=255, null=True, blank=True)
    expertise = models.CharField(_('area of expertise'), max_length=255, null=True, blank=True)
    notifications = JSONField(_('notifications'), null=True, blank=True)
    privacy_settings = JSONField(_('privacy settings'), null=True, blank=True)
    nationality = models.ForeignKey(Nationality, null=True)
    resident_country = models.ForeignKey(Residence, null=True)
    skills = models.ManyToManyField(Skills, blank=True, null=True)
    issues = models.ManyToManyField(Issues, blank=True, null=True)
    countries = models.ManyToManyField(Countries, blank=True, null=True)
    is_organisation = models.BooleanField(_('organisation'), default=False)
    is_individual = models.BooleanField(_('individual'), default=True)
    is_journalist = models.BooleanField(_('journalist'), default=False)
    get_newsletter = models.BooleanField(_('recieves newsletter'), default=False)
    firstlogin = models.BooleanField(_('first_login'), default=True)

    def get_twitter_url(self):
        base_twitter = 'https://twitter.com/'
        if self.tweet_url:
            if self.tweet_url.startswith('@'):
                return base_twitter + self.tweet_url[1:]
            else:
                return base_twitter + self.tweet_url
        return None
