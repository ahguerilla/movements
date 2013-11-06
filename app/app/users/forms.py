from django import forms
from models import Nationality, Residence, Skills, Issues, Countries


class SettingsForm(forms.Form):
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    check_password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    bio = forms.CharField(widget=forms.Textarea)
    web_url = forms.CharField()
    fb_url = forms.CharField()
    tweet_url = forms.CharField()
    occupation = forms.CharField()
    expertise = forms.CharField()
    nationality = forms.ModelChoiceField(queryset=Nationality.objects.all()) 	
    country_of_residence = forms.ModelChoiceField(queryset=Residence.objects.all())
    skills = forms.ModelMultipleChoiceField(queryset=Skills.objects.all())
    issues = forms.ModelMultipleChoiceField(queryset=Issues.objects.all())
    countries = forms.ModelMultipleChoiceField(queryset=Countries.objects.all())
    is_organisation = forms.BooleanField(required=False)
    is_individual = forms.BooleanField(required=False)
    is_journalist = forms.BooleanField(required=False)
    get_newsletter = forms.BooleanField(required=False)
