from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render
from django.contrib.auth.models import User
from django.db import transaction
from django.utils.translation import ugettext_lazy as _, ugettext

from ratelimit.decorators import ratelimit
from models import (
    UserProfile, OrganisationalRating, Language, Interest, Region, DeleteAccountRequest)
from forms import (
    SettingsForm, UserForm, VettingForm, SignUpStartForm, SignupForm,
    MoreAboutYouForm, UserGroupForm)
from form_overrides import ResetPasswordFormSilent
from allauth.account.forms import LoginForm
from allauth.account.views import SignupView, PasswordResetView, PasswordChangeView, LoginView
from allauth.socialaccount.views import SignupView as SocialSignupView
from allauth.account.views import ConfirmEmailView as BaseConfirmEmailView
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from allauth.socialaccount.adapter import get_adapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import passthrough_next_redirect_url
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sites.models import Site
from allauth.account.models import EmailConfirmation, EmailAddress
from constance import config
from django.core.urlresolvers import reverse, reverse_lazy
from app.market.api.utils import value
import app.users as users
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
import json
from django.core.mail import EmailMessage
import constance
from django.template.loader import render_to_string
from django.utils import translation
from two_factor.utils import default_device
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from django.conf import settings as site_settings


def render_settings(request):
    user = User.objects.get(pk=request.user.id)
    delete_account_request = False
    try:
        delete_request = DeleteAccountRequest.objects.filter(user=user).first()
        if delete_request:
            delete_account_request = True
    except ObjectDoesNotExist:
        delete_account_request = False
    try:
        settings = UserProfile.objects.get(user=user)
        user_groups = user.groups.all()
        group_list = []
        for g in user_groups:
            group_list.append({
                'id': g.id,
                'name': g.name,
                'receive_updates': settings.get_group_notification_preference(g.id)
            })
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
            # update the interface language
            if settings.interface_lang:
                translation.activate(settings.interface_lang)
                request.LANGUAGE_CODE = translation.get_language()

            # get group update settings
            for g in group_list:
                gets_notif = True if request.POST.get('group_notif_' + str(g.get('id'))) else False
                settings.set_group_notification_preference(g.get('id'), gets_notif)
                g['receive_updates'] = gets_notif

            # check for delete account requests
            if request.POST.get('delete_account_option') == 'delete':
                DeleteAccountRequest.objects.create(user=user)
                delete_account_request = True
                settings.set_active(False)
                ctx = {
                    "user": user,
                }
                html = render_to_string('emails/delete_account_request.html', ctx)
                email = EmailMessage('Delete user account request',
                                     html,
                                     constance.config.NO_REPLY_EMAIL,
                                     [config.ACTIVATE_USER_EMAIL])
                email.content_subtype = "html"
                email.send()
            else:
                if delete_account_request:
                    DeleteAccountRequest.objects.filter(user=user).delete()
                    delete_account_request = False
                    settings.set_active(True)
            messages.add_message(request, messages.SUCCESS, 'Profile Update Successful.')
    else:
        user_form = UserForm(instance=request.user)
        settings_form = SettingsForm(instance=settings)

    errors = dict(user_form.errors)
    errors.update(settings_form.errors)

    interest_types = {'languages': [(lang.id, lang.name) for lang in Language.objects.all()],
                      'interests': [(interest.id, interest.name) for interest in Interest.objects.all()],
                      'regions': [(region.id, region.name) for region in Region.objects.all()]}

    return render_to_response('users/user_settings_v2.html',
                              {
                                'settings_form': settings_form,
                                'user_form': user_form,
                                'group_list': group_list,
                                'interest_types': interest_types,
                                'has_password': user.has_usable_password(),
                                'errors': errors,
                                'delete_account_request': delete_account_request,
                              },
                              context_instance=RequestContext(request))


@login_required
def settings(request):
    return render_settings(request)


@login_required
def profile_for_user(request, user_name):
    return profile(request, user_name)


@login_required
def profile(request, user_name=None):
    is_public = False if request.GET.get("public", False) is False else True
    if not user_name:
        user = User.objects.get(pk=request.user.id)
    else:
        user = get_object_or_404(User, username=user_name)

    is_self = False
    if user.id == request.user.id:
        is_self = True

    # if the user isn't active, return a 404 unless it's yourself
    if is_self:
        if is_public and not user.is_active:
            raise Http404
    else:
        if not user.is_active:
            raise Http404

    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None

    orate = users.models.OrganisationalRating.objects.filter(user=user).all()
    if len(orate) > 0:
        orate = orate[0].rated_by_ahr
    else:
        orate = 0
    # 2 == public, 1 == secure, 0 == private
    visibility_settings = 2 if is_self and not is_public else user_profile.profile_visibility
    return render_to_response('users/user_profile_v2.html',
                              {
                                  'user_details': user,
                                  'user_profile': user_profile,
                                  'is_self': is_self,
                                  'is_public': is_public,
                                  'visibility_settings': visibility_settings,
                                  'ahr_rating': orate,
                                  'is_cm': request.user.userprofile.is_cm,
                              },
                              context_instance=RequestContext(request))


