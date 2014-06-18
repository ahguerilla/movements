from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings as django_settings

def home(request):
    if request.user.is_authenticated() and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('exchange'))
    view_dict = {'sign_up': True}
    if django_settings.V2_TEMPLATES:
        template = 'ahr/home_v2.html'
    else:
        template = 'ahr/home.html'

    return render_to_response(template, view_dict, context_instance=RequestContext(request))


def terms_and_conditions(request):
    return render_to_response('ahr/terms_and_conditions.html', context_instance=RequestContext(request))


def contact_us(request):
    return render_to_response('ahr/contact_us.html', context_instance=RequestContext(request))


def exchange(request):
    return HttpResponseRedirect(reverse('show_market'))
