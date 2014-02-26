from django.test import TestCase


class MarketTestCase(TestCase):
    fixtures = ['test_data.json',]

    def setUp(self):
        # Test definitions as before.
        pass

    def testFluffyAnimals(self):
        # A test that uses the fixtures.
        pass