def waitforactivation(request):
    return render_to_response('users/waitforactivation.html',
                              {},
                              context_instance=RequestContext(request))


def thanksforactivation(request):
    return render_to_response('users/thanksforactivation.html',
                              {},
                              context_instance=RequestContext(request))


class SilentPasswordResetView(PasswordResetView):
    form_class = ResetPasswordFormSilent
    def form_valid(self, form):
        if form.cleaned_data['email'] == 'silentreject@exchangivist.org':
            return super(PasswordResetView, self).form_valid(form)
        return super(SilentPasswordResetView, self).form_valid(form)

password_reset = SilentPasswordResetView.as_view()


class PasswordChangeViewConf(PasswordChangeView):
    success_url = reverse_lazy("account_change_password_success")

password_change = login_required(PasswordChangeViewConf.as_view())

def password_change_done(request):
    return render_to_response('account/password_change.html',
                              {'message':True},
                              context_instance=RequestContext(request))


def email_doublesignup_upret(self, ret):
    if (ret.has_key('form') and
        ret['form'].errors.has_key('email') and
        ret['form'].errors['email'][0] == u'A user is already registered with this e-mail address.'):
        confem = EmailAddress.objects.filter(email=ret['form'].data['email']).all()

        if len(ret['form'].errors)==1:
            self.template_name = "account/verification_sent.html"
        else:
            ret['form'].errors['email'].remove(u'A user is already registered with this e-mail address.')
            if len(ret['form'].errors['email']) == 0:
                ret['form'].errors.pop('email')

        if not confem[0].user.is_active:
            text = render_to_string('emails/notready.html', {})
            subject = render_to_string('emails/notready_subject.html', {})
            email = EmailMessage(subject,
                                 text,
                                 constance.config.NO_REPLY_EMAIL,
                                 [ret['form'].data['email']])
            email.content_subtype = "html"
            email.send()
        else:
            text = render_to_string('emails/securityalert.html', {})
            email = EmailMessage('Security Alert from Movements',
                                 text,
                                 constance.config.NO_REPLY_EMAIL,
                                 [ret['form'].data['email']])
            email.content_subtype = "html"
            email.send()
    return ret


class AhrSocialSignupForm(SocialSignupForm):

    def save(self, request):
        adapter = get_adapter()
        user = adapter.save_user(request, self.sociallogin, form=self)
        return user


class AhrSocialSignupView(SocialSignupView):
    form_class = AhrSocialSignupForm

    def get_context_data(self, **kwargs):
        ret = super(AhrSocialSignupView, self).get_context_data(**kwargs)
        context_data = {
            'sign_up': True,
            'post_url': ''
        }
        ret.update(context_data)
        ret = email_doublesignup_upret(self, ret)

        return ret
    template_name = SignupView.template_name

ahr_social_signup = AhrSocialSignupView.as_view()


class AhrSignupView(SignupView):
    form_class = SignupForm

    def dispatch(self, request, *args, **kwargs):
        if 'email' not in request.session:
            return HttpResponseRedirect(reverse('signup_start'))
        return super(AhrSignupView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ret = super(SignupView, self).get_context_data(**kwargs)
        context_data = {
            'sign_up': True,
            'post_url': ''
        }
        ret.update(context_data)
        ret = email_doublesignup_upret(self, ret)

        login_url = passthrough_next_redirect_url(self.request,
                                                  reverse("account_login"),
                                                  self.redirect_field_name)
        redirect_field_name = self.redirect_field_name
        redirect_field_value = self.request.REQUEST.get(redirect_field_name)
        ret.update({"login_url": login_url,
                    "redirect_field_name": redirect_field_name,
                    "redirect_field_value": redirect_field_value})
        return ret

process_signup = AhrSignupView.as_view()


def signup_from_home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('show_market'))
    elif not request.session.get('email') or not \
            request.session.get('password'):
        return HttpResponseRedirect(reverse('signup_start'))

    return render_to_response(
        AhrSignupView.template_name, {
            'form': AhrSignupView.form_class(request.POST or None),
            'post_url': reverse(process_signup),
            'sign_up': True,
        }, context_instance=RequestContext(request))


