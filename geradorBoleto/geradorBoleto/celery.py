import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geradorBoleto.settings')
app = Celery('geradorBoleto')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'America/Sao_Paulo'
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)