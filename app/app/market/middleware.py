from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

class NoUserProfile(object):
    def process_request(self, request):
        if not request.user.is_anonymous() and not request.user.is_superuser and not hasattr(request.user,'userprofile') and (
            request.path != reverse('getting_started') and
            request.path != reverse('account_logout') and
            request.path != reverse('avatar_change') and
            request.path != reverse('avatar_add') and
            '/'.join(request.path.split('/')[:-2]) != '/'.join(reverse('avatar_render_primary',args=(request.user.username,120)).split('/')[:-2]) and
            '/'.join(request.path.split('/')[:-1]) != '/'.join(reverse('get_avatar',args=('json',request.user.id,80)).split('/')[:-1]) and
            request.path != reverse('avatar_add') and
            not request.path.startswith(settings.MEDIA_URL+'avatars/'+request.user.username) and
            request.path != reverse('account_change_password') and
            request.path != reverse('account_change_password_success')
            ):
            return HttpResponseRedirect(reverse('getting_started'))
        return None