def signup_start(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('show_market'))

    form = SignUpStartForm(request.POST or None)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        request.session['email'] = cleaned_data['email']
        request.session['password'] = cleaned_data['password1']
        return HttpResponseRedirect(reverse('sign_up'))
    return render_to_response(
        "account/signup_start.html", {'form': form},
        context_instance=RequestContext(request))


@login_required
def more_about_you(request):
    form = MoreAboutYouForm(request.POST or None,
                            instance=request.user.userprofile)
    if form.is_valid():
        post_type = form.cleaned_data.get('post_type', 0)
        redirect_url = reverse('create_offer') if post_type == u'1' else reverse('create_request') \
            if post_type == u'2' else request.GET.get('next', reverse('show_market'))
        keep_first_logged_in = True if post_type in [u'1', u'2'] else False
        form.save(keep_first_login=keep_first_logged_in)
        return HttpResponseRedirect(redirect_url)
    return render_to_response(
        "users/more_about_you.html",
        {
            'settings_form': form,
        },
        context_instance=RequestContext(request))


class AccAdapter(DefaultAccountAdapter):
    def new_user(self, *args, **kwargs):
        user = super(AccAdapter, self).new_user(*args, **kwargs)
        user.is_active = True
        return user

    def send_vetting_email(self, user, form):
        if not config.ACTIVATE_USER_EMAIL:
            raise Exception("Configuration Error: Check that ACTIVATE_USER_EMAIL is set")
        vet_url = reverse('vet_user', args=(user.id,))
        vet_url = site_settings.BASE_ADMIN_URL + vet_url
        ctx = {
            "user": user,
            "form": form,
            "vet_url": vet_url,
        }
        self.send_mail('account/email/user_vetting_email', config.ACTIVATE_USER_EMAIL, ctx)

    def save_user(self, request, user, form, commit=False):
        cleaned_data = form.cleaned_data
        user = super(AccAdapter, self).save_user(request, user, form, commit)
        if 'email' in request.session:
            user.email = request.session.pop('email')

        if 'password' in request.session:
            user.set_password(request.session.pop('password'))

        # set the language code from the cookie default to english
        lang_code = request.LANGUAGE_CODE if request.LANGUAGE_CODE else 'en'

        with transaction.atomic():
            user.save()
            UserProfile.objects.create(
                user=user,
                resident_country=cleaned_data['resident_country'],
                bio=cleaned_data['bio'],
                linkedin_url=cleaned_data['linkedin_url'],
                tweet_url=cleaned_data['tweet_url'],
                fb_url=cleaned_data['fb_url'],
                web_url=cleaned_data['web_url'],
                interface_lang=lang_code,
            )

        self.send_vetting_email(user, form)
        return user

    def get_email_confirmation_redirect_url(self, request):
        super(AccAdapter, self).get_email_confirmation_redirect_url(request)
        key = request.path.split('/')[3]
        conf = EmailConfirmation.objects.filter(key=key)[0]
        user = conf.email_address.user
        if user.is_active:
            return 'http://'+Site.objects.get_current().domain+'/user/thanksforactivation';

        vet_url = reverse('vet_user', args=(user.id,))
        vet_url = 'http://' + Site.objects.get_current().domain + vet_url
        ctx = {
            "user": str(conf.email_address),
            "activate_url": vet_url,
            "vetted": user.is_active,
            "current_site": Site.objects.get_current().domain,
        }

        if not config.ACTIVATE_USER_EMAIL:
            raise Exception("Configuration Error: Check that ACTIVATE_USER_EMAIL is set")

        self.send_mail('account/email/user_confirmed_email', config.ACTIVATE_USER_EMAIL, ctx)
        return 'http://'+Site.objects.get_current().domain+'/user/waitforactivation'


