# WbgNews - Flask News Application

A modern, responsive Flask web application for news publishing, designed for deployment on Render.

## 🚀 Features

- **Modern UI**: Clean, responsive design using Bootstrap 5
- **Mobile-First**: Optimized for all device sizes
- **API Endpoints**: RESTful API for news data
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
├── README.md             # This file
├── DEPLOYMENT.md         # Deployment guide
├── .gitignore           # Git ignore file
├── templates/            # Jinja2 templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── news.html         # News listing
│   ├── about.html        # About page
│   ├── 404.html          # 404 error page
│   └── 500.html          # 500 error page
└── static/               # Static assets
    ├── css/
    │   └── style.css     # Custom styles
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

- `GET /` - Homepage
- `GET /news` - News listing page
- `GET /about` - About page
- `GET /api/health` - Health check endpoint
- `GET /api/news` - JSON API for news data

## 🚀 Deployment on Render

### Method 1: Infrastructure as Code (Recommended)

This project includes a `render.yaml` file for easy deployment:

1. **Fork or push this code to your GitHub repository**

2. **Connect to Render**:
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file

3. **Deploy**: Render will automatically build and deploy your application based on the configuration in `render.yaml`

### Method 2: Manual Web Service Creation

1. **Fork or push this code to your GitHub repository**

2. **Create a new Web Service on Render**:
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure the service**:
   ```
   Name: wbgnews (or your preferred name)
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
   ```

4. **Set environment variables**:
   ```
   FLASK_DEBUG=False
   ```

5. **Deploy**: Click "Create Web Service"

### Method 3: Using Render CLI

1. **Install Render CLI** (if preferred):
   ```bash
   npm install -g @render-tools/cli
   ```

2. **Deploy using CLI**:
   ```bash
   render deploy
   ```

## 🔒 Environment Variables

Environment variables are automatically configured through the `render.yaml` file:

- `FLASK_DEBUG`: Set to `False` in production
- `PORT`: Automatically set by Render
- `PYTHON_VERSION`: Specified as `3.9.16`

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
- Secure secret key handling
- Input validation ready

## 📊 Monitoring

- Built-in health check endpoint: `/api/health`
- Error logging ready
- Performance monitoring ready

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

## 🐛 Troubleshooting

### Common Issues

1. **Port binding error**: Ensure the PORT environment variable is properly set
2. **Static files not loading**: Check static file paths and CORS settings
3. **Template not found**: Verify template paths and ensure templates directory exists

### Logs

Check Render logs for detailed error information:
- Go to your service dashboard
- Click on "Logs" tab
- Monitor real-time logs during deployment

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
- Contact: info@wbgnews.com

## 🚀 Next Steps

After deployment, consider adding:
- Database integration (PostgreSQL on Render)
- User authentication system
- Admin panel for content management
- Real news API integration
- Comment system
- Newsletter functionality
- Social media integration
- Analytics and monitoring

---

**Happy Coding!** 🎉
