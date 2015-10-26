from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from two_factor.utils import default_device
from django.conf import settings


class FirstLoginMiddleware(object):
    """ Redirects a user to more_about_you page if user logged in first time."""

    def process_request(self, request):
        current_url = request.get_full_path()
        target_url = reverse('more_about_you')
        allowed_urls = [reverse('create_offer'), reverse('create_request')]
        if not target_url in current_url and \
            hasattr(request.user, 'userprofile') and \
            current_url not in allowed_urls and \
            request.user.userprofile.first_login and not any([
                request.user.is_superuser,
                request.user.is_staff]):
            return HttpResponseRedirect(
                '%s?next=%s' % (target_url, current_url))


class ForceTwoFactorForStaffMiddleware(object):
    """ Force admin to have 2 factor enabled """
    def process_request(self, request):
        if settings.ADMIN_ENABLED:
            allowed_urls = [reverse('admin:logout')]
            requested_url = request.get_full_path()
            two_factor_base = reverse('two_factor:profile')
            if two_factor_base not in requested_url \
               and requested_url not in allowed_urls \
               and request.user and any([request.user.is_superuser, request.user.is_staff]) \
               and not default_device(request.user):
                    return HttpResponseRedirect(reverse('two_factor:setup'))


class CsrfLoginMiddleware(object):
    """ Set login csrftoken to httponly. """
    def process_response(self, request, response):
        current_url = request.get_full_path()
        target_url = reverse('account_login')
        if current_url == target_url:
            token = response.cookies.get('csrftoken', None)
            if token:
                token['httponly'] = True
        return response