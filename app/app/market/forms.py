import app.market as market
import app.users as users
from django import forms


class newofferForm(forms.ModelForm):
	exp_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M',])
	class Meta:
		model = market.models.Offer
		fields = ['issues','skills','countries','title','details','exp_date']

	def save(self, commit=False, *args, **kwargs):
		instance = super(newofferForm, self).save(commit=commit, *args, **kwargs)
		instance.ip_address = self.cleaned_data['ip_address']
		instance.owner = self.cleaned_data['owner']
		return instance
