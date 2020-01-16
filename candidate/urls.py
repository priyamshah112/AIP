from django.urls import path
from . import views


urlpatterns = [
    path('jobsboard', views.jobsboard, name="jobsboard"),
    path('profile', views.profile, name="profile"),
    path('resume', views.resume, name="resume"),
    path('applications', views.applications, name="applications"),
    path('psychology', views.psychology, name="psychology"),
    path('video_resume', views.videoResume, name="videoResume"),
    path('mock_interview', views.mockInterview, name="mockInterview"),
    path('job_interview', views.jobInterview, name="jobInterview"),
    path('add_application', views.addApplication, name="addApplication"),
    path('external_interview', views.externalInterview, name="externalInterview"),
]
