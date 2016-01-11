# coding=utf-8

from django.conf import settings
from django.test import TestCase
from app.market.models import MarketNewsItemData, MarketItem
from app.market.utils import fetch_graph_data
from django_dynamic_fixture import G


class OpenGraphTestCase(TestCase):
    def test_fetch_graph_data(self):
        test_url = settings.BASE_URL + '/market/test/open-graph'
        test_graph_data = fetch_graph_data(test_url)
        self.assertTrue(test_graph_data.is_valid())
        self.assertEqual(test_graph_data.title, u'Graph Test Title')

    def test_fetch_news_item(self):
        test_url = settings.BASE_URL + '/market/test/open-graph'
        news_item = MarketNewsItemData.fetch_news_item(test_url)
        self.assertIsNotNone(news_item)
        self.assertEqual(news_item.original_url, test_url)
        self.assertEqual(news_item.title, 'Graph Test Title')
        self.assertEqual(news_item.url, 'http://www.newyorktimes.com/test-article')
        self.assertEqual(news_item.type, 'article')
        self.assertEqual(news_item.image, 'http://www.newyorktimes.com/image1.jpg')
        self.assertEqual(news_item.description, 'This is a short description')
        self.assertEqual(news_item.site_name, 'NYTimes')
        self.assertEqual(news_item.published, '2016-01-02T14:51:46.897Z')
        self.assertEqual(news_item.author_url, settings.BASE_URL + '/market/test/open-graph-author')
        self.assertEqual(news_item.author_name, 'Aidan Hamade')

    def test_date1(self):
        test_url = settings.BASE_URL + '/market/test/open-graph-date1'
        news_item = MarketNewsItemData.fetch_news_item(test_url)
        self.assertEqual(news_item.published, '2016-01-02')

    def test_date2(self):
        test_url = settings.BASE_URL + '/market/test/open-graph-date2'
        news_item = MarketNewsItemData.fetch_news_item(test_url)
        self.assertEqual(news_item.published, '2016-01-04')

    def test_create_news_item(self):
        test_url = settings.BASE_URL + '/market/test/open-graph'
        market_item = G(MarketItem)
        market_item.generate_news_item(test_url)
        news_item = MarketNewsItemData.objects.get(pk=market_item.id)
        self.assertIsNotNone(news_item)

