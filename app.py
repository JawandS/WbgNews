"""
Williamsburg Local News Application
Local news and events for the Williamsburg community
Enhanced with meeting agenda scraping and AI summaries
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_cors import CORS
import os
import json
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Import our custom modules
from models import db, MeetingAgenda, ScrapingLog
from scrapers import scrape_all_sources
from ai_service import AIService
from tasks import make_celery, scrape_and_process_agendas, generate_missing_summaries

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///williamsburg_news.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Celery configuration
    app.config['CELERY_BROKER_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    app.config['CELERY_RESULT_BACKEND'] = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Initialize Celery
    celery = make_celery(app)
    
    # Add custom Jinja filters
    @app.template_filter('from_json')
    def from_json_filter(value):
        """Parse JSON string into Python object"""
        try:
            return json.loads(value) if value else []
        except (json.JSONDecodeError, TypeError):
            return []
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Routes
    @app.route('/')
    def index():
        """Homepage with recent meeting highlights"""
        try:
            # Get recent meetings with AI summaries
            recent_meetings = MeetingAgenda.query.filter(
                MeetingAgenda.is_processed == True,
                MeetingAgenda.ai_highlights.isnot(None)
            ).order_by(MeetingAgenda.meeting_date.desc()).limit(6).all()
            
            # Parse highlights for display
            meeting_highlights = []
            for meeting in recent_meetings:
                try:
                    highlights = json.loads(meeting.ai_highlights) if meeting.ai_highlights else []
                    meeting_highlights.append({
                        'meeting': meeting,
                        'highlights': highlights[:3]  # Show top 3 highlights
                    })
                except json.JSONDecodeError:
                    continue
            
            return render_template('index.html', 
                                 title='Williamsburg Local News - Your Community Source',
                                 current_year=datetime.now().year,
                                 meeting_highlights=meeting_highlights)
        except Exception as e:
            app.logger.error(f"Error loading homepage: {e}")
            return render_template('index.html', 
                                 title='Williamsburg Local News - Your Community Source',
                                 current_year=datetime.now().year,
                                 meeting_highlights=[])
    
    @app.route('/meetings')
    def meetings():
        """Meeting agendas and summaries page"""
        try:
            page = request.args.get('page', 1, type=int)
            source = request.args.get('source', '')
            
            # Build query
            query = MeetingAgenda.query
            
            if source:
                query = query.filter(MeetingAgenda.source == source)
            
            # Paginate results
            meetings = query.order_by(MeetingAgenda.meeting_date.desc()).paginate(
                page=page, per_page=10, error_out=False
            )
            
            return render_template('meetings.html',
                                 title='Meeting Agendas & Summaries',
                                 meetings=meetings,
                                 current_source=source)
        except Exception as e:
            app.logger.error(f"Error loading meetings page: {e}")
            return render_template('meetings.html',
                                 title='Meeting Agendas & Summaries',
                                 meetings=None,
                                 current_source='')
    
    @app.route('/meeting/<int:meeting_id>')
    def meeting_detail(meeting_id):
        """Detailed view of a specific meeting"""
        try:
            meeting = MeetingAgenda.query.get_or_404(meeting_id)
            
            # Parse highlights
            highlights = []
            if meeting.ai_highlights:
                try:
                    highlights = json.loads(meeting.ai_highlights)
                except json.JSONDecodeError:
                    pass
            
            return render_template('meeting_detail.html',
                                 title=f"{meeting.meeting_title} - Meeting Details",
                                 meeting=meeting,
                                 highlights=highlights)
        except Exception as e:
            app.logger.error(f"Error loading meeting detail: {e}")
    
    @app.route('/admin/scrape')
    def admin_scrape():
        """Admin endpoint to trigger manual scraping"""
        try:
            # Trigger background scraping task
            task = scrape_and_process_agendas.delay()
            flash(f'Scraping task started. Task ID: {task.id}', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            app.logger.error(f"Error starting scraping task: {e}")
            flash(f'Error starting scraping: {str(e)}', 'error')
            return redirect(url_for('admin_dashboard'))
    
    @app.route('/admin')
    def admin_dashboard():
        """Simple admin dashboard"""
        try:
            # Get recent scraping logs
            recent_logs = ScrapingLog.query.order_by(ScrapingLog.started_at.desc()).limit(10).all()
            
            # Get meeting statistics
            total_meetings = MeetingAgenda.query.count()
            processed_meetings = MeetingAgenda.query.filter(MeetingAgenda.is_processed == True).count()
            
            # Get meetings by source
            williamsburg_count = MeetingAgenda.query.filter(MeetingAgenda.source == 'williamsburg').count()
            jamescity_count = MeetingAgenda.query.filter(MeetingAgenda.source == 'jamescity').count()
            
            stats = {
                'total_meetings': total_meetings,
                'processed_meetings': processed_meetings,
                'williamsburg_count': williamsburg_count,
                'jamescity_count': jamescity_count
            }
            
            return render_template('admin.html',
                                 title='Admin Dashboard',
                                 stats=stats,
                                 recent_logs=recent_logs)
        except Exception as e:
            app.logger.error(f"Error loading admin dashboard: {e}")
            return render_template('admin.html',
                                 title='Admin Dashboard',
                                 stats={},
                                 recent_logs=[])
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint for monitoring"""
        try:
            # Test database connection
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            
            # Test AI service if API key is available
            ai_status = False
            if os.getenv('OPENAI_API_KEY'):
                try:
                    ai_service = AIService()
                    ai_status = ai_service.test_connection()
                except Exception as e:
                    logger.warning(f"AI service test failed: {e}")
                    ai_status = False
            
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'service': 'Williamsburg Local News',
                'database': 'connected',
                'ai_service': 'connected' if ai_status else 'unavailable'
            })
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'timestamp': datetime.now().isoformat(),
                'service': 'Williamsburg Local News',
                'error': str(e)
            }), 500
    
    @app.route('/about')
    def about():
        """About page"""
        return render_template('about.html', 
                             title='About - Williamsburg Local News')
    
    @app.route('/news')
    def news():
        """News listing page"""
        # Placeholder local news data
        local_news = [
            {
                'id': 1,
                'title': 'New Community Center Opens in Historic District',
                'summary': 'The Williamsburg Community Center officially opened its doors today, offering programs for residents of all ages...',
                'date': '2025-07-04',
                'author': 'Sarah Johnson',
                'category': 'Community',
                'location': 'Historic District'
            },
            {
                'id': 2,
                'title': 'Local Farmers Market Celebrates 10th Anniversary',
                'summary': 'The Williamsburg Farmers Market marks a decade of serving fresh, local produce to the community...',
                'date': '2025-07-03',
                'author': 'Mike Chen',
                'category': 'Events',
                'location': 'Market Square'
            },
            {
                'id': 3,
                'title': 'School Board Approves New Playground Equipment',
                'summary': 'Williamsburg Elementary will receive new playground equipment thanks to recent fundraising efforts...',
                'date': '2025-07-02',
                'author': 'Lisa Rodriguez',
                'category': 'Education',
                'location': 'Williamsburg Elementary'
            },
            {
                'id': 4,
                'title': 'Fourth of July Fireworks Display Set for Tonight',
                'summary': 'The annual Independence Day celebration will feature fireworks over Colonial Lake at 9 PM...',
                'date': '2025-07-04',
                'author': 'Tom Wilson',
                'category': 'Events',
                'location': 'Colonial Lake'
            }
        ]
        return render_template('news.html', 
                             title='Local News - Williamsburg',
                             news_articles=local_news)
    
    @app.route('/events')
    def events():
        """Community events page"""
        upcoming_events = [
            {
                'id': 1,
                'title': 'Summer Concert Series',
                'date': '2025-07-10',
                'time': '7:00 PM',
                'location': 'Colonial Park Amphitheater',
                'description': 'Join us for an evening of live music featuring local bands.',
                'category': 'Music'
            },
            {
                'id': 2,
                'title': 'Williamsburg Heritage Festival',
                'date': '2025-07-15',
                'time': '10:00 AM - 6:00 PM',
                'location': 'Historic District',
                'description': 'Celebrate our community\'s rich history with demonstrations, food, and activities.',
                'category': 'Festival'
            },
            {
                'id': 3,
                'title': 'Town Hall Meeting',
                'date': '2025-07-20',
                'time': '7:30 PM',
                'location': 'City Hall',
                'description': 'Monthly community meeting to discuss local issues and upcoming projects.',
                'category': 'Government'
            }
        ]
        return render_template('events.html', 
                             title='Community Events - Williamsburg',
                             events=upcoming_events)
    
    @app.route('/api/news')
    def api_news():
        """API endpoint for news data"""
        local_news = [
            {
                'id': 1,
                'title': 'New Community Center Opens in Historic District',
                'summary': 'The Williamsburg Community Center officially opened its doors today...',
                'date': '2025-07-04',
                'author': 'Sarah Johnson',
                'category': 'Community',
                'location': 'Historic District'
            },
            {
                'id': 2,
                'title': 'Local Farmers Market Celebrates 10th Anniversary',
                'summary': 'The Williamsburg Farmers Market marks a decade of serving fresh, local produce...',
                'date': '2025-07-03',
                'author': 'Mike Chen',
                'category': 'Events',
                'location': 'Market Square'
            }
        ]
        return jsonify({'news': local_news})
    
    @app.route('/api/events')
    def api_events():
        """API endpoint for events data"""
        upcoming_events = [
            {
                'id': 1,
                'title': 'Summer Concert Series',
                'date': '2025-07-10',
                'time': '7:00 PM',
                'location': 'Colonial Park Amphitheater',
                'category': 'Music'
            },
            {
                'id': 2,
                'title': 'Williamsburg Heritage Festival',
                'date': '2025-07-15',
                'time': '10:00 AM - 6:00 PM',
                'location': 'Historic District',
                'category': 'Festival'
            }
        ]
        return jsonify({'events': upcoming_events})
    
    @app.route('/api/meetings')
    def api_meetings():
        """API endpoint for meeting data"""
        try:
            page = request.args.get('page', 1, type=int)
            source = request.args.get('source', '')
            
            query = MeetingAgenda.query
            if source:
                query = query.filter(MeetingAgenda.source == source)
            
            meetings = query.order_by(MeetingAgenda.meeting_date.desc()).paginate(
                page=page, per_page=20, error_out=False
            )
            
            return jsonify({
                'meetings': [meeting.to_dict() for meeting in meetings.items],
                'total': meetings.total,
                'pages': meetings.pages,
                'current_page': page
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/meeting/<int:meeting_id>')
    def api_meeting_detail(meeting_id):
        """API endpoint for individual meeting data"""
        try:
            meeting = MeetingAgenda.query.get_or_404(meeting_id)
            return jsonify(meeting.to_dict())
        except Exception as e:
            return jsonify({'error': str(e)}), 404
    
    @app.errorhandler(404)
    def not_found(error):
        """Custom 404 page"""
        return render_template('404.html', title='Page Not Found'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Custom 500 page"""
        return render_template('500.html', title='Server Error'), 500
    
    return app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
