from celery import shared_task
from django.core.management import call_command

@shared_task
def run_scraper():
    call_command("scrape_jobs")  # shu yerda sening scraperingni chaqiramiz
