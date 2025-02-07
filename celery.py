from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edusson_project.settings')  # Correct the project name

app = Celery('edusson_app')  # Your app name, not project name

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related config keys should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Celery Beat Schedule: Scheduling tasks for periodic execution
app.conf.beat_schedule = {
    'auto-bid-every-hour': {
        'task': 'edusson_app.tasks.run_auto_bidding_task',  # Update with correct task path
        'schedule': crontab(minute=0, hour='*/1'),  # Run every hour
    },
}
