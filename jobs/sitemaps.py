
from django.contrib.sitemaps import Sitemap
from django.utils import timezone
from django.urls import reverse

from .models import Job


class JobSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Job.objects.filter(
            is_active=True,
            closing_date__gte=timezone.localdate(),
            slug__isnull=False
        ).exclude(
            slug=""
        ).order_by('id')

    def location(self, obj):
        return reverse(
            'job_detail',
            kwargs={'slug': obj.slug}
        )

    def lastmod(self, obj):
        return obj.created_at
