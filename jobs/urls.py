
from django.urls import path
from . import views

from django.contrib.sitemaps.views import sitemap
from jobs.sitemaps import JobSitemap

sitemaps = {
    'jobs': JobSitemap,
}

urlpatterns = [
    path('', views.home, name='home'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<slug:slug>/', views.job_detail, name='job_detail'),
    path('jobs/<slug:slug>/apply/', views.apply_job, name='apply_job'),
    path('thank-you/', views.thank_you, name='thank_you'),
    
    path(
        'resume/<int:application_id>/',
        views.download_resume,
        name='download_resume'
    ),

    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]