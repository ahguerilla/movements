from django import forms
from django.contrib.auth.models import User
from models import UserProfile, OrganisationalRating



class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
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

    def check_https(data):
        if not data.startswith('https://'):
            if data.startswith('http://'):
                data = 'https://'+data[7:]
            else:
                data = 'https://'+data
        return data

    def clean_fb_url(self):
        data = self.cleaned_data['fb_url']
        self.check_https(data)
        if not data.startswith('https://www.facebook.com/'):
            raise forms.ValidationError("You must provide a link to your facebook profile")
        return data

    def clean_linkedin_url(self):
        data = self.cleaned_data['linkedin_url']
        self.check_https(data)
        if not data.startswith('https://www.linkedin.com/'):
            raise forms.ValidationError("You must provide a link to your linked in profile")
        return data

    def clean_linkedin_url(self):
        data = self.cleaned_data['tweet_url']
        self.check_https(data)
        if not data.startswith('https://www.twitter.com/'):
            raise forms.ValidationError("You must provide a link to your twitter in page")
        return data


class VettingForm(forms.ModelForm):
    class Meta:
        model = OrganisationalRating
        fields = ['rated_by_ahr']
