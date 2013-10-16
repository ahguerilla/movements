from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response,get_object_or_404
from models import UserProfile
from django.contrib.auth.models import User

def register(request):
	return render_to_response('users/register.html', {}, context_instance=RequestContext(request))