from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response,get_object_or_404
from models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from forms import SettingsForm

#@login_required(login_url='/accounts/login/')
def settings(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            flag = True

            password = request.POST.get('password')
            check = request.POST.get('check_password')
            if password != check:
                flag = False

            username = request.POST.get('username')
            email = request.POST.get('email')
            #user = User.objects.create_user(username, email, password)

            if flag:
                return HttpResponseRedirect("/settings")
    else:
        form = SettingsForm()

    return render_to_response('users/usersettings.html', {
            'form': form,
        }, context_instance=RequestContext(request))