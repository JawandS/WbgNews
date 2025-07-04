"""
Test configuration and utilities for the Williamsburg News test suite
"""

import os
import tempfile
import sys
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test configuration
TEST_CONFIG = {
    'TESTING': True,
    'SECRET_KEY': 'test-secret-key',
    'WTF_CSRF_ENABLED': False,
    'DEBUG': False
}

# Mock data for testing
MOCK_WILLIAMSBURG_MEETINGS = [
    {
        'id': 'wb_test_001',
        'council': 'williamsburg',
        'council_name': 'Williamsburg City Council',
        'type': 'Regular Meeting',
        'title': 'Test City Council Regular Meeting',
        'date': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
        'time': '19:00',
        'agenda_url': 'https://example.com/agenda.pdf',
        'minutes_url': 'https://example.com/minutes.pdf',
        'status': 'completed'
    },
    {
        'id': 'wb_test_002',
        'council': 'williamsburg',
        'council_name': 'Williamsburg City Council',
        'type': 'Work Session',
        'title': 'Test Budget Work Session',
        'date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
        'time': '18:00',
        'agenda_url': 'https://example.com/agenda2.pdf',
        'minutes_url': None,
        'status': 'upcoming'
    }
]

MOCK_JAMES_CITY_MEETINGS = [
    {
        'id': 'jc_test_001',
        'council': 'james_city',
        'council_name': 'James City County Board of Supervisors',
        'type': 'Regular Meeting',
        'title': 'Test Board of Supervisors Regular Meeting',
        'date': (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
        'time': '19:00',
        'agenda_url': 'https://example.com/jc_agenda.pdf',
        'minutes_url': 'https://example.com/jc_minutes.pdf',
        'status': 'completed'
    },
    {
        'id': 'jc_test_002',
        'council': 'james_city',
        'council_name': 'James City County Board of Supervisors',
        'type': 'Public Hearing',
        'title': 'Test Public Hearing',
        'date': (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'),
        'time': '16:00',
        'agenda_url': 'https://example.com/jc_agenda2.pdf',
        'minutes_url': None,
        'status': 'upcoming'
    }
]

MOCK_MEETING_DETAIL = {
    'id': 'test_meeting_001',
    'council': 'williamsburg',
    'title': 'Test City Council Regular Meeting',
    'date': '2025-07-01',
    'time': '19:00',
    'location': 'Test City Hall Council Chambers',
    'agenda_items': [
        'Call to Order',
        'Test Public Comment Period',
        'Approval of Test Minutes',
        'Test Budget Discussion',
        'Test Zoning Applications',
        'Test New Business',
        'Adjournment'
    ],
    'documents': [
        {'name': 'Test Meeting Agenda', 'url': 'https://example.com/test_agenda.pdf', 'type': 'agenda'},
        {'name': 'Test Meeting Minutes', 'url': 'https://example.com/test_minutes.pdf', 'type': 'minutes'}
    ]
}

class TestDataGenerator:
    """Utility class for generating test data"""
    
    @staticmethod
    def create_test_meeting(council='williamsburg', days_offset=0, status='completed'):
        """Create a test meeting with customizable parameters"""
        meeting_date = datetime.now() + timedelta(days=days_offset)
        
        council_info = {
            'williamsburg': {
                'council_name': 'Williamsburg City Council',
                'prefix': 'wb_'
            },
            'james_city': {
                'council_name': 'James City County Board of Supervisors',
                'prefix': 'jc_'
            }
        }
        
        info = council_info.get(council, council_info['williamsburg'])
        
        return {
            'id': f"{info['prefix']}test_{abs(hash(f'{council}_{days_offset}')) % 10000}",
            'council': council,
            'council_name': info['council_name'],
            'type': 'Regular Meeting',
            'title': f"Test {info['council_name']} Meeting",
            'date': meeting_date.strftime('%Y-%m-%d'),
            'time': '19:00',
            'agenda_url': f'https://example.com/{council}_agenda.pdf' if status == 'completed' else None,
            'minutes_url': f'https://example.com/{council}_minutes.pdf' if status == 'completed' else None,
            'status': status
        }
    
    @staticmethod
    def create_test_meetings_list(count=5):
        """Create a list of test meetings"""
        meetings = []
        
        for i in range(count):
            # Alternate between councils
            council = 'williamsburg' if i % 2 == 0 else 'james_city'
            # Mix of past and future meetings
            days_offset = -i if i < count // 2 else i - count // 2
            status = 'completed' if days_offset < 0 else 'upcoming'
            
            meeting = TestDataGenerator.create_test_meeting(council, days_offset, status)
            meetings.append(meeting)
        
        # Sort by date (newest first)
        meetings.sort(key=lambda x: x['date'], reverse=True)
        return meetings

class MockHTTPResponse:
    """Mock HTTP response for testing web scraping"""
    
    def __init__(self, content, status_code=200):
        self.content = content.encode('utf-8') if isinstance(content, str) else content
        self.status_code = status_code
        self.text = content if isinstance(content, str) else content.decode('utf-8')
    
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code} Error")

def create_mock_html_response(meetings_count=3):
    """Create a mock HTML response that looks like a government website"""
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Test Government Site</title></head>
    <body>
        <h1>Meeting Schedule</h1>
        <table>
    """
    
    for i in range(meetings_count):
        date = (datetime.now() - timedelta(days=i*7)).strftime('%m/%d/%Y')
        html += f"""
            <tr class="RowStyle">
                <td>{date} 7:00 PM</td>
                <td>Regular Meeting {i+1}</td>
                <td><a href="/Agenda_{i+1}.pdf">Agenda</a></td>
                <td><a href="/Minutes_{i+1}.pdf">Minutes</a></td>
            </tr>
        """
    
    html += """
        </table>
        <div class="meeting">
            <h3>Upcoming Meeting</h3>
            <p>January 15, 2025 - Regular Board Meeting</p>
        </div>
    </body>
    </html>
    """
    
    return html

# Test utilities
def get_test_database_url():
    """Get a temporary database URL for testing"""
    db_fd, db_path = tempfile.mkstemp()
    return f'sqlite:///{db_path}', db_fd, db_path

def cleanup_test_database(db_fd, db_path):
    """Clean up test database"""
    os.close(db_fd)
    os.unlink(db_path)

def assert_meeting_structure(meeting_dict, test_case):
    """Assert that a meeting dictionary has the correct structure"""
    required_fields = ['id', 'council', 'council_name', 'title', 'date', 'time', 'status']
    
    for field in required_fields:
        test_case.assertIn(field, meeting_dict, f"Missing required field: {field}")
    
    test_case.assertIn(meeting_dict['council'], ['williamsburg', 'james_city'])
    test_case.assertIn(meeting_dict['status'], ['completed', 'upcoming'])
    
    # Test date format
    try:
        datetime.strptime(meeting_dict['date'], '%Y-%m-%d')
    except ValueError:
        test_case.fail(f"Invalid date format: {meeting_dict['date']}")
    
    # Test time format
    test_case.assertRegex(meeting_dict['time'], r'^\d{2}:\d{2}$', "Invalid time format")

def assert_api_response_structure(response_data, test_case):
    """Assert that an API response has the correct structure"""
    test_case.assertIn('success', response_data)
    test_case.assertIsInstance(response_data['success'], bool)
    
    if response_data['success']:
        test_case.assertIn('meetings', response_data)
        test_case.assertIsInstance(response_data['meetings'], list)
        
        for meeting in response_data['meetings']:
            assert_meeting_structure(meeting, test_case)
    else:
        test_case.assertIn('error', response_data)
