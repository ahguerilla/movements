from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from models import UserProfile
from forms import SettingsForm, UserForm
from allauth.account.views import SignupView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse


def render_settings(request, initial=False):
    template = 'users/user_settings.html'
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
            messages.add_message(request, messages.SUCCESS, 'Profile Update Successfull.')
            if initial:
                template = 'users/welcome.html'
    else:
        user_form = UserForm(instance=request.user)
        settings_form = SettingsForm(instance=settings)

    return render_to_response(template, 
                              {
                                'settings_form': settings_form,
                                'user_form': user_form,
                                'initial': initial,
                              }, 
                              context_instance=RequestContext(request))


@login_required
def initial_settings(request):
    if hasattr(request.user,'userprofile'):
        return HttpResponseRedirect(reverse('user_settings'))
    return render_settings(request, True)


@login_required
def settings(request):
    return render_settings(request)


@login_required
def profile_for_user(request, user_name):
    return profile(request, user_name)


@login_required
def profile(request, user_name=None):
    print "user_name " + str(user_name)
    if not user_name:
        user = User.objects.get(pk=request.user.id)
    else:
        user = get_object_or_404(User, username=user_name)

    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None

    is_self = False
    if user.id == request.user.id:
        is_self = True

    return render_to_response('users/user_profile.html', 
                                {
                                    'user': user,
                                    'user_profile': user_profile,
                                    'is_self': is_self,

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