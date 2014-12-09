from django.utils.translation import ugettext_lazy as _
from models import SafeVPNLink
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
import hashlib


class SafeVPNLinkPlugin(CMSPluginBase):
    model = SafeVPNLink
    name = _("Safe VPN Link")
    render_template = "cms/plugins/safe_vpn_link.html"

    def render(self, context, instance, placeholder):
        string_to_encode = context.get('request').META.get('REMOTE_ADDR') + instance.key
        encoded_token = hashlib.md5(string_to_encode).hexdigest()
        the_url = instance.base_url + '?token=' + encoded_token
        the_link = "<a href=" + the_url + ">" + instance.link_text + "</a>"
        context['the_link'] = the_link
        return context

plugin_pool.register_plugin(SafeVPNLinkPlugin)