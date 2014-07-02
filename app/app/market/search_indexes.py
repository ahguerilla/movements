from haystack import indexes
from app.market.models import MarketItem


class MarketItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    details = indexes.EdgeNgramField(model_attr='details')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return MarketItem

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(deleted=False)
