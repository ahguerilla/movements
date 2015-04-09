from django import forms
from postman.forms import WriteForm, FullReplyForm, QuickReplyForm
from app.celerytasks import on_market_item_creation, update_notifications, on_market_item_update
from django.utils.translation import ugettext_lazy as _

import app.market as market
from app.market.models.translation import detect_language
from app.users.forms import CheckboxSelectMultiple, RegionAccordionSelectMultiple


class MarketQuickReplyForm(QuickReplyForm):
    class Meta(QuickReplyForm.Meta):
        widgets = {
            'body': forms.Textarea(attrs={'cols': 55, 'rows': 5, 'class': "form-control"}),
        }


class MarketFullReplyForm(FullReplyForm):
    class Meta(FullReplyForm.Meta):
        widgets = {
            'body': forms.Textarea(attrs={'cols': 55, 'rows': 5, 'class': "form-control"}),
        }


class MarketWriteForm(WriteForm):
    class Meta(WriteForm.Meta):
        widgets = {
            'body': forms.Textarea(attrs={'cols': 55, 'rows': 5, 'class': "form-control"}),
        }


class MarketItemBaseForm(forms.ModelForm):
    class Meta:
        model = market.models.MarketItem
        fields = ['title', 'details', 'specific_skill', 'specific_issue',
                  'receive_notifications', 'interests', 'issues',
                  'countries', 'tweet_permission']
        widgets = {
            'details': forms.Textarea(attrs={'cols': 55, 'rows': 5, 'class': "form-control"}),
            'interests': CheckboxSelectMultiple(),
            'issues': CheckboxSelectMultiple(),
            'countries': RegionAccordionSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        user_skills = kwargs.pop('user_skills', None)
        user_countries = kwargs.pop('user_countries', None)
        super(MarketItemBaseForm, self).__init__(*args, **kwargs)
        if user_skills:
            self.fields['interests'].initial = user_skills
        if user_countries:
            self.fields['countries'].initial = user_countries

    def clean_interests(self):
        data = self.cleaned_data['interests']
        specific_skill = self.cleaned_data['specific_skill']
        if len(data) == 0 and not specific_skill:
            raise forms.ValidationError(_("You must add at least one skill"))
        if len(data) > 4 or (len(data) > 3 and specific_skill):
            raise forms.ValidationError(_("Please select a maximum of 4 skills"))
        return data

    def clean_title(self):
        data = self.cleaned_data['title']
        if len(data) > 120:
            raise forms.ValidationError(_("Please enter a maximum of 120 characters"))
        return data

    def save(self, commit=True, *args, **kwargs):
        self.instance.item_type = self.ITEM_TYPE
        if self.instance.id is None:
            self.instance.owner = kwargs['owner']
        return super(MarketItemBaseForm, self).save(commit=commit)


class OfferForm(MarketItemBaseForm):
    ITEM_TYPE = market.models.MarketItem.TYPE_CHOICES.OFFER

    def clean_issues(self):
        data = self.cleaned_data['issues']
        specific_issue = self.cleaned_data['specific_issue']
        if len(data) == 0 and not specific_issue:
            raise forms.ValidationError(_("You must add at least one issue"))
        return data


class RequestForm(MarketItemBaseForm):
    ITEM_TYPE = market.models.MarketItem.TYPE_CHOICES.REQUEST

    def clean_issues(self):
        data = self.cleaned_data['issues']
        specific_issue = self.cleaned_data['specific_issue']
        if len(data) == 0 and not specific_issue:
            raise forms.ValidationError(_("You must add at least one issue"))
        if len(data) >= 4 or (len(data) >= 3 and specific_issue):
            raise forms.ValidationError(_("Please select a maximum of 3 issues"))
        return data


class CommentForm(forms.ModelForm):
    class Meta:
        model = market.models.Comment
        fields = ['contents', ]

    def save(self, owner, item, commit=True):
        self.instance.owner = owner
        self.instance.item = item
        lang = detect_language(self.instance.contents)
        if lang:
            self.instance.language = lang
        return super(CommentForm, self).save(commit=commit)


def save_market_item(form, owner):
    """
    TODO - Alerts need to be sent to the admin for approval for new items, probably best done in the
           create notification?
    """
    new_item = form.instance.id is None
    obj = form.save(owner=owner)
    if new_item:
        on_market_item_creation.delay(obj)

        # detect language
        language = detect_language(obj.details)
        if language:
            obj.language = language
            obj.save()
    else:
        on_market_item_update.delay(obj)
    return obj


class ReportMarketItemForm(forms.ModelForm):
    class Meta:
        model = market.models.MarketItemPostReport
        fields = ['contents', ]


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
