from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


class FirstLoginMiddleware(object):
    """ Redirects a user to more_about_you page if user logged in first time."""

    def process_request(self, request):
        current_url = request.get_full_path()
        target_url = reverse('more_about_you')
        if not target_url in current_url and \
            hasattr(request.user, 'userprofile') and \
            request.user.userprofile.first_login and not any([
                request.user.is_superuser,
                request.user.is_staff]):
            return HttpResponseRedirect(
                '%s?next=%s' % (target_url, current_url))


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