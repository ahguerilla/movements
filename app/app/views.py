from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('exchange'))
    view_dict = {'body_class': 'narrow', 'sign_up': True}
    return render_to_response('ahr/home.html', view_dict, context_instance=RequestContext(request))


def terms_and_conditions(request):
    return render_to_response('ahr/terms_and_conditions.html', context_instance=RequestContext(request))


def contact_us(request):
    return render_to_response('ahr/contact_us.html', context_instance=RequestContext(request))


def privacy(request):
    return render_to_response('ahr/privacy.html', context_instance=RequestContext(request))

def how_it_works_pub(request):
    return render_to_response('ahr/how_it_works_public.html', context_instance=RequestContext(request))

@login_required
def how_it_works_priv(request):
    return render_to_response('ahr/how_it_works_private.html', context_instance=RequestContext(request))

def exchange(request):
    return HttpResponseRedirect(reverse('show_market'))
