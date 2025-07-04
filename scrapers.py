"""
Web scraping utilities for meeting agendas
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import logging
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseScraper:
    """Base class for meeting agenda scrapers"""
    
    def __init__(self, source_name: str, base_url: str):
        self.source_name = source_name
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_page(self, url: str, timeout: int = 30) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page"""
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def scrape_agendas(self) -> List[Dict]:
        """Override this method in subclasses"""
        raise NotImplementedError

class WilliamsburgScraper(BaseScraper):
    """Scraper for Williamsburg City Council meetings"""
    
    def __init__(self):
        super().__init__('williamsburg', 'https://williamsburg.civicweb.net')
    
    def scrape_agendas(self) -> List[Dict]:
        """Scrape meeting agendas from Williamsburg City Council"""
        agendas = []
        
        try:
            # Get the main meeting types page
            soup = self.get_page(f"{self.base_url}/Portal/MeetingTypeList.aspx")
            if not soup:
                return agendas
            
            # Find meeting type links
            meeting_links = soup.find_all('a', href=re.compile(r'MeetingSchedule\.aspx'))
            
            for link in meeting_links[:3]:  # Limit to first 3 meeting types
                meeting_type_url = urljoin(self.base_url, link.get('href'))
                agendas.extend(self._scrape_meeting_type(meeting_type_url))
                time.sleep(1)  # Be respectful with requests
                
        except Exception as e:
            logger.error(f"Error scraping Williamsburg agendas: {e}")
        
        return agendas
    
    def _scrape_meeting_type(self, url: str) -> List[Dict]:
        """Scrape meetings for a specific meeting type"""
        meetings = []
        
        soup = self.get_page(url)
        if not soup:
            return meetings
        
        # Look for meeting rows in tables
        meeting_rows = soup.find_all('tr', class_=re.compile(r'(odd|even)'))
        
        for row in meeting_rows[:10]:  # Limit recent meetings
            try:
                # Extract meeting information
                cells = row.find_all('td')
                if len(cells) >= 2:
                    date_cell = cells[0]
                    title_cell = cells[1]
                    
                    # Extract date
                    date_text = date_cell.get_text(strip=True)
                    meeting_date = self._parse_date(date_text)
                    
                    # Extract title and link
                    link = title_cell.find('a')
                    if link:
                        title = link.get_text(strip=True)
                        agenda_url = urljoin(self.base_url, link.get('href'))
                        
                        # Get agenda content
                        content = self._get_agenda_content(agenda_url)
                        
                        meetings.append({
                            'meeting_date': meeting_date,
                            'meeting_title': title,
                            'original_url': agenda_url,
                            'agenda_content': content,
                            'source': self.source_name
                        })
                        
            except Exception as e:
                logger.error(f"Error processing meeting row: {e}")
                continue
        
        return meetings
    
    def _get_agenda_content(self, url: str) -> str:
        """Extract agenda content from meeting page"""
        soup = self.get_page(url)
        if not soup:
            return ""
        
        # Look for content in common containers
        content_selectors = [
            '.meeting-content',
            '.agenda-content',
            '.meeting-details',
            '#content',
            '.main-content'
        ]
        
        for selector in content_selectors:
            content_div = soup.select_one(selector)
            if content_div:
                return content_div.get_text(separator='\n', strip=True)
        
        # Fallback: get all text from body
        body = soup.find('body')
        if body:
            return body.get_text(separator='\n', strip=True)[:5000]  # Limit length
        
        return ""
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string into datetime object"""
        if not date_str:
            return None
            
        # Clean the date string
        date_str = date_str.strip()
        
        date_formats = [
            '%m/%d/%Y',
            '%m-%d-%Y',
            '%B %d, %Y',
            '%b %d, %Y',
            '%Y-%m-%d',
            '%d/%m/%Y'
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        
        # Try to extract just year if nothing else works
        try:
            import re
            year_match = re.search(r'20\d{2}', date_str)
            if year_match:
                year = int(year_match.group())
                return datetime(year, 1, 1).date()
        except:
            pass
        
        logger.warning(f"Could not parse date: {date_str}")
        return None

class JamesCityScraper(BaseScraper):
    """Scraper for James City County Council meetings"""
    
    def __init__(self):
        super().__init__('jamescity', 'https://www.jamescitycountyva.gov')
    
    def scrape_agendas(self) -> List[Dict]:
        """Scrape meeting agendas from James City County"""
        agendas = []
        
        try:
            # Get the agendas and minutes page
            soup = self.get_page(f"{self.base_url}/129/Agendas-Minutes")
            if not soup:
                return agendas
            
            # Look for document links
            doc_links = soup.find_all('a', href=re.compile(r'\.(pdf|doc|docx)$', re.I))
            
            for link in doc_links[:20]:  # Limit to recent documents
                try:
                    href = link.get('href')
                    if not href:
                        continue
                    
                    full_url = urljoin(self.base_url, href)
                    title = link.get_text(strip=True)
                    
                    # Extract date from title or link
                    meeting_date = self._extract_date_from_title(title)
                    
                    if meeting_date:
                        agendas.append({
                            'meeting_date': meeting_date,
                            'meeting_title': title,
                            'original_url': full_url,
                            'agenda_content': f"Document: {title}",  # PDF content extraction would need additional libraries
                            'source': self.source_name
                        })
                        
                except Exception as e:
                    logger.error(f"Error processing James City document: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping James City agendas: {e}")
        
        return agendas
    
    def _extract_date_from_title(self, title: str) -> Optional[datetime]:
        """Extract date from document title"""
        if not title:
            return None
            
        # Common date patterns in document titles
        date_patterns = [
            r'(\d{1,2}[-/]\d{1,2}[-/]\d{4})',
            r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})',
            r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}',
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}',
            r'(\d{4})'  # Just year as fallback
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                date_str = match.group(1)
                date_formats = [
                    '%m/%d/%Y', '%m-%d-%Y',
                    '%Y/%m/%d', '%Y-%m-%d',
                    '%B %d, %Y', '%B %d %Y',
                    '%b %d, %Y', '%b %d %Y',
                    '%Y'  # Just year
                ]
                
                for fmt in date_formats:
                    try:
                        if fmt == '%Y':
                            year = int(date_str)
                            return datetime(year, 1, 1).date()
                        return datetime.strptime(date_str, fmt).date()
                    except ValueError:
                        continue
        
        return None

def scrape_all_sources() -> Dict[str, List[Dict]]:
    """Scrape all configured sources"""
    scrapers = [
        WilliamsburgScraper(),
        JamesCityScraper()
    ]
    
    results = {}
    
    for scraper in scrapers:
        logger.info(f"Scraping {scraper.source_name}...")
        try:
            agendas = scraper.scrape_agendas()
            results[scraper.source_name] = agendas
            logger.info(f"Scraped {len(agendas)} agendas from {scraper.source_name}")
        except Exception as e:
            logger.error(f"Error scraping {scraper.source_name}: {e}")
            results[scraper.source_name] = []
    
    return results
