from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    url = models.URLField()
    posted_at = models.DateTimeField()
    scraped_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    salary = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title
