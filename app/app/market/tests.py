# coding=utf-8

from django.conf import settings
from django.test import TestCase
import opengraph


class OpenGraphTestCase(TestCase):
    def test_open_graph(self):
        test_url = settings.BASE_URL + '/market/test/open-graph'
        test_graph_data = opengraph.OpenGraph(url=test_url)
        self.assertTrue(test_graph_data.is_valid())
        self.assertEqual(test_graph_data.title, u'Graph Test Title')
