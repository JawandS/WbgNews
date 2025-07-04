"""
AI service for generating meeting agenda summaries using OpenAI GPT
"""

import openai
import json
import logging
from typing import Dict, List, Optional
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class AIService:
    """Service for generating AI-powered summaries of meeting agendas"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the AI service with OpenAI API key"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            try:
                self.client = openai.OpenAI(api_key=self.api_key)
                self.available = True
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")
                self.available = False
                self.client = None
        else:
            self.available = False
            self.client = None
            logger.info("No OpenAI API key provided - AI features will be disabled")
    
    def generate_summary(self, agenda_content: str, meeting_title: str, meeting_date: str) -> Dict[str, str]:
        """
        Generate a comprehensive summary and highlights for a meeting agenda
        
        Args:
            agenda_content: The full text content of the meeting agenda
            meeting_title: Title of the meeting
            meeting_date: Date of the meeting
            
        Returns:
            Dictionary containing 'summary' and 'highlights' keys
        """
        if not self.available:
            return self._generate_fallback_summary(agenda_content, meeting_title, meeting_date)
            
        if not agenda_content or len(agenda_content.strip()) < 50:
            return {
                'summary': "Insufficient content available for summary generation.",
                'highlights': json.dumps([])
            }
        
        try:
            # Generate detailed summary
            summary = self._generate_detailed_summary(agenda_content, meeting_title, meeting_date)
            
            # Generate key highlights
            highlights = self._generate_highlights(agenda_content, meeting_title, meeting_date)
            
            return {
                'summary': summary,
                'highlights': json.dumps(highlights)
            }
            
        except Exception as e:
            logger.error(f"Error generating AI summary: {e}")
            return self._generate_fallback_summary(agenda_content, meeting_title, meeting_date)
    
    def _generate_fallback_summary(self, agenda_content: str, meeting_title: str, meeting_date: str) -> Dict[str, str]:
        """Generate a basic summary without AI when API is not available"""
        if not agenda_content or len(agenda_content.strip()) < 50:
            return {
                'summary': "Meeting agenda content is not available or too brief for analysis.",
                'highlights': json.dumps([])
            }
        
        # Extract key information from agenda content
        lines = agenda_content.split('\n')
        agenda_items = []
        highlights = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for numbered items or clear agenda sections
            if (line.startswith(('A.', 'B.', 'C.', 'D.', 'E.')) or 
                line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')) or
                'Resolution' in line or 'Ordinance' in line or '$' in line):
                
                if len(line) < 200:  # Reasonable line length
                    agenda_items.append(line)
                    
                    # Create highlights for important items
                    if any(keyword in line.lower() for keyword in ['budget', 'fund', '$', 'ordinance', 'resolution', 'development', 'zoning']):
                        highlights.append({
                            'title': 'Important Agenda Item',
                            'description': line[:150] + ('...' if len(line) > 150 else '')
                        })
        
        # Create summary
        summary_parts = [
            f"Meeting: {meeting_title}",
            f"Date: {meeting_date}",
            "",
            "Key Agenda Items:"
        ]
        
        for item in agenda_items[:10]:  # Limit to first 10 items
            summary_parts.append(f"• {item}")
        
        if len(agenda_items) > 10:
            summary_parts.append(f"... and {len(agenda_items) - 10} additional items")
        
        # Add note about AI unavailability
        summary_parts.extend([
            "",
            "Note: This is a basic summary. AI-powered analysis is currently unavailable."
        ])
        
        return {
            'summary': '\n'.join(summary_parts),
            'highlights': json.dumps(highlights[:5])  # Limit to 5 highlights
        }
    
    def _generate_detailed_summary(self, content: str, title: str, date: str) -> str:
        """Generate a detailed summary of the meeting agenda"""
        prompt = f"""
        Please provide a comprehensive summary of this meeting agenda from {title} on {date}.
        
        Focus on:
        1. Key agenda items and their importance to the community
        2. Major decisions, votes, or proposals
        3. Public concerns or community issues discussed
        4. Budget items, development projects, or policy changes
        5. Any controversial or significant topics
        
        Write in a clear, journalistic style that would be helpful for residents who want to stay informed about local government activities.
        
        Meeting Content:
        {content[:4000]}  
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a skilled local news reporter who specializes in covering municipal government meetings. Provide clear, informative summaries that help residents understand what happened and why it matters."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating detailed summary: {e}")
            return f"Unable to generate summary due to API error: {str(e)}"
    
    def _generate_highlights(self, content: str, title: str, date: str) -> List[Dict[str, str]]:
        """Generate key highlights as a list of important points"""
        prompt = f"""
        Extract 3-5 key highlights from this meeting agenda from {title} on {date}.
        
        Return ONLY a JSON array of objects, each with "title" and "description" fields.
        Focus on the most newsworthy items that residents would want to know about.
        
        Example format:
        [
            {{"title": "New Park Development Approved", "description": "City council approved funding for a new community park in the downtown area."}},
            {{"title": "Budget Increase for Road Repairs", "description": "Additional $500,000 allocated for infrastructure improvements on Main Street."}}
        ]
        
        Meeting Content:
        {content[:3000]}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a local news editor extracting key highlights. Return only valid JSON format as requested."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.5
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Try to parse the JSON response
            try:
                highlights = json.loads(response_text)
                if isinstance(highlights, list):
                    return highlights[:5]  # Limit to 5 highlights
            except json.JSONDecodeError:
                logger.warning("AI response was not valid JSON, creating fallback highlights")
            
            # Fallback: create structured highlights from the response
            return self._create_fallback_highlights(response_text)
            
        except Exception as e:
            logger.error(f"Error generating highlights: {e}")
            return [{"title": "Summary Available", "description": "See full summary for meeting details."}]
    
    def _create_fallback_highlights(self, text: str) -> List[Dict[str, str]]:
        """Create highlights from unstructured AI response"""
        highlights = []
        
        # Split by common delimiters and create highlights
        lines = text.split('\n')
        for line in lines[:5]:
            line = line.strip()
            if line and len(line) > 10:
                # Remove bullet points, numbers, etc.
                clean_line = line.lstrip('•-*0123456789. ')
                if len(clean_line) > 20:
                    highlights.append({
                        "title": "Meeting Item",
                        "description": clean_line[:200]
                    })
        
        return highlights if highlights else [{"title": "Meeting Summary", "description": text[:200]}]
    
    def test_connection(self) -> bool:
        """Test the OpenAI API connection"""
        if not self.available or not self.client:
            return False
            
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello, this is a test."}],
                max_tokens=10
            )
            return True
        except Exception as e:
            logger.error(f"OpenAI API test failed: {e}")
            return False
