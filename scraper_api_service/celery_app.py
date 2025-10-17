import os
from celery import Celery
from celery.schedules import crontab

# Django settings faylini ko‘rsatamiz
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraper_api_service.settings')

app = Celery('scraper_api_service',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')

# Django settingsdan CELERY konfiguratsiyasini yuklaymiz
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django loyihasidagi barcha app-lardagi tasks.py fayllarni avtomatik yuklaydi
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'scrape-every-hour': {
        'task': 'jobs.tasks.scrape_jobs',
        'schedule': 60.0,  # har soatda
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
