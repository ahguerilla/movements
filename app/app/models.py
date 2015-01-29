from django.db.models.signals import post_save
from menu import invalidate_menu_cache

from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool
from cms.models.pluginmodel import CMSPlugin
from django.db import models


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


class SafeVPNLink(CMSPlugin):
    link_text = models.CharField(max_length=500)
    base_url = models.CharField(max_length=200)
    key = models.CharField(max_length=10)
