from django.template import RequestContext
from django.shortcuts import render_to_response


def open_graph(request):
    return render_to_response('market/tests/open_graph.html', {}, context_instance=RequestContext(request))