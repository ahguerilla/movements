from django.contrib.auth.decorators import permission_required
from django.db.models import Q,Max,F
from django.http import HttpResponse
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext, loader


def index(request):
	from app.api.views import newofferForm
	form = newofferForm()
	return render_to_response('market/offer.html',
	                          {'offer':''},
	                          context_instance=RequestContext(request))