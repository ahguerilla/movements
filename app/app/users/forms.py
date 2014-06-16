from django import forms
from django.contrib.auth.models import User
from models import UserProfile, OrganisationalRating
from django.utils.translation import ugettext_lazy as _
import constance
from django.conf.global_settings import LANGUAGES

COUNTRIES = ((0, '--'),
            (1, 'United Kingdom'),
            (2, 'France'),
            (3, 'Russia'),)


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name', required=False)
    last_name = forms.CharField(max_length=30, label='Last Name', required=False)
    resident_country = forms.ChoiceField(choices=COUNTRIES, label='Country of Residence', required=False)
    bio = forms.CharField(widget=forms.Textarea(), label='Biography', required=False)
    linkedin_url = forms.CharField(max_length=100, label='Linked In', required=False)
    tweet_url = forms.CharField(max_length=100, label='Twitter', required=False)
    fb_url = forms.CharField(max_length=100, label='Facebook', required=False)
    web_url = forms.CharField(max_length=100, label='Website', required=False)

    tnccheckbox = forms.BooleanField()


    def save(self, user):
        user.first_name = ''
        user.last_name = ''
        user.save()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username",]

    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(UserForm, self).save(commit=False)
        if commit:
            m.save()
        return m


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
                  'issues',
                  'countries',
                  'skills',
                  'is_organisation',
                  'is_journalist',
                  'get_newsletter']

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


class VettingForm(forms.ModelForm):
    class Meta:
        model = OrganisationalRating
        fields = ['rated_by_ahr']