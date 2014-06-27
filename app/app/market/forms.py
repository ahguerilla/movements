from django import forms
from django.utils.cache import get_cache
from postman.forms import WriteForm, FullReplyForm, QuickReplyForm
from tasks.celerytasks import create_notification, update_notifications

import app.market as market
from app.users.forms import CheckboxSelectMultiple


cache = get_cache('default')
items_cache = get_cache('items')
user_items_cache = get_cache('user_items')


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


class OfferForm(forms.ModelForm):
    class Meta:
        model = market.models.MarketItem
        fields = ['title', 'details', 'specific_skill', 'receive_notifications', 'interests']
        widgets = {
            'details': forms.Textarea(attrs={'cols': 55, 'rows': 5, 'class': "form-control"}),
            'interests': CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        user_skills = kwargs.pop('user_skills', None)
        super(OfferForm, self).__init__(*args, **kwargs)
        if user_skills:
            self.fields['interests'].initial = user_skills

    def save(self, commit=True, *args, **kwargs):
        self.instance.item_type = market.models.MarketItem.TYPE_CHOICES.OFFER
        if self.instance.id is None:
            self.instance.owner = kwargs['owner']
        return super(OfferForm, self).save(commit=commit)


class RequestForm(forms.ModelForm):
    class Meta:
        model = market.models.MarketItem
        fields = ['title', 'details', 'specific_skill',
                  'receive_notifications', 'interests']
        widgets = {
            'details': forms.Textarea(attrs={'cols': 55, 'rows': 5, 'class': "form-control"}),
            'interests': CheckboxSelectMultiple(),
            'specific_skill': forms.Textarea(attrs={'cols': 55, 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        user_skills = kwargs.pop('user_skills', None)
        super(RequestForm, self).__init__(*args, **kwargs)
        if user_skills:
            self.fields['interests'].initial = user_skills

    def save(self, commit=True, *args, **kwargs):
        self.instance.item_type = market.models.MarketItem.TYPE_CHOICES.REQUEST
        if self.instance.id is None:
            self.instance.owner = kwargs['owner']
        return super(RequestForm, self).save(commit=commit)


class CommentForm(forms.ModelForm):
    class Meta:
        model = market.models.Comment
        fields = ['contents', ]

    def save(self, owner, item, commit=True):
        self.instance.owner = owner
        self.instance.item = item
        return super(CommentForm, self).save(commit=commit)


def save_market_item(form, owner):
    """
    TODO - I've moved code here from the api views but not really checked if it's sane, cache clearing stuff
           seems badly thought out.
    TODO - Alerts need to be sent to the admin for approval for new items, probably best done in the
           create notification?
    """
    new_item = form.instance.id is None
    obj = form.save(owner=owner)
    items_cache.clear()
    user_items_cache.clear()
    if new_item:
        create_notification.delay(obj)
    else:
        cache.delete('item-' + str(obj.id))
        cache.delete('translation-' + str(obj.id))
        update_notifications.delay(obj)
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
