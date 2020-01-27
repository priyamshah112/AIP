from django.urls import path
from . import views


urlpatterns = [
    path('jobsboard', views.jobsboard, name="jobsboard"),
    path('profile', views.profile, name="profile"),
    path('resume', views.resume, name="resume"),
    path('applications', views.applications, name="applications"),
    path('job_interview', views.jobInterview, name="jobInterview"),
    path('add_application', views.addApplication, name="addApplication"),
]
