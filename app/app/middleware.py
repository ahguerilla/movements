from django.conf import settings
from django.http import HttpResponseRedirect


class SSLRedirect:
    def process_request(self, request):
        if not any([settings.DEBUG, request.is_secure(), request.META.get("X-Forwarded-Proto", "") == 'https']):
            url = request.build_absolute_uri(request.get_full_path())
            secure_url = url.replace("http://", "https://")
            return HttpResponseRedirect(secure_url)
