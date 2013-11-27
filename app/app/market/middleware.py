from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse

class NoUserProfile(object):
    def process_request(self,request):
        if not request.user.is_anonymous():            
            if not hasattr(request.user,'userprofile') and (
                request.path != reverse('user_settings') and
                request.path != reverse('account_logout')
            ):
                return HttpResponseRedirect(reverse('user_settings'))
        return None
    
    