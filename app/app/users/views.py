from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response,get_object_or_404
from models import UserProfile
from django.contrib.auth.models import User
from forms import RegisterForm, LoginForm

# /dashboard is just a temporary blank redirect for compilation purposes
def dashboard(request):
	return render_to_response('users/dashboard.html', {}, context_instance=RequestContext(request))

def register(request):
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			flag = True

			password = request.POST.get('password')
			check = request.POST.get('check_password')
			if password != check:
				flag = False

			if flag:
				return HttpResponseRedirect("/dashboard")
	else:
		form = RegisterForm()

	return render_to_response('users/register.html', {
			'form': form,
		}, context_instance=RequestContext(request))

def login(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():

			#username = request.POST.get('username')
			#password = request.POST.get('password')
			#
			#user = authenticate(username=username, password=password)
	        #if user is not None:
	        #    if user.is_active:
	        #        login(request, user)
	        #        state = "You're successfully logged in!"
	        #    else:
	        #        state = "Your account is not active, please contact the site admin."
	        #else:
	        #    state = "Your username and/or password were incorrect."
	
			return HttpResponseRedirect("/dashboard")
	else:
		form = LoginForm()

	return render_to_response('users/login.html', {
			'form': form,
		}, context_instance=RequestContext(request))