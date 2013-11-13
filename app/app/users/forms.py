from django import forms
from models import Nationality, Residence, Skills, Issues, Countries


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def save(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class SettingsForm(forms.Form):
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    check_password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    occupation = forms.CharField()
    expertise = forms.CharField()
    bio = forms.CharField(widget=forms.Textarea, required=False)
    web_url = forms.CharField(required=False)
    facebook_url = forms.CharField(required=False)
    twitter_url = forms.CharField(required=False)
    nationality = forms.ModelChoiceField(queryset=Nationality.objects.all()) 	
    country_of_residence = forms.ModelChoiceField(queryset=Residence.objects.all())
    skills = forms.ModelMultipleChoiceField(queryset=Skills.objects.all(), required=False)
    issues = forms.ModelMultipleChoiceField(queryset=Issues.objects.all(), required=False)
    countries = forms.ModelMultipleChoiceField(queryset=Countries.objects.all(), required=False)
    is_organisation = forms.BooleanField(required=False)
    is_individual = forms.BooleanField(required=False)
    is_journalist = forms.BooleanField(required=False)
    get_newsletter = forms.BooleanField(required=False)
