from django import forms
from models import Nationality, Residence, Skills, Issues, Countries


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    check_password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    nationality = forms.ModelChoiceField(queryset=Nationality.objects.all()) 	
    country_of_residence = forms.ModelChoiceField(queryset=Residence.objects.all())
    skills = forms.ModelMultipleChoiceField(queryset=Skills.objects.all())
    issues = forms.ModelMultipleChoiceField(queryset=Issues.objects.all())
    countries = forms.ModelMultipleChoiceField(queryset=Countries.objects.all())
    is_oranisation = forms.BooleanField(required=False)
    is_journalist = forms.BooleanField(required=False)
    get_newsletter = forms.BooleanField(required=False)

    def save(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()