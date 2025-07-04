"""
WbgNews Flask Application
Main application file
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
                             title='WbgNews - Your News Source',
                             current_year=datetime.now().year)
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint for monitoring"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'WbgNews'
        })
    
    @app.route('/about')
    def about():
        """About page"""
        return render_template('about.html', 
                             title='About - WbgNews')
    
    @app.route('/news')
    def news():
        """News listing page"""
        # Placeholder news data
        sample_news = [
            {
                'id': 1,
                'title': 'Breaking: Sample News Article',
                'summary': 'This is a placeholder for a news article summary...',
                'date': '2025-07-04',
                'author': 'News Team'
            },
            {
                'id': 2,
                'title': 'Technology Update: AI Advances',
                'summary': 'Latest developments in artificial intelligence...',
                'date': '2025-07-03',
                'author': 'Tech Reporter'
            },
            {
                'id': 3,
                'title': 'Sports Highlights of the Week',
                'summary': 'Recap of this week\'s most exciting sports moments...',
                'date': '2025-07-02',
                'author': 'Sports Desk'
            }
        ]
        return render_template('news.html', 
                             title='Latest News - WbgNews',
                             news_articles=sample_news)
    
    @app.route('/api/news')
    def api_news():
        """API endpoint for news data"""
        sample_news = [
            {
                'id': 1,
                'title': 'Breaking: Sample News Article',
                'summary': 'This is a placeholder for a news article summary...',
                'date': '2025-07-04',
                'author': 'News Team'
            },
            {
                'id': 2,
                'title': 'Technology Update: AI Advances',
                'summary': 'Latest developments in artificial intelligence...',
                'date': '2025-07-03',
                'author': 'Tech Reporter'
            }
        ]
        return jsonify({'news': sample_news})
    
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
