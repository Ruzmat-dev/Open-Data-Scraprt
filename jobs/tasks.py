from celery import shared_task
import requests
from jobs.models import Job
from datetime import datetime

@shared_task
def scrape_jobs():
    url = "https://remoteok.com/api"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    data = response.json()

    saved_count = 0
    for job in data[1:]:
        title = job.get('position')
        company = job.get('company')
        link = job.get('url')
        posted_at = datetime.fromtimestamp(job.get('epoch', datetime.now().timestamp()))

        if title and company:
            Job.objects.update_or_create(
                title=title,
                company=company,
                defaults={
                    'url': link,
                    'posted_at': posted_at,
                    'source': 'remoteok.com'
                }
            )
            saved_count += 1

    print(f"✅ Scraping completed! Total saved: {saved_count}")
