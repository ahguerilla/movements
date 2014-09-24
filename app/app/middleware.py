import re
from django.contrib.sites.models import Site
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import translation


class UserProfileLocaleMiddleware(object):
    def process_request(self, request):
        if hasattr(request.user, 'userprofile'):
            translation.activate(request.user.userprofile.interface_lang)
            request.LANGUAGE_CODE = translation.get_language()
#        else:
#            translation.activate('ar') # read from language cookie?
#            request.LANGUAGE_CODE = translation.get_language()

class SSLRedirect:
    def process_request(self, request):
        if not any([settings.DEBUG, request.is_secure(), request.META.get("X-Forwarded-Proto", "") == 'https',
                    request.META.get("HTTP_X_FORWARDED_PROTO", "") == 'https']):
            url = request.build_absolute_uri(request.get_full_path())
            if url.startswith('http://'):
                secure_url = url.replace("http://", "https://")
                return HttpResponseRedirect(secure_url)


class SitesRedirect:
    def process_request(self, request):
        host = request.get_host()
        site = Site.objects.get_current()
        if host == site.domain:
            return None
        url = "%s://%s%s" % ('https' if request.is_secure() else 'http', site, request.get_full_path())
        return HttpResponseRedirect(url)