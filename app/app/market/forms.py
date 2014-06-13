from django import forms
from django.utils.cache import get_cache
from django.utils.translation import ugettext_lazy as _

from postman.forms import WriteForm, FullReplyForm, QuickReplyForm

from tasks.celerytasks import create_notification, update_notifications
import app.market as market


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
    exp_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M', ], required=False)

    class Meta:
        model = market.models.MarketItem
        fields = ['title', 'details', 'exp_date', 'never_exp', 'specific_skill',
                  'receive_notifications']
        widgets = {
            'details': forms.Textarea(attrs={'cols': 55, 'rows': 5, 'class': "form-control"}),
        }

    def clean(self):
        err = _('You should enter an expiry date for your offer or check never expires')
        cleaned_data = super(OfferForm, self).clean()
        check = [cleaned_data['exp_date'], cleaned_data['never_exp']]
        if not any(check):
            self._errors['exp_date'] = self.error_class([err])
        return cleaned_data

    def save(self, commit=True, *args, **kwargs):
        self.instance.item_type = market.models.MarketItem.TYPE_CHOICES.OFFER
        if self.instance.id is None:
            self.instance.owner = kwargs['owner']
        return super(OfferForm, self).save(commit=commit)


class RequestForm(forms.ModelForm):
    exp_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M', ], required=False)

    class Meta:
        model = market.models.MarketItem
        fields = ['title', 'details', 'exp_date', 'never_exp', 'specific_skill',
                  'receive_notifications']
        widgets = {
            'details': forms.Textarea(attrs={'cols': 55, 'rows': 5, 'class': "form-control"}),
        }

    def clean(self):
        err = _('You should enter an expiry date for your request or check never expires')
        cleaned_data = super(RequestForm, self).clean()
        check = [cleaned_data['exp_date'], cleaned_data['never_exp']]
        if not any(check):
            self._errors['exp_date'] = self.error_class([err])

        return cleaned_data

    def save(self, commit=True, *args, **kwargs):
        self.instance.item_type = market.models.MarketItem.TYPE_CHOICES.REQUEST
        if self.instance.id is None:
            self.instance.owner = kwargs['owner']
        return super(RequestForm, self).save(commit=commit)


class commentForm(forms.ModelForm):
    class Meta:
        model = market.models.Comment
        fields = ['contents', ]

    def save(self, commit=False, *args, **kwargs):
        instance = super(commentForm, self).save(commit=commit, *args, **kwargs)
        if instance.pk == None:
            instance.owner = self.cleaned_data['owner']
            instance.item = self.cleaned_data['item']
        return instance


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


class reportMarketItemForm(forms.ModelForm):
    class Meta:
        model = market.models.MarketItemPostReport
        fields = ['contents', ]


class reportUserForm(forms.ModelForm):
    class Meta:
        model = market.models.UserReport
        fields = ['contents', ]
