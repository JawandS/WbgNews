"""
Celery configuration and worker startup
Run with: celery -A celery_worker.celery worker --loglevel=info
"""

from app import create_app
from tasks import make_celery

app = create_app()
celery = make_celery(app)

if __name__ == '__main__':
    celery.start()
