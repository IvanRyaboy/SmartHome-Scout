from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smarthousescout.settings")
celery = Celery("app_celery")
celery.config_from_object("django.conf:settings", namespace="CELERY")
celery.autodiscover_tasks()

celery.conf.update(
    timezone="Europe/Moscow",
    enable_utc=True,
    beat_schedule={
        'get_data_from_flask_once_a_day': {
            'task': 'tasks.start_fetching_flask_data',
            'schedule': crontab(hour=12, minute=0),
        },
    }
)
