from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response,get_object_or_404
from models import UserProfile
from django.contrib.auth.models import User
from forms import RegisterForm, LoginForm

def register(request):
	if request.method == "POST":
		form = RegisterForm(request.POST)
	else:
		form = RegisterForm()

	return render_to_response('users/register.html', {
			'form': form,
		}, context_instance=RequestContext(request))

def login(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
	else:
		form = LoginForm()

	return render_to_response('users/login.html', {
			'form': form,
		}, context_instance=RequestContext(request))