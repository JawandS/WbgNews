# Deployment Guide for Render

This guide will help you deploy your WbgNews Flask application to Render.

## Quick Deploy Button

You can deploy this application to Render with one click:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## Manual Deployment Steps

### 1. Prepare Your Repository

1. Push this code to a GitHub repository
2. Make sure all files are committed and pushed

### 2. Create a Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub account if not already connected
4. Select your repository

### 3. Configure Your Service

Use these settings:

```
Name: wbgnews (or your preferred name)
Environment: Python 3
Region: Choose your preferred region
Branch: main (or your default branch)
Build Command: pip install -r requirements.txt
Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

### 4. Environment Variables

Set these environment variables in the Render dashboard:

```
SECRET_KEY=your-very-secure-secret-key-here-make-it-long-and-random
FLASK_DEBUG=False
```

To generate a secure secret key, you can use:
```python
import secrets
print(secrets.token_hex(32))
```

### 5. Deploy

1. Click "Create Web Service"
2. Render will automatically deploy your application
3. The deployment process usually takes 2-5 minutes

### 6. Access Your Application

Once deployed, your application will be available at:
`https://your-service-name.onrender.com`

## Post-Deployment

### Custom Domain (Optional)
- Go to your service dashboard
- Navigate to "Settings" → "Custom Domains"
- Add your custom domain

### Monitoring
- Check the "Logs" tab for application logs
- Use the "Metrics" tab to monitor performance
- Set up alerts in the "Alerts" section

### SSL Certificate
Render automatically provides SSL certificates for all deployed applications.

## Troubleshooting

### Common Issues

1. **Build Failed**: Check that all dependencies are in `requirements.txt`
2. **App Won't Start**: Verify the start command is correct
3. **500 Errors**: Check application logs in the Render dashboard

### Checking Logs

```bash
# View recent logs
render logs --tail

# Follow logs in real-time
render logs --follow
```

### Health Check

Your application includes a health check endpoint at `/api/health`. Render will automatically use this to monitor your application's status.

## Updating Your Application

1. Push changes to your GitHub repository
2. Render will automatically redeploy your application
3. You can also manually trigger deploys from the Render dashboard

## Performance Tips

1. **Use Redis**: Add Redis for caching (available as Render add-on)
2. **Database**: Add PostgreSQL for persistent data storage
3. **CDN**: Use a CDN for static assets
4. **Monitoring**: Set up application monitoring with services like Sentry

## Need Help?

- Check the [Render Documentation](https://render.com/docs)
- Join the [Render Community](https://community.render.com/)
- Contact Render Support through their dashboard

---

Happy Deploying! 🚀
