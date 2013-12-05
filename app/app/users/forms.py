from django import forms
from django.contrib.auth.models import User
from models import Nationality, Residence, Skills, Issues, Countries, UserProfile


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def save(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
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