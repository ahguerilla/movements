from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
import app.assets


def home(request):
	return render_to_response('home.html',{},context_instance=RequestContext(request))
