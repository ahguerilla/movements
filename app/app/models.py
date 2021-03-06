import uuid
from django.db.models.signals import post_save
from django.utils.html import strip_tags
from menu import invalidate_menu_cache

from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool
from cms.models.pluginmodel import CMSPlugin
from django.db import models

from tinymce import models as tinymodels
from market.models import MarketItem


class MenuExtension(PageExtension):
    show_on_top_menu = models.BooleanField(default=False)
    show_on_footer_menu = models.BooleanField(default=False)

extension_pool.register(MenuExtension)


def update_menu_settings(sender, **kwargs):
    invalidate_menu_cache()

post_save.connect(update_menu_settings, sender=MenuExtension, dispatch_uid='update_menu_settings')


class NewsletterSignups(models.Model):
    registered_date = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=300)

    class Meta:
        verbose_name = 'Newsletter Signup'
        verbose_name_plural = 'Newsletter Signups'
        ordering = ('-registered_date',)

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email


def partner_image_upload_handler(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return "partner/images/{0}".format(filename)


class Partner(models.Model):
    logo = models.ImageField(upload_to=partner_image_upload_handler)
    title = models.CharField(max_length=100)
    text = models.TextField()
    enabled = models.BooleanField(default=True, blank=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        ordering = ('order',)

    def __unicode__(self):
        return self.title


def banner_image_upload_handler(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return "banner/images/{0}".format(filename)


class HomePageBanner(models.Model):
    main_image = models.ImageField(upload_to=banner_image_upload_handler)
    title_text = models.CharField(max_length=200)
    sub_text = models.CharField(max_length=300)
    enabled = models.BooleanField(default=True, blank=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        ordering = ('order',)

    def __unicode__(self):
        return self.title_text


class SafeVPNLink(CMSPlugin):
    link_text = models.CharField(max_length=500)
    base_url = models.CharField(max_length=200)
    key = models.CharField(max_length=10)


class NotificationPing(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    send_email_to = models.EmailField()
    completed = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return u'Created: {0}, Completed: {1}'.format(self.created, self.completed)


def success_stories_image_upload_handler(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return "success_stories/images/{0}".format(filename)


class SuccessStories(models.Model):
    image = models.ImageField(upload_to=partner_image_upload_handler, blank=True, null=True)
    content = tinymodels.HTMLField()
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    related_post = models.ForeignKey(MarketItem, blank=True, null=True)

    class Meta(object):
        ordering = ('order',)

    def __unicode__(self):
        return strip_tags(self.content)[:50]

    def save(self, *args, **kwargs):
        if self.id is None:
            self.order = 1
            all_success_stories = SuccessStories.objects.all()
            for success_story in all_success_stories:
                success_story.order += 1
                success_story.save()
        super(SuccessStories, self).save(*args, **kwargs)


class SuccessStoriesCMSPlugin(CMSPlugin):
    title = models.CharField(max_length=20)


class RawText(CMSPlugin):
    content = models.TextField()
