from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response,get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.db.models import Q,Max,F



def index(request):
	return render_to_response('market/offer.html',
	                          {},
	                          context_instance=RequestContext(request))