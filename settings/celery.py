import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "posta_office.settings")

app = Celery("posta_office")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send_newsletter_task": {
        "task": "yourapp.tasks.send_newsletter",
        "schedule": crontab(minute=0, hour=0),
        },
        }
