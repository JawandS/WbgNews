"""
Williamsburg News Flask Application
Main application file for displaying meeting agendas and notes
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import logging
from services.williamsburg_scraper import WilliamsburgScraper
from services.james_city_scraper import JamesCityScraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize scrapers
williamsburg_scraper = WilliamsburgScraper()
james_city_scraper = JamesCityScraper()

@app.route('/')
def index():
    """Main page displaying recent meetings from both councils"""
    return render_template('index.html')

@app.route('/api/meetings')
def get_meetings():
    """API endpoint to fetch meetings data"""
    try:
        # Get recent meetings from both sources
        williamsburg_meetings = williamsburg_scraper.get_recent_meetings()
        james_city_meetings = james_city_scraper.get_recent_meetings()
        
        # Combine and sort by date
        all_meetings = williamsburg_meetings + james_city_meetings
        all_meetings.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        return jsonify({
            'success': True,
            'meetings': all_meetings,
            'total': len(all_meetings)
        })
    except Exception as e:
        logger.error(f"Error fetching meetings: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch meetings data'
        }), 500

@app.route('/api/meeting/<council>/<meeting_id>')
def get_meeting_details(council, meeting_id):
    """API endpoint to fetch detailed meeting information"""
    try:
        if council == 'williamsburg':
            meeting_details = williamsburg_scraper.get_meeting_details(meeting_id)
        elif council == 'james_city':
            meeting_details = james_city_scraper.get_meeting_details(meeting_id)
        else:
            return jsonify({'success': False, 'error': 'Invalid council'}), 400
        
        return jsonify({
            'success': True,
            'meeting': meeting_details
        })
    except Exception as e:
        logger.error(f"Error fetching meeting details: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch meeting details'
        }), 500

@app.route('/williamsburg')
def williamsburg_council():
    """Page for Williamsburg City Council meetings"""
    return render_template('williamsburg.html')

@app.route('/james-city')
def james_city_council():
    """Page for James City County Council meetings"""
    return render_template('james_city.html')

@app.route('/meeting/<council>/<meeting_id>')
def meeting_detail(council, meeting_id):
    """Detailed view of a specific meeting"""
    return render_template('meeting_detail.html', council=council, meeting_id=meeting_id)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
