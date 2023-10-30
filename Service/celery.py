from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

import dotenv

env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '.env')
dotenv.load_dotenv(env_file)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Service.settings")
app = Celery("Service",broker='redis://localhost:6379/0')

app.config_from_object("django.conf:settings",namespace="CELERY")
app.conf.enable_utc=True

app.conf.update(
    CELERY_ACCEPT_CONTENT = ['json'],
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_RESULT_SERIALIZER = 'json',
)

app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)