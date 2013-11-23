from django import forms
from models import Nationality, Residence, Skills, Issues, Countries, UserProfile


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def save(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class SettingsForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    repeat_password = forms.CharField(max_length=100, widget=forms.PasswordInput())    
    class Meta:
        model = UserProfile  
        exclude = ['user','privacy_settings','notifications',]

    def __init__(self, user=None, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self._user = user

def saveUser(self, user):
    user.first_name = self.cleaned_data['first_name']
    user.last_name = self.cleaned_data['last_name']
    user.email = self.cleaned_data['email']
    #user.password = self.cleaned_data['password']
    user.save()

def saveSettings(self, profile):
    profile.bio = self.cleaned_data['bio']
    profile.web_rul = self.cleaned_data['web_url']
    # ...?
    profile.save()