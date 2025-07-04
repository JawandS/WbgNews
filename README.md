# Williamsburg News - Local Government Meeting Tracker

A Flask web application that aggregates and displays meeting agendas and minutes from local government councils in the Williamsburg, Virginia area.

## Features

- **Dual Source Monitoring**: Tracks meetings from both Williamsburg City Council and James City County Board of Supervisors
- **Modern UI**: Clean, responsive interface built with Bootstrap 5
- **Real-time Data**: Web scraping services automatically fetch the latest meeting information
- **Meeting Details**: View detailed agenda items, documents, and meeting information
- **Mobile Friendly**: Fully responsive design works on all devices
- **API Endpoints**: RESTful API for accessing meeting data programmatically

## Monitored Sources

- **Williamsburg City Council**: https://williamsburg.civicweb.net/Portal/MeetingTypeList.aspx
- **James City County Board of Supervisors**: https://www.jamescitycountyva.gov/129/Agendas-Minutes

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Web Scraping**: BeautifulSoup4, Requests
- **Testing**: unittest
- **Icons**: Font Awesome

## Project Structure

```
WbgNews/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── services/                   # Web scraping services
│   ├── __init__.py
│   ├── williamsburg_scraper.py # Williamsburg City Council scraper
│   └── james_city_scraper.py   # James City County scraper
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── index.html             # Homepage
│   ├── williamsburg.html      # Williamsburg council page
│   ├── james_city.html        # James City county page
│   ├── meeting_detail.html    # Meeting details page
│   ├── 404.html               # 404 error page
│   └── 500.html               # 500 error page
├── static/                    # Static assets
│   ├── css/
│   │   └── style.css          # Custom styles
│   └── js/
│       └── main.js            # JavaScript functionality
└── tests/                     # Test suite
    ├── __init__.py            # Test utilities
    └── test_app.py            # Main test file
```

## Installation

1. **Clone or download the project files**

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Development Mode

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Production Mode

For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## API Endpoints

### Get All Meetings
```
GET /api/meetings
```

Returns a JSON response with recent meetings from both councils.

**Response:**
```json
{
  "success": true,
  "meetings": [
    {
      "id": "wb_001",
      "council": "williamsburg",
      "council_name": "Williamsburg City Council",
      "type": "Regular Meeting",
      "title": "City Council Regular Meeting",
      "date": "2025-07-01",
      "time": "19:00",
      "agenda_url": "https://...",
      "minutes_url": "https://...",
      "status": "completed"
    }
  ],
  "total": 1
}
```

### Get Meeting Details
```
GET /api/meeting/<council>/<meeting_id>
```

Returns detailed information about a specific meeting.

**Parameters:**
- `council`: Either "williamsburg" or "james_city"
- `meeting_id`: The unique meeting identifier

## Testing

Run the test suite:

```bash
python -m unittest tests.test_app -v
```

Or run tests from the tests directory:

```bash
cd tests
python test_app.py
```

The test suite includes:
- Flask route testing
- Web scraper functionality testing
- API endpoint testing
- Integration testing
- Data structure validation

## Configuration

### Environment Variables

You can set the following environment variables:

- `FLASK_ENV`: Set to "development" for debug mode
- `SECRET_KEY`: Secret key for Flask sessions (change in production)
- `PORT`: Port to run the application on (default: 5000)

### Scraper Configuration

The scrapers include robust error handling and will fall back to mock data if the government websites are unavailable. This ensures the application continues to work even if there are temporary issues with the source websites.

## Features in Detail

### Web Scraping
- Handles various date formats from government websites
- Robust error handling with fallback to mock data
- Respects website rate limits
- Parses complex HTML structures from different CMS systems

### User Interface
- Clean, modern design with intuitive navigation
- Color-coded councils (blue for Williamsburg, green for James City)
- Responsive design for mobile and desktop
- Loading states and error handling
- Smooth animations and transitions

### Data Management
- Combines data from multiple sources
- Sorts meetings chronologically
- Filters by date ranges
- Structured API responses

## Deployment

### Local Development
The application is configured to run in debug mode by default for development.

### Production Deployment
For production:
1. Set `FLASK_ENV=production`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Set up a reverse proxy (Nginx, Apache)
4. Configure proper logging
5. Set up SSL/TLS certificates

### Docker Deployment
Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is open source and available under the MIT License.

## Troubleshooting

### Common Issues

**"Import could not be resolved" errors:**
- Make sure you've installed the requirements: `pip install -r requirements.txt`
- Activate your virtual environment if using one

**Web scraping returns empty results:**
- Government websites may have changed their structure
- Check if the websites are accessible
- The app will fall back to mock data in case of errors

**Port already in use:**
- Change the port in `app.py` or set the `PORT` environment variable
- Kill any existing processes using the port

### Logs

The application logs important events and errors. Check the console output for debugging information.

## Future Enhancements

- Database storage for historical meeting data
- Email notifications for new meetings
- Calendar integration (iCal export)
- Search functionality across meeting content
- RSS feed for updates
- Admin panel for configuration
- Caching layer for improved performance

## Contact

For questions or support, please open an issue in the project repository.
