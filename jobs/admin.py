
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Job, Application


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'location',
        'department',
        'job_type',
        'closing_date',
        'is_active',
    )
    list_filter = ('is_active', 'job_type', 'department')
    search_fields = ('title', 'location', 'department')



@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'email',
        'job',
        'applied_at',
        'view_resume',
    )

    search_fields = ('full_name', 'email')
    list_filter = ('applied_at',)

    readonly_fields = ('resume_preview',)

    fields = (
        'job',
        'full_name',
        'email',
        'phone',
        'resume',
        'resume_preview',
        'cover_letter',
    )

    @admin.display(description='Resume Preview')
    def resume_preview(self, obj):
        if obj and obj.resume:
            url = reverse(
                'download_resume',
                args=[obj.id]
            )

            return format_html(
                '<iframe src="{}" width="100%" height="700" '
                'style="border:1px solid #ccc; border-radius:8px;" '
                'title="Applicant Resume"></iframe>',
                url
            )

        return "No resume uploaded"

    @admin.display(description='Resume')
    def view_resume(self, obj):
        if obj and obj.resume:
            url = reverse(
                'download_resume',
                args=[obj.id]
            )
            return format_html(
                '<a href="{}" target="_blank">View Resume</a>',
                url
            )

        return "No resume"
