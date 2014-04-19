from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import translation

class UserProfileLocaleMiddleware(object):
    def process_request(self, request):
        if hasattr(request.user, 'userprofile'):
            translation.activate(request.user.userprofile.interface_lang)
            request.LANGUAGE_CODE = translation.get_language()

class SSLRedirect:
    def process_request(self, request):
        if not any([settings.DEBUG, request.is_secure(), request.META.get("X-Forwarded-Proto", "") == 'https', request.META.get("HTTP_X_FORWARDED_PROTO", "") == 'https']):
            url = request.build_absolute_uri(request.get_full_path())
            if url.startswith('http://'):
                secure_url = url.replace("http://", "https://")
                return HttpResponseRedirect(secure_url)
