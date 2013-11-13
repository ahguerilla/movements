import app.market as market
import app.users as users
from django import forms


class newofferForm(forms.ModelForm):
    exp_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M',])
    class Meta:
        model = market.models.MarketItem
        fields = ['issues','skills','countries','title','details','exp_date']

    def save(self, commit=False, *args, **kwargs):
        instance = super(newofferForm, self).save(commit=commit, *args, **kwargs)
        instance.item_type = self.cleaned_data['item_type']
        instance.owner = self.cleaned_data['owner']
        return instance


class commentForm(forms.ModelForm):
    class Meta:
        model = market.models.Comment
        fields = ['title','contents']

    def save(self, commit=False, *args, **kwargs):
        instance = super(commentForm, self).save(commit=commit, *args, **kwargs)
        if instance.pk == None:
            instance.owner = self.cleaned_data['owner']
            instance.item = self.cleaned_data['item']
        return instance
