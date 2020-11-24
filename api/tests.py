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


class CounterFunctionalTests(unittest.TestCase):
    def setUp(self):
        from api import main
        app = main({})
        from webtest import TestApp

        self.testapp = TestApp(app)

    def test_home(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'status', res.body)
