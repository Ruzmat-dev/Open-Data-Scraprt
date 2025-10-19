# scraper/management/commands/scrape_remoteok.py

import requests
from django.core.management.base import BaseCommand
from django.utils import timezone
from jobs.models import Job
from datetime import datetime


class Command(BaseCommand):
    help = 'Scrape jobs from remoteok.com API and reset DB'

    def handle(self, *args, **options):
        url = "https://remoteok.com/api"
        headers = {'User-Agent': 'Mozilla/5.0'}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"❌ Failed to fetch API: {e}"))
            return

        # DB ni tozalash (0 dan boshlab)
        Job.objects.all().delete()
        self.stdout.write("🗑️ All previous jobs deleted.")

        saved_count = 0
        self.stdout.write(f"🔍 Found {len(data)} records in API response")

        for job in data[1:]:  # 0-index element metadata bo‘ladi
            title = job.get('position')
            company = job.get('company')
            link = job.get('url')

            epoch = job.get('epoch')
            if epoch:
                posted_at = datetime.fromtimestamp(epoch)
            else:
                posted_at = timezone.now()

            if title and company:
                Job.objects.create(
                    title=title,
                    company=company,
                    url=link,
                    posted_at=posted_at,
                    source='remoteok.com'
                )
                saved_count += 1
                self.stdout.write(f"✅ Saved: {title} at {company}")

        self.stdout.write(self.style.SUCCESS(f"🎯 Scraping completed! Total saved: {saved_count}"))
