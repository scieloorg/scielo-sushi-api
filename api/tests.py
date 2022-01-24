import unittest

from pyramid import testing


class CounterViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home(self):
        from .views import CounterViews

        request = testing.DummyRequest()
        inst = CounterViews(request)
        response = inst.home()
        self.assertEqual('200', response.get('status', ''))
