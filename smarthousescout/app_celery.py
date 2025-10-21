from celery import Celery
from celery.schedules import crontab, timedelta
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smarthousescout.settings")
celery = Celery("app_celery")
celery.config_from_object("django.conf:settings", namespace="CELERY")
celery.autodiscover_tasks()

celery.conf.update(
    timezone="Europe/Moscow",
    enable_utc=True,
    beat_schedule={
        'get_apartments_data_from_flask_once_a_day': {
            'task': 'tasks.start_fetching_apartments_flask_data',
            'schedule': crontab(hour=3, minute=0),
        },
        'get_rent_data_from_flask_once_a_day': {
            'task': 'tasks.start_fetching_rent_flask_data',
            'schedule': crontab(hour=3, minute=0),
        },
    }
)
