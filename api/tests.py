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


class CleanerTests(unittest.TestCase):
    """Tests for cleaner module functions"""
    
    def test_clean_collection_acronym_with_valid_collection(self):
        """Test that valid collection acronyms are returned as-is"""
        from api.libs import cleaner
        
        self.assertEqual('scl', cleaner.clean_collection_acronym('scl'))
        self.assertEqual('ssp', cleaner.clean_collection_acronym('ssp'))
        self.assertEqual('dom', cleaner.clean_collection_acronym('dom'))
        self.assertEqual('arg', cleaner.clean_collection_acronym('arg'))
    
    def test_clean_collection_acronym_with_empty_collection(self):
        """Test that empty collection defaults to 'scl'"""
        from api.libs import cleaner
        
        self.assertEqual('scl', cleaner.clean_collection_acronym(''))
        self.assertEqual('scl', cleaner.clean_collection_acronym(None))
    
    def test_clean_collection_acronym_no_fallback_for_unknown(self):
        """Test that unknown collections are returned as-is, not defaulted to 'scl'"""
        from api.libs import cleaner
        
        # Unknown collections should be returned as-is
        self.assertEqual('xyz', cleaner.clean_collection_acronym('xyz'))
        self.assertEqual('unknown', cleaner.clean_collection_acronym('unknown'))


class UtilsTests(unittest.TestCase):
    """Tests for utils module functions"""
    
    def test_set_collection_extra_for_scl(self):
        """Test that scl collection gets nbr as collection_extra"""
        from api import utils
        
        attrs = {'collection': 'scl', 'api': 'v2'}
        utils.set_collection_extra('cr_j1', attrs)
        
        self.assertEqual('nbr', attrs.get('collection_extra'))
    
    def test_set_collection_extra_for_nbr(self):
        """Test that nbr collection gets scl as collection_extra"""
        from api import utils
        
        attrs = {'collection': 'nbr', 'api': 'v2'}
        utils.set_collection_extra('cr_j1', attrs)
        
        self.assertEqual('scl', attrs.get('collection_extra'))
    
    def test_set_collection_extra_for_other_collections(self):
        """Test that other collections get empty string as collection_extra"""
        from api import utils
        
        # Test for 'ssp' collection
        attrs = {'collection': 'ssp', 'api': 'v2'}
        utils.set_collection_extra('cr_j1', attrs)
        self.assertEqual('', attrs.get('collection_extra'))
        
        # Test for 'dom' collection
        attrs = {'collection': 'dom', 'api': 'v2'}
        utils.set_collection_extra('cr_j1', attrs)
        self.assertEqual('', attrs.get('collection_extra'))
        
        # Test for 'arg' collection
        attrs = {'collection': 'arg', 'api': 'v2'}
        utils.set_collection_extra('cr_j1', attrs)
        self.assertEqual('', attrs.get('collection_extra'))


class AdapterTests(unittest.TestCase):
    """Tests for adapter module functions"""
    
    def test_json_cr_j1_with_empty_data(self):
        """Test that cr_j1 returns zero counts when no data is available"""
        from api import adapter
        from api.models.sql_declarative import Report
        
        # Mock params
        params = {
            'collection': 'dom',
            'customer': 'test',
            'begin_date': '2020-01-01',
            'end_date': '2020-12-31',
            'platform': 'Scientific Electronic Library Online - Test',
            'report_db_params': Report(
                report_id='cr_j1',
                release='5',
                name='Collection Report',
                description='Test',
                path='/reports/cr_j1'
            )
        }
        
        # Call with empty data
        result = adapter._json_cr_j1([], params, [])
        
        # Verify structure
        self.assertIn('Report_Header', result)
        self.assertIn('Report_Items', result)
        self.assertEqual(1, len(result['Report_Items']))
        
        # Verify the collection title matches requested collection
        report_item = result['Report_Items'][0]
        self.assertEqual('dom', report_item['Title'])
        
        # Verify Performance has entries with zero counts
        self.assertIn('Performance', report_item)
        self.assertEqual(2, len(report_item['Performance']))
        
        # Check that counts are zero
        for performance in report_item['Performance']:
            self.assertEqual('0', performance['Instance']['Count'])
    
    def test_json_cr_j1_title_matches_requested_collection(self):
        """Test that Title in Report_Items always matches the requested collection"""
        from api import adapter
        from api.models.sql_declarative import Report
        from collections import namedtuple
        
        # Create mock result
        MockResult = namedtuple('MockResult', ['beginDate', 'endDate', 'totalItemRequests', 'uniqueItemRequests'])
        mock_data = [MockResult('2020-01-01', '2020-12-31', 100, 50)]
        
        # Mock params with 'ssp' collection
        params = {
            'collection': 'ssp',
            'customer': 'test',
            'begin_date': '2020-01-01',
            'end_date': '2020-12-31',
            'platform': 'Scientific Electronic Library Online - Test',
            'report_db_params': Report(
                report_id='cr_j1',
                release='5',
                name='Collection Report',
                description='Test',
                path='/reports/cr_j1'
            )
        }
        
        # Call with mock data
        result = adapter._json_cr_j1(mock_data, params, [])
        
        # Verify the Title matches the requested collection, not the data collection
        self.assertEqual(1, len(result['Report_Items']))
        self.assertEqual('ssp', result['Report_Items'][0]['Title'])
