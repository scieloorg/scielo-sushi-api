import unittest
from concurrent.futures import ThreadPoolExecutor
from os import environ
from threading import Barrier, Event
from unittest.mock import Mock, patch

from pyramid.request import Request

from api import main
from api.libs import db
from api.models.sql_automap import Base, DBSession


class IrA1LimitTests(unittest.TestCase):
    article_url = (
        '/reports/ir_a1?begin_date=2020-01&end_date=2020-02&collection=scl'
        '&api=v2&granularity=month&pid=10.1234/example'
    )
    journal_url = (
        '/reports/tr_j1?begin_date=2020-01&end_date=2020-02&collection=scl'
        '&api=v2&granularity=month&issn=0102-8650'
    )

    def _make_app(self, limit):
        self.addCleanup(setattr, Base.metadata, 'bind', Base.metadata.bind)
        settings = {'STR_CONNECTION': 'sqlite://', 'SUSHI_IR_A1_MAX_CONCURRENT': limit}
        with patch.dict(environ, settings), patch.object(DBSession, 'configure'):
            return main({}, **{'pyramid.includes': 'pyramid_tm'})

    def _request(self, app, url=None):
        return Request.blank(url or self.article_url).get_response(app)

    def _mock_database(self):
        mocks = {
            'collection_exists': Mock(return_value=True),
            'get_report_by_id': Mock(),
            'get_dates_not_ready': Mock(return_value=[]),
            'call_procedure': Mock(side_effect=lambda query: iter(())),
        }
        patcher = patch.multiple(db, **mocks)
        patcher.start()
        self.addCleanup(patcher.stop)
        return mocks

    def test_disabled_returns_503_before_database_access(self):
        app = self._make_app('0')
        mocks = self._mock_database()

        response = self._request(app, self.article_url + '&fmt=tsv')

        self.assertEqual(response.status_int, 503)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json_body['Code'], 1000)
        self.assertIn('disabled', response.json_body['Data'])
        self.assertEqual(response.headers['Cache-Control'], 'no-store')
        self.assertNotIn('Retry-After', response.headers)
        mocks['collection_exists'].assert_not_called()
        mocks['call_procedure'].assert_not_called()

    def test_saturated_report_rejects_without_waiting_and_spares_other_reports(self):
        app = self._make_app('2')
        mocks = self._mock_database()
        entered = Barrier(3)
        release = Event()

        def call_procedure(query):
            if 'V2_IR_A1_ARTICLE_MONTHLY' in query and not release.is_set():
                entered.wait(timeout=5)
                if not release.wait(timeout=10):
                    raise AssertionError('Test did not release the active reports')
            return iter(())

        mocks['call_procedure'].side_effect = call_procedure
        with ThreadPoolExecutor(max_workers=3) as executor:
            active = [executor.submit(self._request, app) for _ in range(2)]
            try:
                entered.wait(timeout=5)
                excess = executor.submit(self._request, app).result(timeout=2)
                self.assertEqual(excess.status_int, 503)
                self.assertIn('busy', excess.json_body['Data'])
                self.assertEqual(excess.headers['Retry-After'], '5')
                self.assertEqual(mocks['collection_exists'].call_count, 2)
                self.assertEqual(mocks['call_procedure'].call_count, 2)

                other = executor.submit(self._request, app, self.journal_url)
                self.assertEqual(other.result(timeout=2).status_int, 200)
                self.assertEqual(mocks['call_procedure'].call_count, 3)
            finally:
                release.set()
            for request in active:
                self.assertEqual(request.result(timeout=5).status_int, 200)

        self.assertEqual(self._request(app).status_int, 200)
        self.assertEqual(mocks['call_procedure'].call_count, 4)

    def test_slot_is_released_after_an_exception(self):
        app = self._make_app('1')
        mocks = self._mock_database()
        mocks['call_procedure'].side_effect = [RuntimeError('query failed'), iter(())]

        with self.assertRaisesRegex(RuntimeError, 'query failed'):
            self._request(app)

        self.assertEqual(self._request(app).status_int, 200)
        self.assertEqual(mocks['call_procedure'].call_count, 2)
