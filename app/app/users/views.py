from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from models import UserProfile
from forms import SettingsForm, UserForm, SignupForm
from form_overrides import ResetPasswordFormSilent
from allauth.account.views import SignupView, PasswordResetView
from allauth.socialaccount.views import SignupView as SocialSignupView
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from allauth.account.models import EmailConfirmation
from constance import config


def render_settings(request, initial=False):
    template = 'users/user_settings.html'
    user = User.objects.get(pk=request.user.id)
    try:
        settings = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        settings = None
    try:
        perms = request.user.userprofile.notperm
    except:
        perms = {}

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if settings:
            settings_form = SettingsForm(request.POST, instance=settings)
        else:
            settings_form = SettingsForm(request.POST)
        if user_form.is_valid() and settings_form.is_valid():
            perms = {k[8:]:v for k, v in request.POST.items() if k.startswith('notperm-')}
            user = user_form.save()
            settings = settings_form.save(commit=False)
            settings.user_id = request.user.id
            settings.notperm = perms
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
                                'notperm': str(perms).replace("u'","'"),
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
                                    'user_details': user,
                                    'user_profile': user_profile,
                                    'is_self': is_self,
                                },
                                context_instance=RequestContext(request))

def waitforactivation(request):
    return render_to_response('users/waitforactivation.html',
                              {},
                              context_instance=RequestContext(request))



class SilentPasswordResetView(PasswordResetView):
    form_class = ResetPasswordFormSilent
    def form_valid(self, form):
        if form.cleaned_data['email'] == 'silentreject@exchangivist.org':
            return super(PasswordResetView, self).form_valid(form)
        return super(SilentPasswordResetView, self).form_valid(form)

password_reset = SilentPasswordResetView.as_view()


class AhrSocialSignupView(SocialSignupView):
    def get_context_data(self, **kwargs):
        ret = super(AhrSocialSignupView, self).get_context_data(**kwargs)
        context_data = {
            'body_class': 'narrow',
            'sign_up': True,
            'post_url': ''
        }
        ret.update(context_data)
        return ret
    template_name = SignupView.template_name
    
ahr_social_signup = AhrSocialSignupView.as_view()

def signup_from_home(request):
    form = SignupView.form_class()
    if request.method == 'POST':
        form.fields['first_name'].initial = request.POST.get('first_name', '')
        form.fields['last_name'].initial = request.POST.get('last_name', '')
        form.fields['email'].initial = request.POST.get('email', '')
    view_dict = {
        'form': form,
        'body_class': 'narrow',
        'post_url': reverse(process_signup),
        'sign_up': True,
    }
    return render_to_response(SignupView.template_name, view_dict, context_instance=RequestContext(request))


def process_signup(request):
    form = SignupView.form_class()
    if request.method == 'POST':
        form.fields['first_name'].initial = request.POST.get('first_name', '')
        form.fields['last_name'].initial = request.POST.get('last_name', '')
        form.fields['email'].initial = request.POST.get('email', '')
    view_dict = {
        'form': form,
        'body_class': 'narrow',
        'sign_up': True,
        'post_url': ''
    }
    return render_to_response(SignupView.template_name, view_dict, context_instance=RequestContext(request))    


class AccAdapter(DefaultAccountAdapter):
    def new_user(self, *args, **kwargs):
        user = super(AccAdapter,self).new_user(*args,**kwargs)
        user.is_active = False
        return user

    def save_user(self, *args,**kwargs):
        user = super(AccAdapter,self).save_user(*args,**kwargs)
        return user

    def get_email_confirmation_redirect_url(self, request):
        super(AccAdapter,self).get_email_confirmation_redirect_url(request)
        key = request.path.split('/')[3]
        conf = EmailConfirmation.objects.filter(key=key)[0]
        if conf.email_address.user.is_active:
            return 'http://'+Site.objects.get_current().domain

        ctx = {
            "user": str(conf.email_address),
            "activate_url": 'http://'+Site.objects.get_current().domain+"/admin/auth/user/"+str(conf.email_address.user_id),
            "current_site": Site.objects.get_current().domain,
        }
        self.send_mail('account/email/user_confirmed_email', config.ACTIVATE_USER_EMAIL, ctx)
        return 'http://'+Site.objects.get_current().domain+'/user/waitforactivation'
