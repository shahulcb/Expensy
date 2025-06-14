from __future__ import absolute_import  
from celery import Celery
import os  
from django.conf import settings  
from celery import Celery
from celery.schedules import crontab
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expensy.settings')

app = Celery('expensy')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

app.conf.beat_schedule = {
    'delete-expired-otps-every-3-minutes': {
        'task': 'user.tasks.delete_expired_otps',
        'schedule': crontab(minute='*/3'), 
    },
}
