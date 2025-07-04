#!/usr/bin/env python3
"""
CLI management script for Williamsburg News Application
"""

import click
import os
import sys
from datetime import datetime

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, MeetingAgenda, ScrapingLog
from scrapers import scrape_all_sources
from ai_service import AIService

@click.group()
def cli():
    """Williamsburg News CLI Management Tool"""
    pass

@cli.command()
def init_db():
    """Initialize the database with tables"""
    app = create_app()
    with app.app_context():
        db.create_all()
        click.echo("Database initialized successfully!")

@cli.command()
def load_demo_data():
    """Load demo meeting data for testing"""
    app = create_app()
    with app.app_context():
        from demo_data import get_demo_meetings
        
        click.echo("Loading demo meeting data...")
        
        demo_meetings = get_demo_meetings()
        added_count = 0
        
        for meeting_data in demo_meetings:
            # Check if already exists
            existing = MeetingAgenda.query.filter_by(
                original_url=meeting_data['original_url']
            ).first()
            
            if existing:
                click.echo(f"  Skipping existing: {meeting_data['meeting_title']}")
                continue
            
            # Create new agenda
            agenda = MeetingAgenda(
                meeting_date=meeting_data['meeting_date'],
                meeting_title=meeting_data['meeting_title'],
                original_url=meeting_data['original_url'],
                agenda_content=meeting_data['agenda_content'],
                source=meeting_data['source']
            )
            
            db.session.add(agenda)
            added_count += 1
            click.echo(f"  Added: {meeting_data['meeting_title']}")
        
        db.session.commit()
        click.echo(f"Demo data loaded! Added {added_count} meetings.")

@cli.command()
def scrape():
    """Manually trigger scraping of all sources"""
    app = create_app()
    with app.app_context():
        click.echo("Starting manual scraping...")
        
        # Log the start
        log = ScrapingLog(
            source='manual',
            status='running',
            started_at=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()
        
        try:
            results = scrape_all_sources()
            total_scraped = 0
            
            for source, agendas in results.items():
                click.echo(f"Processing {len(agendas)} agendas from {source}...")
                
                for agenda_data in agendas:
                    # Check if already exists
                    existing = MeetingAgenda.query.filter_by(
                        original_url=agenda_data['original_url']
                    ).first()
                    
                    if existing:
                        click.echo(f"  Skipping existing: {agenda_data['meeting_title']}")
                        continue
                    
                    # Create new agenda
                    agenda = MeetingAgenda(
                        meeting_date=agenda_data['meeting_date'],
                        meeting_title=agenda_data['meeting_title'],
                        original_url=agenda_data['original_url'],
                        agenda_content=agenda_data['agenda_content'],
                        source=agenda_data['source']
                    )
                    
                    db.session.add(agenda)
                    total_scraped += 1
                    click.echo(f"  Added: {agenda_data['meeting_title']}")
            
            db.session.commit()
            
            # Update log
            log.status = 'success'
            log.items_scraped = total_scraped
            log.completed_at = datetime.utcnow()
            db.session.commit()
            
            click.echo(f"Scraping completed! Added {total_scraped} new agendas.")
            
        except Exception as e:
            log.status = 'error'
            log.error_message = str(e)
            log.completed_at = datetime.utcnow()
            db.session.commit()
            click.echo(f"Error during scraping: {e}")

@cli.command()
def generate_summaries():
    """Generate AI summaries for agendas that don't have them"""
    app = create_app()
    with app.app_context():
        if not os.getenv('OPENAI_API_KEY'):
            click.echo("Error: OPENAI_API_KEY environment variable not set!")
            return
        
        click.echo("Generating AI summaries...")
        
        # Find unprocessed agendas
        unprocessed = MeetingAgenda.query.filter(
            MeetingAgenda.is_processed == False,
            MeetingAgenda.agenda_content.isnot(None)
        ).all()
        
        if not unprocessed:
            click.echo("No agendas need processing.")
            return
        
        ai_service = AIService()
        processed_count = 0
        
        for agenda in unprocessed:
            if len(agenda.agenda_content.strip()) < 50:
                continue
            
            try:
                click.echo(f"Processing: {agenda.meeting_title}")
                
                ai_result = ai_service.generate_summary(
                    agenda.agenda_content,
                    agenda.meeting_title,
                    str(agenda.meeting_date)
                )
                
                agenda.ai_summary = ai_result['summary']
                agenda.ai_highlights = ai_result['highlights']
                agenda.summary_generated_at = datetime.utcnow()
                agenda.is_processed = True
                
                processed_count += 1
                
            except Exception as e:
                click.echo(f"Error processing {agenda.meeting_title}: {e}")
                continue
        
        db.session.commit()
        click.echo(f"Generated summaries for {processed_count} agendas.")

@cli.command()
def stats():
    """Show database statistics"""
    app = create_app()
    with app.app_context():
        total_meetings = MeetingAgenda.query.count()
        processed_meetings = MeetingAgenda.query.filter(MeetingAgenda.is_processed == True).count()
        williamsburg_count = MeetingAgenda.query.filter(MeetingAgenda.source == 'williamsburg').count()
        jamescity_count = MeetingAgenda.query.filter(MeetingAgenda.source == 'jamescity').count()
        
        click.echo(f"Database Statistics:")
        click.echo(f"  Total Meetings: {total_meetings}")
        click.echo(f"  Processed: {processed_meetings}")
        click.echo(f"  Williamsburg: {williamsburg_count}")
        click.echo(f"  James City: {jamescity_count}")

@cli.command()
def test_ai():
    """Test the AI service connection"""
    if not os.getenv('OPENAI_API_KEY'):
        click.echo("Error: OPENAI_API_KEY environment variable not set!")
        return
    
    try:
        ai_service = AIService()
        if ai_service.test_connection():
            click.echo("AI service connection successful!")
        else:
            click.echo("AI service connection failed!")
    except Exception as e:
        click.echo(f"Error testing AI service: {e}")

if __name__ == '__main__':
    cli()
