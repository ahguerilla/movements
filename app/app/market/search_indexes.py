from haystack import indexes
from app.market.models import MarketItem
from app.users.models import UserProfile


class MarketItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    details = indexes.EdgeNgramField(model_attr='details')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return MarketItem

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(deleted=False)

def make_cond(name, value):
    from django.utils import simplejson
    cond = simplejson.dumps({name:value})[1:-1] # remove '{' and '}'
    return ' ' + cond # avoid '\"'


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    username = indexes.EdgeNgramField()
    occupation = indexes.EdgeNgramField(model_attr='occupation')
    bio = indexes.EdgeNgramField(model_attr='bio')
    expertise = indexes.EdgeNgramField(model_attr='expertise')
    tag_ling = indexes.EdgeNgramField(model_attr='tag_ling')
    nationality = indexes.EdgeNgramField(model_attr='nationality')
    resident_country = indexes.EdgeNgramField(model_attr='resident_country')

    def prepare_username(self,obj):
        return obj.user.username


    def prepare_resident_country(self,obj):
        if obj.notperm.has_key('resident_country'):
            return ''
        return obj.resident_country.residence


    def prepare_nationality(self, obj):
        if obj.notperm.has_key('nationality'):
            return ''
        return obj.nationality.nationality


    def prepate_bio(self, obj):
        if obj.notperm.has_key('bio'):
            return ''
        return obj.bio


    def prepare_expertise(self, obj):
        if obj.notperm.has_key('expertise'):
            return ''
        return obj.expertise


    def prepare_tag_ling(self, obj):
        if obj.notperm.has_key('tag_ling'):
            return ''
        return obj.tag_ling

    def prepare_occupation(self, obj):
        if obj.notperm.has_key('occupation'):
            return ''
        return obj.occupation


    def get_model(self):
        return UserProfile


    def index_queryset(self, using=None):
        #return self.get_model().objects.filter(~Q(notperm__contains=make_cond('bio','on')))
        return self.get_model().objects