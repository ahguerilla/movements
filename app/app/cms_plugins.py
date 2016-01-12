from django.utils.translation import ugettext_lazy as _
from models import SafeVPNLink, SuccessStoriesCMSPlugin, SuccessStories, RawText
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
import hashlib


class SafeVPNLinkPlugin(CMSPluginBase):
    model = SafeVPNLink
    name = _("Safe VPN Link")
    render_template = "cms/plugins/safe_vpn_link.html"

    def render(self, context, instance, placeholder):
        ip = context.get('request').META.get("HTTP_X_FORWARDED_FOR", None)
        if ip:
            ip = ip.split(", ")[0]
        else:
            ip = context.get('request').META.get("REMOTE_ADDR", "")
        string_to_encode = ip + instance.key
        encoded_token = hashlib.md5(string_to_encode).hexdigest()
        the_url = instance.base_url + '?token=' + encoded_token
        the_link = "<a target='_blank' href=" + the_url + ">" + instance.link_text + "</a>"
        context['the_link'] = the_link
        return context


class SuccessStoriesPlugin(CMSPluginBase):
    model = SuccessStoriesCMSPlugin
    name = _("Success Stories")
    render_template = "cms/plugins/success_stories.html"

    def render(self, context, instance, placeholder):
        success_stories = SuccessStories.objects.all()
        context['success_stories'] = success_stories
        return context


class RawHtmlPlugin(CMSPluginBase):
    model = RawText
    name = _("Raw HTML")
    render_template = "cms/plugins/raw_html.html"

    def render(self, context, instance, placeholder):
        context['raw_html'] = instance.content
        return context

plugin_pool.register_plugin(SafeVPNLinkPlugin)
plugin_pool.register_plugin(SuccessStoriesPlugin)
plugin_pool.register_plugin(RawHtmlPlugin)