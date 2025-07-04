"""
Background tasks for scraping and processing meeting agendas
"""

from celery import Celery
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def make_celery(app):
    """Create Celery instance with Flask app context"""
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context."""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# Standalone Celery app for when running worker
celery = Celery('williamsburg_news')
celery.conf.update(
    broker_url=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    result_backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery.task(bind=True)
def scrape_and_process_agendas(self):
    """
    Background task to scrape meeting agendas and generate AI summaries
    """
    from scrapers import scrape_all_sources
    from ai_service import AIService
    from models import db, MeetingAgenda, ScrapingLog
    
    try:
        # Log start of scraping
        log = ScrapingLog(
            source='all',
            status='running',
            started_at=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()
        
        # Scrape all sources
        results = scrape_all_sources()
        total_scraped = 0
        
        # Initialize AI service
        ai_service = AIService()
        
        for source, agendas in results.items():
            for agenda_data in agendas:
                try:
                    # Check if this agenda already exists
                    existing = MeetingAgenda.query.filter_by(
                        original_url=agenda_data['original_url']
                    ).first()
                    
                    if existing:
                        logger.info(f"Agenda already exists: {agenda_data['meeting_title']}")
                        continue
                    
                    # Create new agenda record
                    agenda = MeetingAgenda(
                        meeting_date=agenda_data['meeting_date'],
                        meeting_title=agenda_data['meeting_title'],
                        original_url=agenda_data['original_url'],
                        agenda_content=agenda_data['agenda_content'],
                        source=agenda_data['source']
                    )
                    
                    # Generate AI summary if content is available
                    if agenda_data['agenda_content'] and len(agenda_data['agenda_content'].strip()) > 50:
                        try:
                            ai_result = ai_service.generate_summary(
                                agenda_data['agenda_content'],
                                agenda_data['meeting_title'],
                                str(agenda_data['meeting_date'])
                            )
                            
                            agenda.ai_summary = ai_result['summary']
                            agenda.ai_highlights = ai_result['highlights']
                            agenda.summary_generated_at = datetime.utcnow()
                            agenda.is_processed = True
                            
                        except Exception as e:
                            logger.error(f"Error generating AI summary for {agenda_data['meeting_title']}: {e}")
                            agenda.is_processed = False
                    
                    db.session.add(agenda)
                    total_scraped += 1
                    
                except Exception as e:
                    logger.error(f"Error processing agenda {agenda_data.get('meeting_title', 'Unknown')}: {e}")
                    continue
        
        # Commit all changes
        db.session.commit()
        
        # Update log
        log.status = 'success'
        log.items_scraped = total_scraped
        log.completed_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Successfully scraped and processed {total_scraped} agendas")
        return f"Scraped {total_scraped} agendas"
        
    except Exception as e:
        logger.error(f"Error in scraping task: {e}")
        
        # Update log with error
        try:
            log.status = 'error'
            log.error_message = str(e)
            log.completed_at = datetime.utcnow()
            db.session.commit()
        except:
            pass
        
        raise

@celery.task(bind=True)
def generate_missing_summaries(self):
    """
    Background task to generate AI summaries for agendas that don't have them yet
    """
    from ai_service import AIService
    from models import db, MeetingAgenda
    
    try:
        # Find agendas without AI summaries
        unprocessed_agendas = MeetingAgenda.query.filter(
            MeetingAgenda.is_processed == False,
            MeetingAgenda.agenda_content.isnot(None)
        ).limit(10).all()  # Process 10 at a time
        
        if not unprocessed_agendas:
            return "No agendas need processing"
        
        ai_service = AIService()
        processed_count = 0
        
        for agenda in unprocessed_agendas:
            try:
                if len(agenda.agenda_content.strip()) < 50:
                    continue
                
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
                logger.error(f"Error generating summary for agenda {agenda.id}: {e}")
                continue
        
        db.session.commit()
        logger.info(f"Generated summaries for {processed_count} agendas")
        return f"Generated summaries for {processed_count} agendas"
        
    except Exception as e:
        logger.error(f"Error in summary generation task: {e}")
        raise
