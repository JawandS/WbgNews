"""
Database models for Williamsburg News Application
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from typing import Optional

db = SQLAlchemy()

class MeetingAgenda(db.Model):
    """Model for storing meeting agendas and minutes"""
    __tablename__ = 'meeting_agendas'
    
    id = db.Column(db.Integer, primary_key=True)
    meeting_date = db.Column(db.Date, nullable=False, index=True)
    meeting_title = db.Column(db.String(500), nullable=False)
    original_url = db.Column(db.String(1000), nullable=False, unique=True)
    agenda_content = db.Column(db.Text)
    source = db.Column(db.String(100), nullable=False)  # 'williamsburg' or 'jamescity'
    
    # AI-generated content
    ai_summary = db.Column(db.Text)
    ai_highlights = db.Column(db.Text)  # JSON string of highlights
    summary_generated_at = db.Column(db.DateTime)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_processed = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<MeetingAgenda {self.meeting_title} - {self.meeting_date}>'
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'meeting_date': self.meeting_date.isoformat() if self.meeting_date else None,
            'meeting_title': self.meeting_title,
            'original_url': self.original_url,
            'agenda_content': self.agenda_content,
            'source': self.source,
            'ai_summary': self.ai_summary,
            'ai_highlights': self.ai_highlights,
            'summary_generated_at': self.summary_generated_at.isoformat() if self.summary_generated_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_processed': self.is_processed
        }

class ScrapingLog(db.Model):
    """Model for tracking scraping operations"""
    __tablename__ = 'scraping_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # 'success', 'error', 'partial'
    items_scraped = db.Column(db.Integer, default=0)
    error_message = db.Column(db.Text)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<ScrapingLog {self.source} - {self.status}>'
