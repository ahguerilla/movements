from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from models import UserProfile
from forms import SettingsForm, UserForm
from allauth.account.views import SignupView
from django.contrib.auth.decorators import login_required


@login_required
def settings(request):
    messages = None
    user = User.objects.get(pk=request.user.id)
    try:
        settings = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        settings = None
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if settings:
            settings_form = SettingsForm(request.POST, instance=settings)
        else:
            settings_form = SettingsForm(request.POST)
        if user_form.is_valid() and settings_form.is_valid():
            user = user_form.save()
            settings = settings_form.save(commit=False)
            settings.user_id = request.user.id
            settings.save()
            settings_form.save_m2m()
            messages = ["Profile Update Successfull"]

    else:
        user_form = UserForm(instance=request.user)
        settings_form = SettingsForm(instance=settings)

    return render_to_response('users/user_settings.html', 
                              {
                                'settings_form': settings_form,
                                'user_form': user_form,
                                'messages': messages
                              }, 
                              context_instance=RequestContext(request))



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