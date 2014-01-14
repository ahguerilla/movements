from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('exchange'))
    return render_to_response('home.html', {}, context_instance=RequestContext(request))


def exchange(request):
    return HttpResponseRedirect(reverse('show_market'))
