
from django.core.management.base import BaseCommand
from django.utils import timezone

from jobs.models import Job


class Command(BaseCommand):
    help = "Automatically deactivate expired jobs"

    def handle(self, *args, **options):
        today = timezone.localdate()

        expired_jobs = Job.objects.filter(
            is_active=True,
            closing_date__lt=today
        )

        count = expired_jobs.count()

        expired_jobs.update(is_active=False)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully deactivated {count} expired job(s)."
            )
        )
