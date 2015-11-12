from django import forms
from django.contrib.auth.models import User, Group
from django.forms.widgets import (
    CheckboxFieldRenderer as BaseCheckboxFieldRenderer,
    CheckboxChoiceInput as BaseCheckboxChoiceInput,
    CheckboxSelectMultiple as BaseCheckboxSelectMultiple)
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.utils.html import format_html
from models import (
    UserProfile, OrganisationalRating, Residence, Countries, Region
    )
from django.utils.translation import ugettext_lazy as _
import constance
from django.conf.global_settings import LANGUAGES
import re

from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email


class SignUpStartForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise forms.ValidationError(_('Please enter a valid email'))
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_('This email is used already'))
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        if not password1 or not password2:
            raise forms.ValidationError(_('Please enter a password'))
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
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise forms.ValidationError(_('Please enter a username'))
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(_('This username is already in use'))
        if not re.match("^[A-Za-z0-9_-]*$", username):
            raise forms.ValidationError(_('Username must contain only letters, numbers - and _. White space is not allowed'))
        if len(username) < 3 or len(username) > 30:
            raise forms.ValidationError(_('Username must be greater that 2 characters and less than 30 contain only letters, numbers - and _. White space is not allowed'))
        return username


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]

    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(UserForm, self).save(commit=False)
        if commit:
            m.save()
        return m

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise forms.ValidationError(_('Please enter a username'))
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(_('This username is already in use'))
        if not re.match("^[A-Za-z0-9_-]*$", username):
            raise forms.ValidationError(_('Username must contain only letters, numbers - and _. White space is not allowed'))
        if len(username) < 3 or len(username) > 30:
            raise forms.ValidationError(_('Username must be greater that 2 characters and less than 30 contain only letters, numbers - and _. White space is not allowed'))
        return username


class CheckboxInput(BaseCheckboxChoiceInput):
    def render(self, name=None, value=None, attrs=None, choices=()):
        if 'id' in self.attrs:
            label_for = format_html(
                u' for="{0}_{1}"', self.attrs['id'], self.index)
        else:
            label_for = u''
        return format_html(
            u'<div class="select-checkbox {0}">{1}<label></label><div{2} class="select-label">{3}</div></div>',
            u'checked' if self.is_checked() else u'',
            self.tag(), label_for, self.choice_label)


class CheckboxRenderer(BaseCheckboxFieldRenderer):
    choice_input_class = CheckboxInput

    def render(self):
        return render_to_string('users/checkbox_select_multiple.html', {
            'widgets': [force_text(widget) for widget in self]})


class CheckboxSelectMultiple(BaseCheckboxSelectMultiple):
    """Custom CheckboxSelectMultiple for skills and interests"""
    renderer = CheckboxRenderer


class RegionAccordionRenderer(BaseCheckboxFieldRenderer):
    choice_input_class = CheckboxInput

    def render(self):
        countries = Countries.objects.all()
        regions = Region.objects.all()
        region_dict = dict()
        for widget in self:
            country = next((c for c in countries if str(c.id) == widget.choice_value), None)
            region = next((r for r in regions if r.id == country.region_id), None)
            if region:
                if region.name in region_dict.keys():
                    region_dict[region.name].append(force_text(widget))
                else:
                    region_dict[region.name] = [force_text(widget)]

        region_list = []
        for reg in region_dict:
            region_item = {
                "region": reg,
                "country_list": region_dict[reg]
            }
            region_list.append(region_item)
        region_list = sorted(region_list, key=lambda r: r['region'])

        return render_to_string('widgets/accordion_multi_select.html', {'regions': region_list})


class RegionAccordionSelectMultiple(BaseCheckboxSelectMultiple):
    renderer = RegionAccordionRenderer


class SettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['languages'].required = False
        self.fields['interests'].required = False
        self.fields['countries'].required = False

    class Meta:
        model = UserProfile
        fields = [
            'occupation', 'resident_country', 'interface_lang', 'expertise', 'web_url', 'fb_url',
            'linkedin_url', 'tweet_url', 'tag_ling', 'bio', 'interests',
            'countries', 'languages', 'is_organisation', 'is_journalist',
            'get_newsletter', 'profile_visibility', 'notification_frequency'
        ]
        widgets = {
            'interests': CheckboxSelectMultiple(),
            'languages': CheckboxSelectMultiple(),
            'countries': RegionAccordionSelectMultiple(),
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


class MoreAboutYouForm(forms.ModelForm):
    USER_TYPE_PREFERENCE = ((0, _("I will offer my skills")),
                            (1, _("I will Request help")),
                            (2, _("I'll decide later")),)
    user_preference_type = forms.ChoiceField(widget=forms.RadioSelect, choices=USER_TYPE_PREFERENCE)
    CREATE_POST = ((0, _("None")),
                   (1, _("Offer")),
                   (2, _("Request")),)
    post_type = forms.ChoiceField(choices=CREATE_POST)

    def __init__(self, *args, **kwargs):
        super(MoreAboutYouForm, self).__init__(*args, **kwargs)
        self.fields['languages'].required = False
        self.fields['interests'].required = False
        self.fields['countries'].required = False
        self.fields['user_preference_type'].required = False

    class Meta:
        model = UserProfile
        fields = ('languages', 'interests', 'countries')

        widgets = {
            'languages': CheckboxSelectMultiple(),
            'interests': CheckboxSelectMultiple(),
            'countries': RegionAccordionSelectMultiple(),
        }

    def save(self, commit=True, keep_first_login=False):
        user_profile = super(MoreAboutYouForm, self).save(commit)
        # map user_preference_type
        u_pref = self.cleaned_data.get('user_preference_type', u'2')
        if u_pref == u'0':
            user_profile.user_preference_type = UserProfile.USER_TYPE_PREFERENCE.OFFER
        elif u_pref == u'1':
            user_profile.user_preference_type = UserProfile.USER_TYPE_PREFERENCE.REQUEST
        else:
            user_profile.user_preference_type = UserProfile.USER_TYPE_PREFERENCE.UNKNOWN

        if not keep_first_login:
            user_profile.first_login = False

        user_profile.save()
        return user_profile


class VettingForm(forms.ModelForm):
    class Meta:
        model = OrganisationalRating
        fields = ['rated_by_ahr']


class UserGroupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['groups']