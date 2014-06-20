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
