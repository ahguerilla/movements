from __future__ import absolute_import

from django.http import HttpResponseForbidden
from adminplus.sites import AdminSitePlus
from django.views.decorators.cache import never_cache
from ratelimit.decorators import ratelimit


class MovementsAdminSite(AdminSitePlus):
    @never_cache
    @ratelimit(key='ip', rate='3/m', method=['POST'])
    def login(self, request, **kwargs):
        if request.limited:
            return HttpResponseForbidden('<h1>Rate limit exceeded</h1>')
        return super(MovementsAdminSite, self).login(request, **kwargs)
