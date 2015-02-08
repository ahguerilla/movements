from __future__ import absolute_import

from django.contrib import admin
from django.http import HttpResponseForbidden
from ratelimit.decorators import ratelimit

old_login = admin.site.login


@ratelimit(key='ip', rate='5/m', method=['POST'])
def login_ratelimited(request, **kwargs):
    if request.limited:
        return HttpResponseForbidden('<h1>Rate limit exceeded</h1>')
    return old_login(request, **kwargs)

admin.site.login = login_ratelimited
