from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from forms import SettingsForm
from allauth.account.views import SignupView

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



class AccountSignupView(SignupView):
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.fields['first_name'].initial = self.request.GET.get('first_name', '')
        form.fields['last_name'].initial = self.request.GET.get('last_name', '')
        kwargs['form'] = form
        context = self.get_context_data(**kwargs)
        context['form'].fields['email'].initial = self.request.GET.get('email', '')
        return self.render_to_response(context)      

accountsignup = AccountSignupView.as_view()