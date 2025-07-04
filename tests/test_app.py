"""
Test suite for the Williamsburg News Flask application
"""

import unittest
import json
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the path to import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from services.williamsburg_scraper import WilliamsburgScraper
from services.james_city_scraper import JamesCityScraper

class TestFlaskApp(unittest.TestCase):
    """Test cases for the Flask application routes"""

    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        """Test the main index route"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Williamsburg News', response.data)
        self.assertIn(b'Local Government', response.data)

    def test_williamsburg_route(self):
        """Test the Williamsburg council route"""
        response = self.app.get('/williamsburg')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Williamsburg City Council', response.data)

    def test_james_city_route(self):
        """Test the James City county route"""
        response = self.app.get('/james-city')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'James City County', response.data)

    def test_api_meetings_route(self):
        """Test the API meetings endpoint"""
        response = self.app.get('/api/meetings')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('success', data)
        self.assertIn('meetings', data)
        self.assertIsInstance(data['meetings'], list)

    def test_api_meeting_details_williamsburg(self):
        """Test the API meeting details endpoint for Williamsburg"""
        response = self.app.get('/api/meeting/williamsburg/test_id')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('success', data)
        self.assertIn('meeting', data)

    def test_api_meeting_details_james_city(self):
        """Test the API meeting details endpoint for James City"""
        response = self.app.get('/api/meeting/james_city/test_id')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('success', data)
        self.assertIn('meeting', data)

    def test_api_invalid_council(self):
        """Test API with invalid council parameter"""
        response = self.app.get('/api/meeting/invalid/test_id')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('error', data)

    def test_meeting_detail_route(self):
        """Test the meeting detail route"""
        response = self.app.get('/meeting/williamsburg/test_id')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Meeting Details', response.data)

    def test_404_error(self):
        """Test 404 error handling"""
        response = self.app.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404', response.data)


class TestWilliamsburgScraper(unittest.TestCase):
    """Test cases for the Williamsburg scraper"""

    def setUp(self):
        """Set up the scraper"""
        self.scraper = WilliamsburgScraper()

    def test_scraper_initialization(self):
        """Test scraper initializes correctly"""
        self.assertIsInstance(self.scraper, WilliamsburgScraper)
        self.assertEqual(self.scraper.base_url, "https://williamsburg.civicweb.net")

    def test_get_recent_meetings(self):
        """Test getting recent meetings (will use mock data)"""
        meetings = self.scraper.get_recent_meetings()
        self.assertIsInstance(meetings, list)
        
        if meetings:
            meeting = meetings[0]
            self.assertIn('id', meeting)
            self.assertIn('council', meeting)
            self.assertIn('title', meeting)
            self.assertIn('date', meeting)
            self.assertEqual(meeting['council'], 'williamsburg')

    def test_parse_date(self):
        """Test date parsing functionality"""
        # Test various date formats
        test_dates = [
            ('1/15/2025', '2025-01-15'),
            ('January 15, 2025', '2025-01-15'),
            ('Jan 15, 2025', '2025-01-15'),
        ]
        
        for date_str, expected in test_dates:
            parsed = self.scraper._parse_date(date_str)
            if parsed:
                self.assertEqual(parsed.strftime('%Y-%m-%d'), expected)

    def test_get_meeting_details(self):
        """Test getting meeting details"""
        details = self.scraper.get_meeting_details('test_id')
        self.assertIsInstance(details, dict)
        
        if details:
            self.assertIn('id', details)
            self.assertIn('council', details)
            self.assertEqual(details['council'], 'williamsburg')

    def test_get_mock_meetings(self):
        """Test mock meetings generation"""
        mock_meetings = self.scraper._get_mock_meetings()
        self.assertIsInstance(mock_meetings, list)
        self.assertGreater(len(mock_meetings), 0)
        
        for meeting in mock_meetings:
            self.assertEqual(meeting['council'], 'williamsburg')
            self.assertIn('id', meeting)
            self.assertIn('title', meeting)
            self.assertIn('date', meeting)


class TestJamesCityScraper(unittest.TestCase):
    """Test cases for the James City scraper"""

    def setUp(self):
        """Set up the scraper"""
        self.scraper = JamesCityScraper()

    def test_scraper_initialization(self):
        """Test scraper initializes correctly"""
        self.assertIsInstance(self.scraper, JamesCityScraper)
        self.assertEqual(self.scraper.base_url, "https://www.jamescitycountyva.gov")

    def test_get_recent_meetings(self):
        """Test getting recent meetings (will use mock data)"""
        meetings = self.scraper.get_recent_meetings()
        self.assertIsInstance(meetings, list)
        
        if meetings:
            meeting = meetings[0]
            self.assertIn('id', meeting)
            self.assertIn('council', meeting)
            self.assertIn('title', meeting)
            self.assertIn('date', meeting)
            self.assertEqual(meeting['council'], 'james_city')

    def test_parse_date(self):
        """Test date parsing functionality"""
        test_dates = [
            ('January 15, 2025', '2025-01-15'),
            ('1/15/2025', '2025-01-15'),
            ('2025-01-15', '2025-01-15'),
        ]
        
        for date_str, expected in test_dates:
            parsed = self.scraper._parse_date(date_str)
            if parsed:
                self.assertEqual(parsed.strftime('%Y-%m-%d'), expected)

    def test_make_absolute_url(self):
        """Test URL conversion"""
        test_cases = [
            ('https://example.com/path', 'https://example.com/path'),
            ('/relative/path', 'https://www.jamescitycountyva.gov/relative/path'),
            ('relative/path', 'https://www.jamescitycountyva.gov/relative/path'),
        ]
        
        for input_url, expected in test_cases:
            result = self.scraper._make_absolute_url(input_url)
            self.assertEqual(result, expected)

    def test_get_meeting_details(self):
        """Test getting meeting details"""
        details = self.scraper.get_meeting_details('test_id')
        self.assertIsInstance(details, dict)
        
        if details:
            self.assertIn('id', details)
            self.assertIn('council', details)
            self.assertEqual(details['council'], 'james_city')

    def test_get_mock_meetings(self):
        """Test mock meetings generation"""
        mock_meetings = self.scraper._get_mock_meetings()
        self.assertIsInstance(mock_meetings, list)
        self.assertGreater(len(mock_meetings), 0)
        
        for meeting in mock_meetings:
            self.assertEqual(meeting['council'], 'james_city')
            self.assertIn('id', meeting)
            self.assertIn('title', meeting)
            self.assertIn('date', meeting)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete application"""

    def setUp(self):
        """Set up test client and scrapers"""
        self.app = app.test_client()
        self.app.testing = True
        self.williamsburg_scraper = WilliamsburgScraper()
        self.james_city_scraper = JamesCityScraper()

    def test_end_to_end_meetings_flow(self):
        """Test the complete flow from scraping to API response"""
        # Test that scrapers return data
        wb_meetings = self.williamsburg_scraper.get_recent_meetings()
        jc_meetings = self.james_city_scraper.get_recent_meetings()
        
        self.assertIsInstance(wb_meetings, list)
        self.assertIsInstance(jc_meetings, list)
        
        # Test that API returns combined data
        response = self.app.get('/api/meetings')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['meetings'], list)

    def test_meeting_data_structure(self):
        """Test that meeting data has the required structure"""
        response = self.app.get('/api/meetings')
        data = json.loads(response.data)
        
        if data['meetings']:
            meeting = data['meetings'][0]
            required_fields = ['id', 'council', 'title', 'date', 'time', 'status']
            
            for field in required_fields:
                self.assertIn(field, meeting, f"Missing required field: {field}")
            
            # Test council values
            self.assertIn(meeting['council'], ['williamsburg', 'james_city'])
            
            # Test status values
            self.assertIn(meeting['status'], ['completed', 'upcoming'])

    def test_date_sorting(self):
        """Test that meetings are sorted by date"""
        response = self.app.get('/api/meetings')
        data = json.loads(response.data)
        
        if len(data['meetings']) > 1:
            dates = [meeting['date'] for meeting in data['meetings']]
            sorted_dates = sorted(dates, reverse=True)
            self.assertEqual(dates, sorted_dates, "Meetings should be sorted by date (newest first)")


if __name__ == '__main__':
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestFlaskApp,
        TestWilliamsburgScraper,
        TestJamesCityScraper,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with error code if tests failed
    if not result.wasSuccessful():
        sys.exit(1)
