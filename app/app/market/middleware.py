from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse

class NoUserProfile(object):
    def process_request(self,request):
        if not request.user.is_anonymous() and not hasattr(request.user,'userprofile') and (
            request.path != reverse('getting_started') and
            request.path != reverse('account_logout')
            ):
            return HttpResponseRedirect(reverse('getting_started'))
        return None