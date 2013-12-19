import datetime
from haystack import indexes
from app.market.models import MarketItem
from app.users.models import UserProfile
from django.db.models import Q


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    details = indexes.CharField(model_attr='details')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return MarketItem

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects

def make_cond(name, value):
    from django.utils import simplejson
    cond = simplejson.dumps({name:value})[1:-1] # remove '{' and '}'
    return ' ' + cond # avoid '\"'


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    occupation = indexes.CharField(model_attr='occupation')

    def get_model(self):
        return UserProfile

    def index_queryset(self, using=None):
        #return self.get_model().objects.filter(~Q(notperm__contains=make_cond('bio','on')))
        return self.get_model().objects