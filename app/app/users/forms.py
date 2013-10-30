from django import forms
from models import UserProfile, Nationality, Residence, Skills, Issues, Countries

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
	is_oranisation = forms.BooleanField()
	is_journalist = forms.BooleanField()
	get_newsletter = forms.BooleanField()

class LoginForm(forms.Form):
	username = forms.CharField(max_length=100)
	password = forms.CharField(max_length=100, widget=forms.PasswordInput())
