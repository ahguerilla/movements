# coding=utf-8

from django.test import TestCase
import opengraph


class OpenGraphTestCase(TestCase):
    def test_open_graph(self):
        test_graph_data = opengraph.OpenGraph(url="/market/tests/opengraph.html")
        self.assertTrue(test_graph_data.is_valid())
        self.assertEqual(test_graph_data.title, u'Graph Test Title')
