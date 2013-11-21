import datetime
from haystack import indexes
from app.market.models import MarketItem


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    details = indexes.CharField(model_attr='details')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return MarketItem

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())