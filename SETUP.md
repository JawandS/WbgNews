# Williamsburg Local News - Meeting Agenda Scraper

An enhanced Flask web application that scrapes meeting agendas from local government sources, generates AI-powered summaries, and presents them in an easy-to-read format for the Williamsburg community.

## Features

- **Automated Web Scraping**: Collects meeting agendas from:
  - Williamsburg City Council (https://williamsburg.civicweb.net/Portal/MeetingTypeList.aspx)
  - James City County Council (https://www.jamescitycountyva.gov/129/Agendas-Minutes)

- **AI-Powered Summaries**: Uses OpenAI's GPT API to generate:
  - Comprehensive meeting summaries
  - Key highlights and important points
  - Community-focused insights

- **Database Storage**: SQLite/PostgreSQL database with:
  - Meeting metadata (date, title, source, URL)
  - Full agenda content
  - AI-generated summaries and highlights
  - Scraping logs and statistics

- **Web Interface**: Clean, responsive interface featuring:
  - Meeting listings with filters
  - Detailed meeting views
  - AI summary display
  - Links to original documents
  - Admin dashboard

- **Background Processing**: Celery-powered background tasks for:
  - Scheduled scraping
  - AI summary generation
  - Error handling and logging

## Installation

### Prerequisites

- Python 3.8+
- Redis (for background tasks)
- OpenAI API key

### Setup

1. **Clone and navigate to the project:**
   ```bash
   cd /home/js/dev/WbgNews
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration:**
   Copy `.env.example` to `.env` and update the values:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your configuration:
   ```env
   FLASK_DEBUG=False
   FLASK_SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///williamsburg_news.db
   OPENAI_API_KEY=your-openai-api-key-here
   REDIS_URL=redis://localhost:6379/0
   ```

5. **Initialize Database:**
   ```bash
   python manage.py init-db
   ```

6. **Test AI Service (optional):**
   ```bash
   python manage.py test-ai
   ```

## Usage

### Running the Application

1. **Start Redis (required for background tasks):**
   ```bash
   redis-server
   ```

2. **Start the Flask application:**
   ```bash
   # Using the VS Code task
   # Or manually:
   python app.py
   ```

3. **Start Celery worker (for background tasks):**
   ```bash
   celery -A tasks.celery worker --loglevel=info
   ```

### Manual Operations

**Manual Scraping:**
```bash
python manage.py scrape
```

**Generate AI Summaries:**
```bash
python manage.py generate-summaries
```

**View Statistics:**
```bash
python manage.py stats
```

### Web Interface

- **Homepage**: http://localhost:5000 - Meeting highlights and news
- **Meetings**: http://localhost:5000/meetings - Full meeting listings
- **Admin**: http://localhost:5000/admin - Administrative dashboard
- **API Health**: http://localhost:5000/api/health - System status

## API Endpoints

### Public APIs

- `GET /api/health` - Health check
- `GET /api/meetings` - Meeting listings (paginated)
- `GET /api/meeting/<id>` - Individual meeting details
- `GET /api/news` - Local news (legacy)
- `GET /api/events` - Community events (legacy)

### Admin APIs

- `GET /admin/scrape` - Trigger manual scraping

## Architecture

### Core Components

1. **Flask Application** (`app.py`)
   - Main web application
   - Route handlers
   - Database integration

2. **Database Models** (`models.py`)
   - `MeetingAgenda`: Meeting data and AI summaries
   - `ScrapingLog`: Scraping operation tracking

3. **Web Scrapers** (`scrapers.py`)
   - `WilliamsburgScraper`: City council scraper
   - `JamesCityScraper`: County council scraper
   - Robust error handling and rate limiting

4. **AI Service** (`ai_service.py`)
   - OpenAI GPT integration
   - Summary and highlight generation
   - Error handling and fallbacks

5. **Background Tasks** (`tasks.py`)
   - Celery task definitions
   - Automated scraping and processing
   - Error logging

### Data Flow

1. **Scraping**: Background tasks collect meeting agendas
2. **Storage**: Raw data stored in database
3. **AI Processing**: GPT generates summaries and highlights
4. **Presentation**: Web interface displays processed data
5. **Linking**: Each summary links to original source

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_DEBUG` | Enable debug mode | `False` |
| `FLASK_SECRET_KEY` | Flask secret key | Required |
| `DATABASE_URL` | Database connection string | `sqlite:///williamsburg_news.db` |
| `OPENAI_API_KEY` | OpenAI API key | Required for AI features |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |

### Scraping Configuration

- **Rate Limiting**: 1-second delays between requests
- **Content Limits**: 5000 characters max per agenda
- **Error Handling**: Comprehensive logging and continuation
- **Duplicate Prevention**: URL-based deduplication

### AI Configuration

- **Model**: GPT-3.5-turbo (configurable)
- **Summary Length**: ~800 tokens
- **Highlights**: 3-5 key points per meeting
- **Fallback**: Graceful degradation on API errors

## Error Handling

### Scraping Errors
- Network timeouts: Retry with exponential backoff
- Parsing failures: Log and continue with next item
- Rate limiting: Respect site policies

### AI Service Errors
- API failures: Store without summary, retry later
- Content too long: Truncate and process
- Invalid responses: Create fallback highlights

### Database Errors
- Connection issues: Retry operations
- Constraint violations: Skip duplicates
- Transaction failures: Rollback and log

## Security Considerations

- **Rate Limiting**: Respectful scraping practices
- **Data Validation**: Input sanitization and validation
- **Error Logging**: No sensitive data in logs
- **API Keys**: Environment variable storage only
- **CORS**: Configured for secure cross-origin requests

## Performance Optimization

- **Database Indexing**: Key fields indexed for fast queries
- **Pagination**: Large datasets paginated
- **Background Processing**: Non-blocking operations
- **Caching**: Static content served efficiently
- **Connection Pooling**: Database connection optimization

## Maintenance

### Regular Tasks

1. **Monitor Scraping Logs**: Check `/admin` dashboard
2. **Database Cleanup**: Archive old meetings periodically
3. **API Key Rotation**: Update OpenAI keys as needed
4. **Dependency Updates**: Keep packages current

### Troubleshooting

**Common Issues:**

1. **Scraping Fails**: Check source website changes
2. **AI Summaries Missing**: Verify OpenAI API key and credits
3. **Background Tasks Not Running**: Ensure Redis and Celery are active
4. **Database Errors**: Check disk space and permissions

### Monitoring

- Health check endpoint: `/api/health`
- Admin dashboard: `/admin`
- Application logs: Check console output
- Database stats: `python manage.py stats`

## Development

### Code Structure

```
/home/js/dev/WbgNews/
├── app.py              # Main Flask application
├── models.py           # Database models
├── scrapers.py         # Web scraping utilities
├── ai_service.py       # OpenAI integration
├── tasks.py            # Background tasks
├── manage.py           # CLI management tool
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── templates/          # HTML templates
├── static/             # CSS, JS, images
└── README.md           # This file
```

### Adding New Sources

1. Create new scraper class in `scrapers.py`
2. Implement required methods
3. Add to `scrape_all_sources()` function
4. Update database models if needed
5. Test thoroughly

### Extending AI Features

1. Modify prompts in `ai_service.py`
2. Add new summary types
3. Implement custom processing logic
4. Update templates for display

## Deployment

### Production Considerations

1. **Database**: Use PostgreSQL for production
2. **Redis**: Configure persistence and clustering
3. **Web Server**: Use Gunicorn with nginx
4. **Environment**: Set production environment variables
5. **Monitoring**: Implement comprehensive logging
6. **Backups**: Regular database backups
7. **SSL**: HTTPS configuration

### Example Production Command

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## License

This project is designed for the Williamsburg community and follows local government data access policies.

## Support

For issues or questions, check the admin dashboard at `/admin` or review application logs for detailed error information.
