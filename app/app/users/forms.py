from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import (
    CheckboxFieldRenderer as BaseCheckboxFieldRenderer,
    CheckboxChoiceInput as BaseCheckboxChoiceInput,
    CheckboxSelectMultiple as BaseCheckboxSelectMultiple)
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.utils.html import format_html
from models import UserProfile, OrganisationalRating, Residence
from django.utils.translation import ugettext_lazy as _
import constance
from django.conf.global_settings import LANGUAGES

from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email


class SignUpStartForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('This email is used already'))
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError(_('Passwords must match'))
        return password2


class SignupForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField(
        max_length=30, label='First Name', required=False)
    last_name = forms.CharField(
        max_length=30, label='Last Name', required=False)
    resident_country = forms.ModelChoiceField(
        queryset=(), label='Country of Residence', required=False)
    bio = forms.CharField(
        widget=forms.Textarea(), label='Biography', required=False)
    linkedin_url = forms.CharField(
        max_length=100, label='Linked In', required=False)
    tweet_url = forms.CharField(max_length=100, label='Twitter', required=False)
    fb_url = forms.CharField(max_length=100, label='Facebook', required=False)
    web_url = forms.CharField(max_length=100, label='Website', required=False)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['resident_country'].queryset = Residence.objects.all()

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        return user

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('This username is already in used'))
        return username


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username",]

    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(UserForm, self).save(commit=False)
        if commit:
            m.save()
        return m


class CheckboxInput(BaseCheckboxChoiceInput):
    def render(self, name=None, value=None, attrs=None, choices=()):
        if 'id' in self.attrs:
            label_for = format_html(
                ' for="{0}_{1}"', self.attrs['id'], self.index)
        else:
            label_for = ''
        return format_html(
            '{0}<label></label><div{1} class="select-label">{2}</div>',
            self.tag(), label_for, self.choice_label)


class CheckboxRenderer(BaseCheckboxFieldRenderer):
    choice_input_class = CheckboxInput

    def render(self):
        return render_to_string('users/checkbox_select_multiple.html', {
            'widgets': [force_text(widget) for widget in self]})


class CheckboxSelectMultiple(BaseCheckboxSelectMultiple):
    """Custom CheckboxSelectMultiple for skills and interests"""
    renderer = CheckboxRenderer


class SettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        if kwargs.has_key('instance'):
            user_profile = initial=kwargs['instance']
        else:
            user_profile = None
        langs = constance.config.TRANSLATED_LANGUAGES.split(',')
        translated = []
        initial = None
        for lang in LANGUAGES:
            if lang[0] in langs:
                translated.append(lang)
            if user_profile and not initial and lang[0] == user_profile.interface_lang:
                initial = lang
            else:
                initial = 'en'
        self.fields['interface_lang'] = forms.ChoiceField(choices=translated, initial=initial[0])

    class Meta:
        model = UserProfile
        fields = ['nationality',
                  'occupation',
                  'resident_country',
                  'expertise',
                  'web_url',
                  'fb_url',
                  'linkedin_url',
                  'tweet_url',
                  'tag_ling',
                  'bio',
                  'interests',
                  'regions',
                  'languages',
                  'is_organisation',
                  'is_journalist',
                  'get_newsletter',
                  'profile_visibility',
                  'notification_frequency']
        widgets = {
            'interests': CheckboxSelectMultiple(),
            'regions': CheckboxSelectMultiple(),
            'languages': CheckboxSelectMultiple(),
        }

    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(SettingsForm, self).save(commit=False)
        if commit:
            m.save()
        return m

    def check_https(self, data):
        if not data.startswith('https://') and data != '':
            if data.startswith('http://'):
                data = 'https://'+data[7:]
            else:
                data = 'https://'+data
        return data

    def clean_fb_url(self):
        data = self.cleaned_data['fb_url']
        data = self.check_https(data)
        if not data.startswith('https://www.facebook.com/') and data !='':
            raise forms.ValidationError(_("You must provide a link to your facebook profile"))
        return data

    def clean_linkedin_url(self):
        data = self.cleaned_data['linkedin_url']
        data = self.check_https(data)
        if not data.startswith('https://www.linkedin.com/') and data !='':
            raise forms.ValidationError(_("You must provide a link to your linkedin profile"))
        return data

    def clean_tweet_url(self):
        data = self.cleaned_data['tweet_url']
        data = self.check_https(data)
        if not data.startswith('https://www.twitter.com/') and data !='':
            raise forms.ValidationError(_("You must provide a link to your twitter page"))
        return data


class MoreAboutYouForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('languages', 'interests', 'regions')
        widgets = {
            'languages': forms.CheckboxSelectMultiple(),
            'interests': forms.CheckboxSelectMultiple(),
            'regions': forms.CheckboxSelectMultiple()
        }

    def save(self, commit=True):
        user_profile = super(MoreAboutYouForm, self).save(commit)
        user_profile.first_login = False
        user_profile.save()
        return user_profile


class VettingForm(forms.ModelForm):
    class Meta:
        model = OrganisationalRating
        fields = ['rated_by_ahr']
