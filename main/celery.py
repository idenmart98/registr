import os
from django.conf import settings
from celery import Celery

if not ("DJANGO_SETTINGS_MODULE" in os.environ):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','main.settings')

app = Celery('main')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.task_always_eager = False


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))