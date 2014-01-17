from django import forms
from django.contrib.auth.models import User
from models import UserProfile



class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    linkedin_url = forms.CharField(max_length=100, label='Linked In', required=False)
    tweet_url = forms.CharField(max_length=100, label='Twitter', required=False)
    fb_url = forms.CharField(max_length=100, label='Facebook', required=False)
    web_url = forms.CharField(max_length=100, label='Website', required=False)

    def save(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.linkedin_url = self.cleaned_data['linkedin_url']
        user.tweet_url = self.cleaned_data['tweet_url']
        user.fb_url = self.cleaned_data['fb_url']
        user.web_url = self.cleaned_data['web_url']
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