import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')

app = Celery('news')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'send_weekly_mail',
        'schedule': crontab(hour=8, minute=00, day_of_week='monday'),
    },
}


# app.conf.beat_schedule = {
#     'action_every_monday_8am': {
#         'task': 'new.tasks.send_weekly_mail',
#         'schedule': 10,
#     },
# }