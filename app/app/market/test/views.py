from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings


def open_graph(request):
    ctx = {
        'base_url': settings.BASE_URL
    }
    return render_to_response('market/tests/open_graph.html', ctx, context_instance=RequestContext(request))


def open_graph_author(request):
    return render_to_response('market/tests/open_graph_author.html', {}, context_instance=RequestContext(request))