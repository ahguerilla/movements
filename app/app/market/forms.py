import app.market as market
import app.users as users
from django import forms
from postman.forms import WriteForm,FullReplyForm,QuickReplyForm
from postman.fields import CommaSeparatedUserField
from django.core.validators import ValidationError
from django.utils.translation import ugettext_lazy as _



class MarketQuickReplyForm(QuickReplyForm):
    class Meta(QuickReplyForm.Meta):
        widgets = {
            'body': forms.Textarea(attrs={'cols': 55, 'rows': 5, 'class':"form-control"}),
        }


class MarketFullReplyForm(FullReplyForm):
    class Meta(FullReplyForm.Meta):
        widgets = {
            'body': forms.Textarea(attrs={'cols': 55, 'rows': 5, 'class':"form-control"}),
        }



class MarketWriteForm(WriteForm):
    class Meta(WriteForm.Meta):
        widgets = {
            'body': forms.Textarea(attrs={'cols': 55, 'rows': 5, 'class':"form-control"}),
        }


class offerForm(forms.ModelForm):
    exp_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M',], required=False)
    class Meta:
        model = market.models.MarketItem
        fields = ['issues','skills','countries','title','details','exp_date','never_exp']

    def clean(self):
        err = _('You should enter an expiry date for your offer or check never expires')
        cleaned_data = super(offerForm, self).clean()
        check = [cleaned_data['exp_date'], cleaned_data['never_exp']]
        if not any(check):
            self._errors['exp_date'] = self.error_class([err])
        return cleaned_data

    def save(self, commit=False, *args, **kwargs):
        instance = super(offerForm, self).save(commit=commit, *args, **kwargs)
        instance.item_type = self.cleaned_data['item_type']
        instance.owner = self.cleaned_data['owner']
        return instance


class requestForm(forms.ModelForm):
    exp_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M',], required=False)
    class Meta:
        model = market.models.MarketItem
        fields = ['issues','countries','title','details','exp_date','never_exp']

    def clean(self):
        err = _('You should enter an expiry date for your request or check never expires')
        cleaned_data = super(requestForm, self).clean()
        check = [cleaned_data['exp_date'], cleaned_data['never_exp']]
        if not any(check):
            self._errors['exp_date'] = self.error_class([err])

        return cleaned_data

    def save(self, commit=False, *args, **kwargs):
        instance = super(requestForm, self).save(commit=commit, *args, **kwargs)
        instance.item_type = self.cleaned_data['item_type']
        instance.owner = self.cleaned_data['owner']
        return instance


class resourceForm(forms.ModelForm):
    exp_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M',])
    class Meta:
        model = market.models.MarketItem
        fields = ['issues','countries','skills','title','details','exp_date','url']

    def save(self, commit=False, *args, **kwargs):
        instance = super(resourceForm, self).save(commit=commit, *args, **kwargs)
        instance.item_type = self.cleaned_data['item_type']
        instance.owner = self.cleaned_data['owner']
        return instance


class fileForm(forms.ModelForm):
    afile = forms.FileField()
    class Meta:
        model = market.models.File
        fields = ['afile',]

    def save(self, commit=False, *args, **kwargs):
        instance = super(FileForm, self).save(commit=commit, *args, **kwargs)
        instance.filename = self.cleaned_data['filename']
        #instance.afile = self.cleaned_data['afile']
        instance.item = self.cleaned_data['item']
        return instance


class commentForm(forms.ModelForm):
    class Meta:
        model = market.models.Comment
        fields = ['contents',]

    def save(self, commit=False, *args, **kwargs):
        instance = super(commentForm, self).save(commit=commit, *args, **kwargs)
        if instance.pk == None:
            instance.owner = self.cleaned_data['owner']
            instance.item = self.cleaned_data['item']
        return instance


def saveMarketItem(form, obj_type, owner):
    form.cleaned_data['item_type'] = obj_type
    form.cleaned_data['owner'] = owner
    obj = form.save()
    obj.save()
    form.save_m2m()
    return obj


def saveFile(form,obj_type,owner,objs):
    form.cleaned_data['item'] = objs[-1].id
    form.cleaned_data['filename'] = 'test'
    #form.cleaned_data['afile'] = 'test'
    obj = form.save()
    return obj


item_forms = {
    'offer':offerForm,
    'request':requestForm,
    'resource':resourceForm
}


class reportMarketItemForm(forms.ModelForm):
    class Meta:
        model = market.models.MarketItemPostReport
        fields = ['contents',]


class reportUserForm(forms.ModelForm):
    class Meta:
        model = market.models.UserReport
        fields = ['contents',]


class QuestionnaireForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questionnaire = kwargs.pop('questionnaire')
        super(QuestionnaireForm, self).__init__(*args, **kwargs)
        for question in questionnaire.questions.all():
            self.fields['question_%s' % question.pk] = forms.CharField(
                widget=forms.Textarea()
            )
