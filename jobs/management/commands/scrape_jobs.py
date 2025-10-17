import requests
from django.core.management.base import BaseCommand
from jobs.models import Job
from datetime import datetime

class Command(BaseCommand):
    help = 'Scrape jobs from remoteok.com API'

    def handle(self, *args, **options):
        url = "https://remoteok.com/api"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        data = response.json()

        saved_count = 0
        self.stdout.write(f"🔍 Found {len(data)} records")

        for job in data[1:]:  # 0-index element metadata bo‘ladi
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
                self.stdout.write(f"✅ Saved: {title} at {company}")

        self.stdout.write(self.style.SUCCESS(f"Scraping completed successfully! Total saved: {saved_count}"))