@staff_member_required
def vet_user(request, user_id):
    user = User.objects.get(pk=user_id)
    try:
        rating = OrganisationalRating.objects.get(user=user)
    except OrganisationalRating.DoesNotExist:
        rating = None
    msg = ''
    if request.method == 'POST':
        form = VettingForm(request.POST, instance=rating)
        group_form = UserGroupForm(request.POST, instance=user)
        msg = None
        if form.is_valid() and group_form.is_valid():
            if not rating:
                rating = form.save(commit=False)
                rating.user_id = user.id
                rating.save()
            else:
                form.save()
            group_form.save()
            user.save()
            typeuser = ContentType.objects.filter(name='user').all()[0]
            log = LogEntry(user_id=request.user.id,
                           content_type=typeuser,
                           object_id=user.id,
                           object_repr=user.username,
                           action_flag=2,
                           change_message="vetted")
            log.save()
            msg = 'User updated'
    else:
        form = VettingForm(instance=rating)
        group_form = UserGroupForm(instance=user)
    email_verified = EmailAddress.objects.filter(user=user, verified=True).exists()
    ctx = {
        'email_verified': email_verified,
        'original': user,
        'user': user,
        'form': form,
        'group_form': group_form,
        'msg': msg,
        'vetted': user.is_active
    }
    return render_to_response('admin/auth/user/vet_user.html', ctx, context_instance=RequestContext(request))


@staff_member_required
def email_vet_user(request, user_id):
    user = User.objects.get(pk=user_id)
    if not user.is_active:
        return HttpResponse(json.dumps({'success': False, 'message': 'User is not vetted.'}), mimetype="application/json")
    text = render_to_string('emails/getstarted.html',
                            {
                                'user': user,
                                'login_url': 'http://'+Site.objects.get_current().domain+'/accounts/login'
                            }
                        )
    subject = render_to_string('emails/getstarted_subject.html',{})

    email = EmailMessage(subject,
                         text,
                         constance.config.NO_REPLY_EMAIL,
                         [user.email])
    email.content_subtype = "html"
    email.send()
    return HttpResponse(json.dumps({'success': True, 'message': 'An email has been sent to the user.'}), mimetype="application/json")


class ConfirmEmailView(BaseConfirmEmailView):
    def post(self, *args, **kwargs):
        self.object = self.get_object()

        # Confirmation of T&C is no longer required to be explicit, so always succeed.

        # if 'accept_terms' in self.request.POST:
        return super(ConfirmEmailView, self).post(*args, **kwargs)

        # messages.warning(self.request, _('You have not accepted terms and conditions'))
        # return HttpResponseRedirect(reverse('account_confirm_email', args=[self.get_object().key]))

confirm_email = ConfirmEmailView.as_view()


class RatelimitedLoginForm(LoginForm):
    @ratelimit(key='post:login', rate='3/m', method=['POST'])
    @ratelimit(key='ip', rate='20/m', method=['POST'])
    def login(self, request, redirect_url=None):
        # prevent admin users hijacking this login page to circumvent
        # two factor authentication
        if site_settings.ADMIN_ENABLED:
            if default_device(self.user):
                raise Http404

        if request.limited:
            return render(request, 'account/ratelimit_triggered.html', {})
        return super(RatelimitedLoginForm, self).login(request, redirect_url)


class RatelimitedLoginView(LoginView):
    form_class = RatelimitedLoginForm


ratelimited_login = RatelimitedLoginView.as_view()


def one_click_unsubscribe(request, uuid):
    if request.method == 'POST' and request.user.is_authenticated():
        error_message = None
        request.user.userprofile.notification_frequency = UserProfile.NOTIFICATION_FREQUENCY.NEVER
        request.user.userprofile.save(update_fields=['notification_frequency'])
    else:
        if uuid:
            uuid_profile = UserProfile.objects.filter(unsubscribe_uuid=uuid).first()
            error_message = None
        else:
            uuid_profile = None
            if not request.user.is_authenticated():
                error_message = ugettext('This unsubscribe link does not map to a valid user.')
            else:
                error_message = ugettext('To unsubscribe click on on the button below.')
        if not error_message and request.user.is_authenticated() and request.user != uuid_profile:
            error_message = ugettext('You are logged in as a different user to the link followed')
        if not error_message and uuid_profile:
            uuid_profile.notification_frequency = UserProfile.NOTIFICATION_FREQUENCY.NEVER
            uuid_profile.save(update_fields=['notification_frequency'])
    return render_to_response('account/unsubscribe.html',
                              {
                                  'error_message': error_message,
                              },
                              context_instance=RequestContext(request))


def one_click_group_unsubscribe(request, group_id, uuid):
    error_message = None
    try:
        user_profile = UserProfile.objects.get(unsubscribe_uuid=uuid)
        group = Group.objects.get(pk=group_id)
        user_profile.set_group_notification_preference(group.id, False)
    except ObjectDoesNotExist:
        error_message = _("Invalid unsubscribe link.")
    return render_to_response('account/unsubscribe.html',
                              {
                                  'group': group,
                                  'error_message': error_message,
                              },
                              context_instance=RequestContext(request))