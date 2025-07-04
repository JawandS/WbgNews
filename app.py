"""
Williamsburg Local News Application
Local news and events for the Williamsburg community
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
import os
from datetime import datetime

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Enable CORS for all routes
    CORS(app)
    
    # Routes
    @app.route('/')
    def index():
        """Homepage"""
        return render_template('index.html', 
                             title='Williamsburg Local News - Your Community Source',
                             current_year=datetime.now().year)
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint for monitoring"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'Williamsburg Local News'
        })
    
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
