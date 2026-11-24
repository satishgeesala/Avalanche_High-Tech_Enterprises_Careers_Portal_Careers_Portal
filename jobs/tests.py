

import json
import re
from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from jobs.models import Job


class JobSEOTests(TestCase):

    def setUp(self):
        self.job = Job.objects.create(
            title="Python Developer Intern",
            slug="python-developer-intern",
            description="Develop Python applications using Django.",
            location="Hyderabad",
            department="IT",
            job_type="Internship",
            salary="15000",
            closing_date=timezone.localdate() + timedelta(days=30),
            is_active=True,
        )

    def test_job_detail_returns_200(self):
        response = self.client.get(
            reverse('job_detail', kwargs={'slug': self.job.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_job_detail_contains_json_ld(self):
        response = self.client.get(
            reverse('job_detail', kwargs={'slug': self.job.slug})
        )
        self.assertContains(response, 'application/ld+json')
        self.assertContains(response, 'JobPosting')

    def test_json_ld_is_valid(self):
        response = self.client.get(
            reverse('job_detail', kwargs={'slug': self.job.slug})
        )
        html = response.content.decode()

        match = re.search(
            r'<script type="application/ld\+json">(.*?)</script>',
            html,
            re.DOTALL
        )

        self.assertIsNotNone(match)
        data = json.loads(match.group(1))

        self.assertEqual(data['@type'], 'JobPosting')
        self.assertEqual(data['title'], self.job.title)
        self.assertEqual(
            data['hiringOrganization']['name'],
            'Avalanche High-Tech Enterprises'
        )

    def test_expired_job_returns_404(self):
        self.job.closing_date = timezone.localdate() - timedelta(days=1)
        self.job.save()

        response = self.client.get(
            reverse('job_detail', kwargs={'slug': self.job.slug})
        )
        self.assertEqual(response.status_code, 404)

    def test_sitemap_contains_active_job(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.job.slug)

    def test_sitemap_excludes_expired_job(self):
        self.job.closing_date = timezone.localdate() - timedelta(days=1)
        self.job.save()

        response = self.client.get('/sitemap.xml')
        self.assertNotContains(response, self.job.slug)

    def test_expire_jobs_command(self):
        expired_job = Job.objects.create(
            title="Expired Developer",
            slug="expired-developer",
            description="Expired job description",
            location="Hyderabad",
            department="IT",
            job_type="Full-time",
            salary="20000",
            closing_date=timezone.localdate() - timedelta(days=1),
            is_active=True,
        )

        call_command('expire_jobs')

        expired_job.refresh_from_db()
        self.assertFalse(expired_job.is_active)

        self.job.refresh_from_db()
        self.assertTrue(self.job.is_active)
