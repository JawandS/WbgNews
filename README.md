# Williamsburg Local News - Community News Application

A modern, responsive Flask web application focused on Williamsburg local news and community events, designed for deployment on Render.

## 🚀 Features

- **Modern UI**: Clean, responsive design using Bootstrap 5 with colonial-themed styling
- **Mobile-First**: Optimized for all device sizes
- **Local Focus**: Williamsburg community news, events, and announcements
- **Events Calendar**: Community events and local happenings
- **API Endpoints**: RESTful API for news and events data
- **Error Handling**: Custom 404 and 500 error pages
- **Health Monitoring**: Built-in health check endpoint
- **SEO Ready**: Proper meta tags and semantic HTML
- **Production Ready**: Configured for deployment on Render

## 🛠️ Technology Stack

- **Backend**: Flask 3.0.0
- **Frontend**: Bootstrap 5, Font Awesome, Custom CSS/JS
- **WSGI Server**: Gunicorn
- **Dependencies**: Flask-CORS for API access

## 📁 Project Structure

```
WbgNews/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version for Render
├── render.yaml           # Infrastructure as Code config
├── README.md             # This comprehensive guide
├── .gitignore           # Git ignore file
├── templates/            # Jinja2 templates
│   ├── base.html         # Base template with Williamsburg branding
│   ├── index.html        # Homepage with community focus
│   ├── news.html         # Local news and announcements
│   ├── events.html       # Community events page
│   ├── about.html        # About Williamsburg Local News
│   ├── 404.html          # 404 error page
│   └── 500.html          # 500 error page
└── static/               # Static assets
    ├── css/
    │   └── style.css     # Custom styles with colonial theme
    └── js/
        └── main.js       # Custom JavaScript
```

## 🔧 Local Development

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd WbgNews
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** (optional):
   ```bash
   export FLASK_DEBUG=True
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

## 🌐 API Endpoints

- `GET /` - Homepage with Williamsburg community focus
- `GET /news` - Local news and announcements page
- `GET /events` - Community events page
- `GET /about` - About Williamsburg Local News
- `GET /api/health` - Health check endpoint
- `GET /api/news` - JSON API for local news data
- `GET /api/events` - JSON API for community events data

## 🚀 Deployment on Render

### Method 1: Infrastructure as Code (Recommended)

This project includes a `render.yaml` file for easy Infrastructure as Code deployment:

#### Quick Start with render.yaml

1. **Fork this repository** to your GitHub account

2. **Connect to Render**:
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Select this repository

3. **Automatic Deployment**: Render automatically detects `render.yaml` and deploys your app

#### render.yaml Configuration Details

The `render.yaml` file configures:

- **Service Type**: Web service
- **Runtime**: Python 3
- **Build**: `pip install -r requirements.txt`
- **Start**: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
- **Health Check**: `/api/health` endpoint
- **Auto Deploy**: Enabled on push to main branch
- **Plan**: Free tier
- **Environment**: Production-ready settings

**Pre-configured Environment Variables:**
- `FLASK_DEBUG=False` (production mode)
- `PYTHON_VERSION=3.9.16` (specified runtime)

**Scaling Configuration:**
- **Min Instances**: 1
- **Max Instances**: 1 (Free tier)

### Method 2: Manual Web Service Creation

1. **Prepare Your Repository**:
   - Push this code to a GitHub repository
   - Make sure all files are committed and pushed

2. **Create a Web Service on Render**:
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub account if not already connected
   - Select your repository

3. **Configure Your Service**:
   ```
   Name: wbgnews (or your preferred name)
   Environment: Python 3
   Region: Choose your preferred region
   Branch: main (or your default branch)
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
   ```

4. **Set Environment Variables**:
   ```
   FLASK_DEBUG=False
   ```

5. **Deploy**: Click "Create Web Service"

### Method 3: Using Render CLI

1. **Install Render CLI**:
   ```bash
   npm install -g @render-tools/cli
   ```

2. **Deploy using CLI**:
   ```bash
   render deploy
   ```

## 📊 Health Monitoring & Management

### Health Check Endpoint

Your application includes a health check endpoint at `/api/health` that returns:
```json
{
  "status": "healthy",
  "timestamp": "2025-07-04T...",
  "service": "Williamsburg Local News"
}
```

Render automatically uses this endpoint to monitor your application's status.

### Post-Deployment Management

**Custom Domain (Optional):**
- Go to your service dashboard
- Navigate to "Settings" → "Custom Domains"
- Add your custom domain

**Monitoring:**
- Check the "Logs" tab for application logs
- Use the "Metrics" tab to monitor performance
- Set up alerts in the "Alerts" section

**SSL Certificate:**
Render automatically provides SSL certificates for all deployed applications.

### Updating Your Application

1. Push changes to your GitHub repository
2. Render will automatically redeploy your application
3. You can also manually trigger deploys from the Render dashboard

## 🔒 Environment Variables

Environment variables are automatically configured through the `render.yaml` file:

- `FLASK_DEBUG`: Set to `False` in production
- `PORT`: Automatically set by Render
- `PYTHON_VERSION`: Specified as `3.9.16`

## 🐛 Troubleshooting

### Common Issues

1. **Build Failed**: Check that all dependencies are in `requirements.txt`
2. **App Won't Start**: Verify the start command is correct
3. **500 Errors**: Check application logs in the Render dashboard
4. **Port binding error**: Ensure the PORT environment variable is properly set
5. **Static files not loading**: Check static file paths and CORS settings
6. **Template not found**: Verify template paths and ensure templates directory exists

### Checking Logs

**Via Render Dashboard:**
- Go to your service dashboard
- Click on "Logs" tab
- Monitor real-time logs during deployment

**Via Render CLI:**
```bash
# View recent logs
render logs --tail

# Follow logs in real-time
render logs --follow
```

## 📱 Responsive Design

The application is fully responsive and includes:
- Mobile-first CSS design
- Bootstrap 5 responsive grid
- Touch-friendly navigation
- Optimized images and fonts

## 🔍 SEO Features

- Semantic HTML structure
- Proper meta tags
- Open Graph tags ready
- Clean URL structure
- Sitemap ready

## 🛡️ Security Features

- CORS protection
- Environment-based configuration
- Input validation ready

## 🎨 Customization

### Adding New Pages

1. Create a new template in `templates/`
2. Add a route in `app.py`
3. Update navigation in `base.html`

### Styling

- Modify `static/css/style.css` for custom styles
- Update color scheme in CSS variables
- Add new components using Bootstrap classes

### Adding Real News Data

Replace the placeholder data in `app.py` with:
- Database integration (SQLAlchemy)
- External API calls (news APIs)
- Content management system

## ⚡ Performance Tips

1. **Use Redis**: Add Redis for caching (available as Render add-on)
2. **Database**: Add PostgreSQL for persistent data storage
3. **CDN**: Use a CDN for static assets
4. **Monitoring**: Set up application monitoring with services like Sentry

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact: info@williamsburgnews.com
- Check the [Render Documentation](https://render.com/docs)
- Join the [Render Community](https://community.render.com/)

## 🚀 Next Steps

After deployment, consider adding:
- Database integration (PostgreSQL on Render)
- User authentication system
- Admin panel for content management
- Real Williamsburg news API integration
- Community event submission system
- Local business directory
- Weather and traffic integration
- Newsletter functionality for residents
- Social media integration
- Analytics and monitoring

---

**Happy Coding!** 🎉
