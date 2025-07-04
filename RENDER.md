# WbgNews Flask App - render.yaml Configuration

This project uses Infrastructure as Code with `render.yaml` for easy deployment to Render.

## Quick Start

1. **Fork this repository** to your GitHub account
2. **Connect to Render**:
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Select this repository
3. **Deploy**: Render automatically detects `render.yaml` and deploys your app

## Configuration Details

The `render.yaml` file configures:

- **Service Type**: Web service
- **Runtime**: Python 3
- **Build**: `pip install -r requirements.txt`
- **Start**: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
- **Health Check**: `/api/health` endpoint
- **Auto Deploy**: Enabled on push to main branch
- **Plan**: Free tier
- **Environment**: Production-ready settings

## Environment Variables

Pre-configured in `render.yaml`:
- `FLASK_DEBUG=False` (production mode)
- `PYTHON_VERSION=3.9.16` (specified runtime)

## Health Monitoring

The app includes a health check endpoint at `/api/health` that returns:
```json
{
  "status": "healthy",
  "timestamp": "2025-07-04T...",
  "service": "WbgNews"
}
```

## Scaling

Currently configured for:
- **Min Instances**: 1
- **Max Instances**: 1 (Free tier)

## Custom Domain

After deployment, you can add a custom domain in the Render dashboard under "Settings" → "Custom Domains".

## Logs and Monitoring

Access logs and metrics through the Render dashboard:
- **Logs**: Real-time application logs
- **Metrics**: Performance and usage statistics
- **Alerts**: Configure notifications for issues

---

**Need help?** Check the [Render Documentation](https://render.com/docs) or see `DEPLOYMENT.md` for detailed deployment instructions.
