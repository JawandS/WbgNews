"""
Williamsburg City Council Web Scraper
Scrapes meeting agendas and notes from https://williamsburg.civicweb.net/
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging
import re
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class WilliamsburgScraper:
    def __init__(self):
        self.base_url = "https://williamsburg.civicweb.net"
        self.meeting_types_url = f"{self.base_url}/Portal/MeetingTypeList.aspx"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_recent_meetings(self, days_back: int = 30) -> List[Dict]:
        """
        Fetch recent meetings from Williamsburg City Council
        """
        try:
            meetings = []
            
            # Get the main meeting types page
            response = self.session.get(self.meeting_types_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find meeting type links
            meeting_type_links = soup.find_all('a', href=re.compile(r'MeetingList\.aspx'))
            
            for link in meeting_type_links[:3]:  # Limit to first 3 meeting types
                try:
                    meeting_type = link.get_text(strip=True)
                    meeting_list_url = self.base_url + link['href']
                    
                    # Get meetings for this type
                    type_meetings = self._get_meetings_for_type(meeting_list_url, meeting_type, days_back)
                    meetings.extend(type_meetings)
                    
                except Exception as e:
                    logger.error(f"Error processing meeting type {meeting_type}: {str(e)}")
                    continue
            
            return meetings[:20]  # Return max 20 recent meetings
            
        except Exception as e:
            logger.error(f"Error fetching Williamsburg meetings: {str(e)}")
            return self._get_mock_meetings()  # Return mock data as fallback
    
    def _get_meetings_for_type(self, url: str, meeting_type: str, days_back: int) -> List[Dict]:
        """Get meetings for a specific meeting type"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            meetings = []
            
            # Look for meeting rows in tables
            meeting_rows = soup.find_all('tr', class_=re.compile(r'RowStyle|AlternatingRowStyle'))
            
            for row in meeting_rows[:10]:  # Limit per type
                try:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        # Extract meeting date and title
                        date_cell = cells[0]
                        title_cell = cells[1] if len(cells) > 1 else cells[0]
                        
                        date_text = date_cell.get_text(strip=True)
                        title_text = title_cell.get_text(strip=True)
                        
                        # Parse date
                        meeting_date = self._parse_date(date_text)
                        if not meeting_date:
                            continue
                        
                        # Check if within date range
                        cutoff_date = datetime.now() - timedelta(days=days_back)
                        if meeting_date < cutoff_date:
                            continue
                        
                        # Look for agenda/minutes links
                        agenda_link = row.find('a', href=re.compile(r'Agenda'))
                        minutes_link = row.find('a', href=re.compile(r'Minutes'))
                        
                        meeting = {
                            'id': f"wb_{hash(f'{meeting_date}_{title_text}') % 10000}",
                            'council': 'williamsburg',
                            'council_name': 'Williamsburg City Council',
                            'type': meeting_type,
                            'title': title_text,
                            'date': meeting_date.strftime('%Y-%m-%d'),
                            'time': meeting_date.strftime('%H:%M'),
                            'agenda_url': self.base_url + agenda_link['href'] if agenda_link else None,
                            'minutes_url': self.base_url + minutes_link['href'] if minutes_link else None,
                            'status': 'completed' if minutes_link else 'upcoming'
                        }
                        
                        meetings.append(meeting)
                        
                except Exception as e:
                    logger.error(f"Error processing meeting row: {str(e)}")
                    continue
            
            return meetings
            
        except Exception as e:
            logger.error(f"Error fetching meetings for type {meeting_type}: {str(e)}")
            return []
    
    def _parse_date(self, date_text: str) -> Optional[datetime]:
        """Parse date from various formats"""
        try:
            # Common date formats
            formats = [
                '%m/%d/%Y %I:%M %p',
                '%m/%d/%Y',
                '%B %d, %Y %I:%M %p',
                '%B %d, %Y',
                '%Y-%m-%d %H:%M',
                '%Y-%m-%d'
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_text.strip(), fmt)
                except ValueError:
                    continue
            
            # If no format matches, try to extract date parts
            date_match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', date_text)
            if date_match:
                month, day, year = date_match.groups()
                return datetime(int(year), int(month), int(day))
            
            return None
            
        except Exception as e:
            logger.error(f"Error parsing date '{date_text}': {str(e)}")
            return None
    
    def get_meeting_details(self, meeting_id: str) -> Dict:
        """Get detailed information for a specific meeting"""
        try:
            # In a real implementation, you would fetch the actual meeting details
            # For now, return mock data based on the meeting_id
            return {
                'id': meeting_id,
                'council': 'williamsburg',
                'title': 'City Council Regular Meeting',
                'date': '2025-07-01',
                'time': '19:00',
                'location': 'City Hall Council Chambers',
                'agenda_items': [
                    'Call to Order',
                    'Public Comment Period',
                    'Approval of Minutes',
                    'Budget Discussion',
                    'Zoning Applications',
                    'New Business',
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
                'id': 'wb_001',
                'council': 'williamsburg',
                'council_name': 'Williamsburg City Council',
                'type': 'Regular Meeting',
                'title': 'City Council Regular Meeting',
                'date': (today - timedelta(days=7)).strftime('%Y-%m-%d'),
                'time': '19:00',
                'agenda_url': '#',
                'minutes_url': '#',
                'status': 'completed'
            },
            {
                'id': 'wb_002',
                'council': 'williamsburg',
                'council_name': 'Williamsburg City Council',
                'type': 'Work Session',
                'title': 'Budget Work Session',
                'date': (today - timedelta(days=14)).strftime('%Y-%m-%d'),
                'time': '18:00',
                'agenda_url': '#',
                'minutes_url': None,
                'status': 'upcoming'
            }
        ]
