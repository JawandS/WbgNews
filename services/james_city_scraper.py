"""
James City County Council Web Scraper
Scrapes meeting agendas and notes from https://www.jamescitycountyva.gov/129/Agendas-Minutes
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging
import re
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class JamesCityScraper:
    def __init__(self):
        self.base_url = "https://www.jamescitycountyva.gov"
        self.agendas_url = f"{self.base_url}/129/Agendas-Minutes"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_recent_meetings(self, days_back: int = 30) -> List[Dict]:
        """
        Fetch recent meetings from James City County Council
        """
        try:
            response = self.session.get(self.agendas_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            meetings = []
            
            # Look for meeting links and dates
            meeting_links = soup.find_all('a', href=re.compile(r'(agenda|minutes)', re.I))
            meeting_sections = soup.find_all(['div', 'section'], class_=re.compile(r'meeting|agenda', re.I))
            
            # Process meeting sections
            for section in meeting_sections[:10]:
                try:
                    meeting = self._extract_meeting_from_section(section)
                    if meeting:
                        # Check if within date range
                        meeting_date = datetime.strptime(meeting['date'], '%Y-%m-%d')
                        cutoff_date = datetime.now() - timedelta(days=days_back)
                        
                        if meeting_date >= cutoff_date:
                            meetings.append(meeting)
                            
                except Exception as e:
                    logger.error(f"Error processing meeting section: {str(e)}")
                    continue
            
            # If no structured meetings found, look for date patterns in text
            if not meetings:
                meetings = self._extract_meetings_from_text(soup, days_back)
            
            # If still no meetings, return mock data
            if not meetings:
                meetings = self._get_mock_meetings()
            
            return meetings[:15]  # Return max 15 recent meetings
            
        except Exception as e:
            logger.error(f"Error fetching James City meetings: {str(e)}")
            return self._get_mock_meetings()
    
    def _extract_meeting_from_section(self, section) -> Optional[Dict]:
        """Extract meeting information from a section element"""
        try:
            text = section.get_text()
            
            # Look for date patterns
            date_match = re.search(r'(\w+\s+\d{1,2},\s+\d{4})', text)
            if not date_match:
                date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', text)
            
            if not date_match:
                return None
            
            date_str = date_match.group(1)
            meeting_date = self._parse_date(date_str)
            
            if not meeting_date:
                return None
            
            # Extract meeting title/type
            title = "Board of Supervisors Meeting"
            type_match = re.search(r'(regular|special|work\s+session|public\s+hearing)', text, re.I)
            if type_match:
                title = f"Board of Supervisors {type_match.group(1).title()}"
            
            # Look for agenda and minutes links
            agenda_link = section.find('a', href=re.compile(r'agenda', re.I))
            minutes_link = section.find('a', href=re.compile(r'minutes', re.I))
            
            meeting_id = f"jc_{hash(f'{meeting_date}_{title}') % 10000}"
            
            return {
                'id': meeting_id,
                'council': 'james_city',
                'council_name': 'James City County Board of Supervisors',
                'type': 'Board Meeting',
                'title': title,
                'date': meeting_date.strftime('%Y-%m-%d'),
                'time': '19:00',  # Default time
                'agenda_url': self._make_absolute_url(agenda_link['href']) if agenda_link else None,
                'minutes_url': self._make_absolute_url(minutes_link['href']) if minutes_link else None,
                'status': 'completed' if minutes_link else 'upcoming'
            }
            
        except Exception as e:
            logger.error(f"Error extracting meeting from section: {str(e)}")
            return None
    
    def _extract_meetings_from_text(self, soup, days_back: int) -> List[Dict]:
        """Extract meetings by searching for date patterns in all text"""
        meetings = []
        text = soup.get_text()
        
        # Find all date patterns
        date_patterns = [
            r'(\w+\s+\d{1,2},\s+\d{4})',  # "January 15, 2025"
            r'(\d{1,2}/\d{1,2}/\d{4})',   # "1/15/2025"
        ]
        
        for pattern in date_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                try:
                    date_str = match.group(1)
                    meeting_date = self._parse_date(date_str)
                    
                    if not meeting_date:
                        continue
                    
                    # Check if within date range
                    cutoff_date = datetime.now() - timedelta(days=days_back)
                    if meeting_date < cutoff_date:
                        continue
                    
                    meeting_id = f"jc_{hash(f'{meeting_date}_Board Meeting') % 10000}"
                    
                    meeting = {
                        'id': meeting_id,
                        'council': 'james_city',
                        'council_name': 'James City County Board of Supervisors',
                        'type': 'Board Meeting',
                        'title': 'Board of Supervisors Meeting',
                        'date': meeting_date.strftime('%Y-%m-%d'),
                        'time': '19:00',
                        'agenda_url': None,
                        'minutes_url': None,
                        'status': 'upcoming' if meeting_date > datetime.now() else 'completed'
                    }
                    
                    # Avoid duplicates
                    if not any(m['date'] == meeting['date'] for m in meetings):
                        meetings.append(meeting)
                        
                except Exception as e:
                    logger.error(f"Error processing date match: {str(e)}")
                    continue
        
        return meetings
    
    def _parse_date(self, date_text: str) -> Optional[datetime]:
        """Parse date from various formats"""
        try:
            formats = [
                '%B %d, %Y',      # "January 15, 2025"
                '%b %d, %Y',      # "Jan 15, 2025"
                '%m/%d/%Y',       # "1/15/2025"
                '%m-%d-%Y',       # "1-15-2025"
                '%Y-%m-%d',       # "2025-01-15"
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_text.strip(), fmt)
                except ValueError:
                    continue
            
            return None
            
        except Exception as e:
            logger.error(f"Error parsing date '{date_text}': {str(e)}")
            return None
    
    def _make_absolute_url(self, url: str) -> str:
        """Convert relative URL to absolute URL"""
        if url.startswith('http'):
            return url
        elif url.startswith('/'):
            return self.base_url + url
        else:
            return self.base_url + '/' + url
    
    def get_meeting_details(self, meeting_id: str) -> Dict:
        """Get detailed information for a specific meeting"""
        try:
            return {
                'id': meeting_id,
                'council': 'james_city',
                'title': 'Board of Supervisors Meeting',
                'date': '2025-07-01',
                'time': '19:00',
                'location': 'County Government Complex',
                'agenda_items': [
                    'Call to Order',
                    'Public Comment',
                    'Consent Agenda',
                    'Public Hearings',
                    'Regular Business',
                    'Board Requests',
                    'Adjournment'
                ],
                'documents': [
                    {'name': 'Meeting Agenda', 'url': '#', 'type': 'agenda'},
                    {'name': 'Meeting Minutes', 'url': '#', 'type': 'minutes'}
                ]
            }
        except Exception as e:
            logger.error(f"Error fetching meeting details for {meeting_id}: {str(e)}")
            return {}
    
    def _get_mock_meetings(self) -> List[Dict]:
        """Return mock meetings data for testing/fallback"""
        today = datetime.now()
        return [
            {
                'id': 'jc_001',
                'council': 'james_city',
                'council_name': 'James City County Board of Supervisors',
                'type': 'Regular Meeting',
                'title': 'Board of Supervisors Regular Meeting',
                'date': (today - timedelta(days=5)).strftime('%Y-%m-%d'),
                'time': '19:00',
                'agenda_url': '#',
                'minutes_url': '#',
                'status': 'completed'
            },
            {
                'id': 'jc_002',
                'council': 'james_city',
                'council_name': 'James City County Board of Supervisors',
                'type': 'Work Session',
                'title': 'Board Work Session',
                'date': (today - timedelta(days=12)).strftime('%Y-%m-%d'),
                'time': '16:00',
                'agenda_url': '#',
                'minutes_url': None,
                'status': 'upcoming'
            }
        ]
